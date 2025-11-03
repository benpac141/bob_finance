"""
Génère un rapport PDF enrichi avec analyse par profil.
"""

import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

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

# Chemins
DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.xlsx"
MARGINS_FILE = Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "reports"


def main():
    """Fonction principale."""
    print("="*70)
    print("GENERATION DU RAPPORT PDF ENRICHI")
    print("="*70)
    
    try:
        # Charger les données
        print("\nChargement des donnees...")
        df = pd.read_excel(DATA_FILE)
        margins = pd.read_csv(MARGINS_FILE)
        df_besancon = df[df['is_besancon']].copy()
        
        print(f"  - {len(df_besancon)} repondants Besancon")
        print(f"  - Population totale : {int(margins['population'].sum()):,}")
        
        # Créer le répertoire de sortie
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Générer le rapport
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f'rapport_enrichi_{timestamp}.pdf'
        
        print(f"\nGeneration du rapport : {output_path}")
        
        # Créer le document
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            topMargin=2*cm,
            bottomMargin=2*cm,
            leftMargin=2*cm,
            rightMargin=2*cm
        )
        
        # Styles
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
        
        # Contenu
        story = []
        
        # Page de titre
        story.append(Spacer(1, 2*cm))
        story.append(Paragraph("Enquete BOB - Bibliotheque d'Objets Besancon", styles['CustomTitle']))
        story.append(Paragraph("Rapport d'Analyse Enrichi", styles['Heading2']))
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph(f"<i>Date : {datetime.now().strftime('%d/%m/%Y')}</i>", styles['CustomBody']))
        story.append(Spacer(1, 1*cm))
        
        # Introduction
        intro_text = f"""
        Ce rapport presente une analyse approfondie de l'enquete BOB menee aupres de 
        {len(df_besancon)} habitants du centre-ville de Besancon. L'analyse inclut un redressement 
        statistique pour representer fidelement la population cible ({int(margins['population'].sum()):,} habitants) 
        ainsi qu'une segmentation par profil demographique.
        """
        story.append(Paragraph(intro_text, styles['CustomBody']))
        
        # Ajouter les sections enrichies
        print("  - Ajout de l'analyse par profil...")
        add_profile_analysis_section(story, df_besancon, styles)
        
        print("  - Ajout des segments cibles...")
        add_target_segments_section(story, df_besancon, margins, styles)
        
        print("  - Ajout de la comparaison methodologique...")
        add_methodology_comparison_section(story, df_besancon, margins, styles)
        
        # Générer le PDF
        print("  - Generation du PDF...")
        doc.build(story)
        
        print("\n" + "="*70)
        print("SUCCES !")
        print("="*70)
        print(f"Rapport genere : {output_path}")
        print("\nContenu :")
        print("  - Page 1 : Introduction")
        print("  - Pages 2-3 : Analyse par profil demographique")
        print("  - Page 4 : Segments cibles prioritaires")
        print("  - Page 5 : Comparaison methodologique")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

