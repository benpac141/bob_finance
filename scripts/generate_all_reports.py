"""
Script master pour générer TOUS les rapports et analyses en une seule fois.

Évite les doublons en exécutant chaque étape une seule fois.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Imports des modules
from utils import load_config, setup_logging
from load_clean import load_survey_data, load_margins, prepare_margins_dict, add_initial_weights
from raking import RakingWeighter
from analysis import quality_metrics

# Chemins
BASE_DIR = Path(__file__).parent.parent
DATA_FILE = BASE_DIR / "data" / "raw" / "enquete_all_prepared.xlsx"
MARGINS_FILE = BASE_DIR / "data" / "margins" / "margins_center.csv"
OUTPUT_DIR = BASE_DIR / "outputs"


def main():
    """Fonction principale."""
    logger = setup_logging(level="INFO")
    
    print("="*70)
    print("GENERATION COMPLETE DE TOUS LES RAPPORTS")
    print("="*70)
    print(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    try:
        # =====================================================================
        # ETAPE 1 : PREPARATION DES DONNEES
        # =====================================================================
        print(f"\n{'='*70}")
        print("ETAPE 1/6 : PREPARATION DES DONNEES")
        print(f"{'='*70}")
        
        if not DATA_FILE.exists():
            print("Execution de prepare_bob_with_all_respondents.py...")
            import subprocess
            result = subprocess.run(
                [sys.executable, BASE_DIR / "scripts" / "prepare_bob_with_all_respondents.py"],
                capture_output=True
            )
            if result.returncode != 0:
                print("[ERREUR] Echec de la preparation des donnees")
                return 1
        else:
            print(f"[OK] Donnees deja preparees : {DATA_FILE}")
        
        # =====================================================================
        # ETAPE 2 : RAPPORT DE SYNTHESE EXECUTIF
        # =====================================================================
        print(f"\n{'='*70}")
        print("ETAPE 2/6 : RAPPORT DE SYNTHESE EXECUTIF")
        print(f"{'='*70}")
        
        from generate_executive_summary import create_executive_summary
        
        output_synthese = OUTPUT_DIR / "reports" / f'synthese_executive_{timestamp}.pdf'
        create_executive_summary(output_synthese)
        print(f"[OK] {output_synthese}")
        
        # =====================================================================
        # ETAPE 3 : RAPPORT ENRICHI
        # =====================================================================
        print(f"\n{'='*70}")
        print("ETAPE 3/6 : RAPPORT ENRICHI")
        print(f"{'='*70}")
        
        # Charger les données
        df = pd.read_excel(DATA_FILE)
        margins = pd.read_csv(MARGINS_FILE)
        df_besancon = df[df['is_besancon']].copy()
        
        # Générer le rapport enrichi
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
        
        from pdf_report_enriched import (
            add_profile_analysis_section,
            add_target_segments_section,
            add_methodology_comparison_section
        )
        
        output_enrichi = OUTPUT_DIR / "reports" / f'rapport_enrichi_{timestamp}.pdf'
        
        doc = SimpleDocTemplate(
            str(output_enrichi),
            pagesize=A4,
            topMargin=2*cm,
            bottomMargin=2*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=styles['Title'],
            fontSize=22,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=20
        ))
        styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10
        ))
        styles.add(ParagraphStyle(
            name='CustomBody',
            parent=styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        story = []
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("Enquete BOB - Bibliotheque d'Objets Besancon", styles['CustomTitle']))
        story.append(Paragraph("Rapport d'Analyse Enrichi", styles['Heading2']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"<i>Date : {datetime.now().strftime('%d/%m/%Y')}</i>", styles['CustomBody']))
        story.append(Spacer(1, 1*cm))
        
        intro_text = f"""
        Ce rapport presente une analyse approfondie de l'enquete BOB menee aupres de 
        {len(df_besancon)} habitants du centre-ville de Besancon. L'analyse inclut un redressement 
        statistique pour representer fidelement la population cible ({int(margins['population'].sum()):,} habitants) 
        ainsi qu'une segmentation par profil demographique.
        """
        story.append(Paragraph(intro_text, styles['CustomBody']))
        
        add_profile_analysis_section(story, df_besancon, styles)
        add_target_segments_section(story, df_besancon, margins, styles)
        add_methodology_comparison_section(story, df_besancon, margins, styles)
        
        doc.build(story)
        print(f"[OK] {output_enrichi}")
        
        # =====================================================================
        # ETAPE 4 : TABLEAU DE BORD
        # =====================================================================
        print(f"\n{'='*70}")
        print("ETAPE 4/6 : TABLEAU DE BORD")
        print(f"{'='*70}")
        
        from create_dashboard import (
            create_heatmap_age_sexe,
            create_barplot_by_profile,
            create_pyramid_chart,
            create_contribution_chart,
            create_summary_dashboard
        )
        
        figures_dir = OUTPUT_DIR / "figures"
        
        create_heatmap_age_sexe(df_besancon, figures_dir / f'dashboard_heatmap_{timestamp}.png')
        create_barplot_by_profile(df_besancon, figures_dir / f'dashboard_barplot_{timestamp}.png')
        create_pyramid_chart(df_besancon, margins, figures_dir / f'dashboard_pyramid_{timestamp}.png')
        create_contribution_chart(df_besancon, margins, figures_dir / f'dashboard_contribution_{timestamp}.png')
        create_summary_dashboard(df_besancon, margins, figures_dir / f'dashboard_summary_{timestamp}.png')
        
        print(f"[OK] 5 visualisations generees")
        
        # =====================================================================
        # ETAPE 5 : BUDGET PREVISIONNEL SIMPLE
        # =====================================================================
        print(f"\n{'='*70}")
        print("ETAPE 5/6 : BUDGET PREVISIONNEL SIMPLE")
        print(f"{'='*70}")
        
        from budget_simulator import (
            calculate_potential_by_profile,
            generate_scenarios,
            export_budget_excel
        )
        
        df_potential = calculate_potential_by_profile(df_besancon, margins)
        scenarios = generate_scenarios(df_potential)
        
        output_budget = OUTPUT_DIR / "reports" / f'budget_previsionnel_{timestamp}.xlsx'
        export_budget_excel(scenarios, output_budget)
        print(f"[OK] {output_budget}")
        
        # =====================================================================
        # ETAPE 6 : BUDGET INTERACTIF
        # =====================================================================
        print(f"\n{'='*70}")
        print("ETAPE 6/6 : BUDGET INTERACTIF")
        print(f"{'='*70}")
        
        from budget_simulator_interactive import (
            analyze_profile_behaviors,
            generate_simulation,
            export_simulation_excel
        )
        
        df_behaviors = analyze_profile_behaviors(df_besancon)
        
        simulations = {}
        simulations['500_adherents_An1'] = generate_simulation(
            500, df_behaviors, margins, "500 adherents (Annee 1)"
        )
        simulations['1000_adherents_An2'] = generate_simulation(
            1000, df_behaviors, margins, "1000 adherents (Annee 2)"
        )
        simulations['1500_adherents_An3'] = generate_simulation(
            1500, df_behaviors, margins, "1500 adherents (Annee 3)"
        )
        simulations['2000_adherents_LT'] = generate_simulation(
            2000, df_behaviors, margins, "2000 adherents (Long terme)"
        )
        
        output_interactif = OUTPUT_DIR / "reports" / f'budget_interactif_{timestamp}.xlsx'
        export_simulation_excel(simulations, output_interactif)
        print(f"[OK] {output_interactif}")
        
        # =====================================================================
        # RESUME FINAL
        # =====================================================================
        print(f"\n{'='*70}")
        print("GENERATION TERMINEE AVEC SUCCES !")
        print(f"{'='*70}")
        
        print(f"\nFICHIERS GENERES :")
        print(f"\n1. RAPPORTS PDF :")
        print(f"   - {output_synthese.name}")
        print(f"   - {output_enrichi.name}")
        
        print(f"\n2. VISUALISATIONS :")
        print(f"   - dashboard_heatmap_{timestamp}.png")
        print(f"   - dashboard_barplot_{timestamp}.png")
        print(f"   - dashboard_pyramid_{timestamp}.png")
        print(f"   - dashboard_contribution_{timestamp}.png")
        print(f"   - dashboard_summary_{timestamp}.png")
        
        print(f"\n3. BUDGETS EXCEL :")
        print(f"   - {output_budget.name}")
        print(f"   - {output_interactif.name}")
        
        print(f"\nTous les fichiers utilisent le meme timestamp : {timestamp}")
        print(f"{'='*70}")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

