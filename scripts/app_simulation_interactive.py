"""
Application web interactive pour simuler le budget avec des curseurs.

Utilise Streamlit pour créer une interface graphique interactive.

Installation :
    pip install streamlit plotly

Lancement :
    streamlit run scripts/app_simulation_interactive.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import yaml
import re
from datetime import datetime
import io
import base64

# Ajouter le chemin
BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / "src"))
sys.path.insert(0, str(SCRIPT_DIR))

# Imports
from scripts.budget_simulator_interactive import (
    load_data,
    analyze_profile_behaviors,
    distribute_adherents_by_profile,
    calculate_recettes_by_profile
)
from raking import RakingWeighter

# Le thème est chargé par chemin absolu : sur Streamlit Cloud, le dossier
# scripts/ est celui du fichier principal, alors que src/ n'est pas toujours
# visible comme module.
import importlib.util

_theme_path = SCRIPT_DIR / "ui_theme.py"
_theme_spec = importlib.util.spec_from_file_location("bob_ui_theme", _theme_path)
if _theme_spec is None or _theme_spec.loader is None:
    raise ImportError(f"Module de thème introuvable : {_theme_path}")
_theme = importlib.util.module_from_spec(_theme_spec)
sys.modules["bob_ui_theme"] = _theme
_theme_spec.loader.exec_module(_theme)

COLORS = _theme.COLORS
PALETTE = _theme.PALETTE
SCALE_TEAL = _theme.SCALE_TEAL
apply_theme_css = _theme.apply_theme_css
apply_plotly_theme = _theme.apply_plotly_theme
render_hero = _theme.render_hero
render_section = _theme.render_section
render_kpi_grid = _theme.render_kpi_grid
render_status_banner = _theme.render_status_banner
render_tariff_grid = _theme.render_tariff_grid

# Imports pour PDF
try:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
        PageBreak, Image, KeepTogether
    )
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    st.warning("⚠️ ReportLab n'est pas installé. L'export PDF n'est pas disponible. Installez avec: pip install reportlab")

# Fonction pour obtenir des couleurs distinctes pour les graphiques en camembert
def get_distinct_colors(labels, color_scheme='default'):
    """
    Génère une liste de couleurs distinctes pour les graphiques en camembert.
    
    Args:
        labels: Liste des labels à colorer
        color_scheme: 'default', 'positive_negative', ou 'sequential'
    
    Returns:
        Liste de couleurs hexadécimales
    """
    # Palette de couleurs distinctes (thème BOB)
    palette_default = list(PALETTE)
    
    # Palette pour positive/negative (vert = positif, rouge = négatif, orange = neutre)
    # Ordre de priorité : chercher d'abord les correspondances spécifiques
    palette_positive_negative = {
        # Catégories négatives
        'non, je ne souhaiterai pas': COLORS['danger'],
        'non, je ne souhaiterais pas': COLORS['danger'],
        'non': COLORS['female'],
        
        # Catégories positives avec montants
        'oui, entre 20€ et 30€': COLORS['ink'],
        'oui, entre 10€ et 20€': COLORS['primary'],
        'oui, entre 1€ et 10€': COLORS['sage'],
        'oui, entre': COLORS['sage'],
        
        # Catégories neutres/intermédiaires
        'peut-être': COLORS['accent'],
        'peut être': COLORS['accent'],
        
        # Catégories positives simples
        'oui': COLORS['success'],
    }
    
    colors = []
    
    if color_scheme == 'positive_negative':
        # Utiliser la palette positive/negative avec fallback
        # Trier les clés par longueur décroissante pour prioriser les correspondances les plus spécifiques
        sorted_keys = sorted(palette_positive_negative.keys(), key=len, reverse=True)
        
        # Garder une trace des couleurs déjà utilisées pour éviter les doublons
        used_colors = []
        
        for i, label in enumerate(labels):
            label_str = str(label).lower()
            color_found = None
            
            # Chercher les correspondances par ordre de spécificité (du plus spécifique au plus général)
            for key in sorted_keys:
                if key in label_str:
                    color_candidate = palette_positive_negative[key]
                    # Si cette couleur n'a pas encore été utilisée, l'utiliser
                    if color_candidate not in used_colors:
                        color_found = color_candidate
                        used_colors.append(color_found)
                        break
            
            # Si aucune couleur spécifique trouvée ou déjà utilisée, utiliser palette par défaut
            if not color_found:
                # Chercher une couleur disponible dans la palette par défaut
                for default_color in palette_default:
                    if default_color not in used_colors:
                        color_found = default_color
                        used_colors.append(color_found)
                        break
                
                # Si toutes les couleurs sont utilisées, réutiliser avec rotation
                if not color_found:
                    color_found = palette_default[i % len(palette_default)]
            
            colors.append(color_found)
    else:
        # Utiliser la palette par défaut avec rotation
        for i in range(len(labels)):
            colors.append(palette_default[i % len(palette_default)])
    
    return colors


# Fonction pour exporter les graphiques Plotly en images
def export_plotly_figure(fig, output_path):
    """Exporte un graphique Plotly en PNG."""
    try:
        # Essayer avec write_image (nécessite kaleido)
        fig.write_image(str(output_path), width=800, height=600, scale=2)
        return True
    except Exception as e:
        # Si kaleido n'est pas disponible, essayer une autre méthode
        try:
            import plotly.io as pio
            if hasattr(pio, 'kaleido'):
                pio.kaleido.scope.default_format = "png"
                fig.write_image(str(output_path), width=800, height=600, scale=2)
                return True
        except:
            pass
        
        # Si tout échoue, utiliser to_html puis convertir (moins optimal)
        try:
            html_path = str(output_path).replace('.png', '.html')
            fig.write_html(html_path)
            st.warning(f"⚠️ Graphique exporté en HTML : {html_path}. Installez kaleido pour exporter en PNG : `pip install kaleido`")
            return False
        except Exception as e2:
            st.warning(f"⚠️ Impossible d'exporter le graphique : {e}. Installez kaleido : `pip install kaleido`")
            return False


def generate_scenario_pdf(scenario_data, output_path):
    """
    Génère un PDF de rapport pour un scénario.
    
    Args:
        scenario_data: Dictionnaire contenant toutes les données du scénario
        output_path: Chemin où sauvegarder le PDF
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("ReportLab n'est pas installé")
    
    doc = SimpleDocTemplate(str(output_path), pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Style personnalisé pour le titre
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#14635C'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    # Page de garde
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("Rapport de Scénario BOB", title_style))
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph(f"<b>Bibliothèque d'Objets Besançon</b>", styles['Normal']))
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph(f"Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
    story.append(PageBreak())
    
    # 1. Hypothèses du scénario
    story.append(Paragraph("1. Hypothèses du Scénario", styles['Heading1']))
    story.append(Spacer(1, 0.5*cm))
    
    # Tableau des hypothèses
    hypotheses_data = [
        ['Paramètre', 'Valeur'],
        ['Nombre d\'adhérents cible', format_nombre(scenario_data['nb_adherents'])],
        ['Tarif Solidaire', f"{scenario_data['cotisation_solidaire']} €"],
        ['Tarif Normal', f"{scenario_data['cotisation_normale']} €"],
        ['Tarif Soutien', f"{scenario_data['cotisation_soutien']} €"],
        ['Prix location moyen', f"{scenario_data['prix_location']} €/jour"],
        ['Nombre locations/an/adhérent', format_nombre(scenario_data['nb_locations_moyen'])],
        ['Dépense moyenne mensuelle', f"{format_nombre(scenario_data.get('depense_mensuelle', 0))} €"],
        ['Tarif solidaire sur justificatif', 'Oui' if scenario_data.get('mode_justificatif') else 'Non'],
    ]
    
    hypotheses_table = Table(hypotheses_data, colWidths=[8*cm, 8*cm])
    hypotheses_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14635C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(hypotheses_table)
    story.append(Spacer(1, 1*cm))
    
    # Répartition des tarifs par profil
    story.append(Paragraph("1.1. Répartition des Tarifs par Profil", styles['Heading2']))
    story.append(Spacer(1, 0.3*cm))
    
    # Tableau des proportions
    proportions_data = [['Profil', 'Solidaire (%)', 'Normal (%)', 'Soutien (%)']]
    for nom_profil, props in scenario_data['proportions_par_profil'].items():
        proportions_data.append([
            nom_profil,
            format_nombre(props['solidaire'] * 100, 1),
            format_nombre(props['normale'] * 100, 1),
            format_nombre(props['soutien'] * 100, 1)
        ])
    
    proportions_table = Table(proportions_data, colWidths=[6*cm, 3*cm, 3*cm, 3*cm])
    proportions_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14635C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(proportions_table)
    story.append(PageBreak())
    
    # 2. KPIs principaux
    story.append(Paragraph("2. Indicateurs Clés (KPIs)", styles['Heading1']))
    story.append(Spacer(1, 0.5*cm))
    
    kpis_data = [
        ['Indicateur', 'Valeur'],
        ['Nombre total d\'adhérents', format_nombre(scenario_data['total_adherents'])],
        ['Recettes cotisations', f"{format_nombre(scenario_data['total_cotisations'])} €"],
        ['Recettes locations', f"{format_nombre(scenario_data['total_locations'])} €"],
        ['Recettes totales', f"{format_nombre(scenario_data['total_recettes'])} €"],
        ['Recette moyenne par adhérent', f"{format_nombre(scenario_data['recette_par_adherent'])} €"],
        ['Cotisation moyenne', f"{format_nombre(scenario_data['cotisation_moyenne'])} €"],
        ['Dépense moyenne mensuelle', f"{format_nombre(scenario_data.get('depense_mensuelle', 0))} €"],
        ['Charges annuelles', f"{format_nombre(scenario_data.get('depenses_annuelles', 0))} €"],
        ['Recettes mensuelles', f"{format_nombre(scenario_data.get('recettes_mensuelles', 0))} €"],
        ['Résultat mensuel', f"{format_nombre(scenario_data.get('resultat_mensuel', 0))} €"],
        ['Résultat annuel', f"{format_nombre(scenario_data.get('resultat_annuel', 0))} €"],
        ['Taux de couverture des charges', f"{format_nombre(scenario_data.get('taux_couverture') or 0, 1)}%"],
        ['Seuil de rentabilité (adhérents)', format_nombre(scenario_data.get('seuil_adherents') or 0)],
        ['Répartition solidaire', f"{format_nombre(scenario_data['pct_solidaire'], 1)}%"],
        ['Répartition normal', f"{format_nombre(scenario_data['pct_normale'], 1)}%"],
        ['Répartition soutien', f"{format_nombre(scenario_data['pct_soutien'], 1)}%"],
    ]
    
    kpis_table = Table(kpis_data, colWidths=[8*cm, 8*cm])
    kpis_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3D8B7A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(kpis_table)
    story.append(PageBreak())
    
    # 3. Graphiques
    if 'graphiques_paths' in scenario_data and scenario_data['graphiques_paths']:
        story.append(Paragraph("3. Visualisations", styles['Heading1']))
        story.append(Spacer(1, 0.5*cm))
        
        for i, (titre, path) in enumerate(scenario_data['graphiques_paths'], 1):
            if Path(path).exists():
                story.append(Paragraph(f"3.{i}. {titre}", styles['Heading2']))
                story.append(Spacer(1, 0.3*cm))
                img = Image(str(path), width=16*cm, height=12*cm)
                story.append(img)
                story.append(Spacer(1, 0.5*cm))
                if i < len(scenario_data['graphiques_paths']):
                    story.append(PageBreak())
    
    # 4. Tableau détaillé par profil
    story.append(Paragraph("4. Détails par Profil", styles['Heading1']))
    story.append(Spacer(1, 0.5*cm))
    
    df_detailed = scenario_data['df_result']
    detailed_data = [['Profil', 'Âge', 'CSP', 'Adhérents', 'Cotis. Moy.', 'Loc/an', 'Rev. Total']]
    
    for _, row in df_detailed.iterrows():
        detailed_data.append([
            row.get('profil', ''),
            row.get('age_group', ''),
            row.get('csp', ''),
            format_nombre(row.get('nb_adherents', 0)),
            f"{format_nombre(row.get('cotisation_moyenne', 0), 2)} €",
            format_nombre(row.get('nb_locations_an', 0)),
            f"{format_nombre(row.get('recettes_totales', 0))} €"
        ])
    
    detailed_table = Table(detailed_data, colWidths=[3*cm, 2*cm, 3*cm, 2*cm, 2*cm, 2*cm, 2*cm])
    detailed_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#14635C')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(detailed_table)
    
    # Générer le PDF
    doc.build(story)
    return output_path


# Fonction helper pour formater les nombres en français
def format_nombre(nombre, decimals=0):
    """
    Formate un nombre selon le format français : virgule pour décimales, pas de séparateur de milliers.
    
    Args:
        nombre: Nombre à formater
        decimals: Nombre de décimales (0 pour entier)
    
    Returns:
        str: Nombre formaté
    """
    if pd.isna(nombre):
        return "N/A"
    
    if decimals == 0:
        return f"{int(round(nombre)):d}"
    else:
        return f"{nombre:.{decimals}f}".replace('.', ',')


def evaluer_equilibre(
    total_recettes,
    total_cotisations,
    total_locations,
    total_adherents,
    depense_mensuelle,
    nb_locations_moyen,
):
    """
    Met les recettes du scénario en regard d'une dépense mensuelle moyenne.

    Le seuil d'adhérents suppose que la recette par adhérent reste celle du
    scénario actuel (même mix tarifaire et même fréquence de location).
    """
    total_recettes = float(total_recettes)
    total_cotisations = float(total_cotisations)
    total_locations = float(total_locations)
    total_adherents = float(total_adherents)
    depense_mensuelle = float(depense_mensuelle)
    nb_locations_moyen = float(nb_locations_moyen)

    recettes_mensuelles = total_recettes / 12.0
    depenses_annuelles = depense_mensuelle * 12.0
    resultat_mensuel = recettes_mensuelles - depense_mensuelle
    resultat_annuel = total_recettes - depenses_annuelles
    recette_par_adherent = total_recettes / total_adherents if total_adherents else 0.0
    cout_par_adherent = depenses_annuelles / total_adherents if total_adherents else 0.0

    if recette_par_adherent > 0:
        seuil_adherents = int(np.ceil(depenses_annuelles / recette_par_adherent - 1e-9))
        ecart_adherents = int(round(total_adherents - seuil_adherents))
    else:
        seuil_adherents = None
        ecart_adherents = None

    taux_couverture = (
        total_recettes / depenses_annuelles * 100 if depenses_annuelles > 0 else None
    )
    marge_nette = resultat_annuel / total_recettes * 100 if total_recettes else None
    couverture_cotisations = (
        total_cotisations / depenses_annuelles * 100 if depenses_annuelles > 0 else None
    )
    couverture_locations = (
        total_locations / depenses_annuelles * 100 if depenses_annuelles > 0 else None
    )

    besoin_annuel = max(0.0, depenses_annuelles - total_recettes)
    hausse_cotisation = besoin_annuel / total_adherents if total_adherents else None
    locations_totales = total_adherents * nb_locations_moyen
    hausse_prix_location = besoin_annuel / locations_totales if locations_totales else None

    return {
        "recettes_mensuelles": recettes_mensuelles,
        "depense_mensuelle": depense_mensuelle,
        "depenses_annuelles": depenses_annuelles,
        "resultat_mensuel": resultat_mensuel,
        "resultat_annuel": resultat_annuel,
        "recette_par_adherent": recette_par_adherent,
        "cout_par_adherent": cout_par_adherent,
        "seuil_adherents": seuil_adherents,
        "ecart_adherents": ecart_adherents,
        "taux_couverture": taux_couverture,
        "marge_nette": marge_nette,
        "couverture_cotisations": couverture_cotisations,
        "couverture_locations": couverture_locations,
        "besoin_annuel": besoin_annuel,
        "hausse_cotisation": hausse_cotisation,
        "hausse_prix_location": hausse_prix_location,
        "equilibre": resultat_annuel >= -0.5,
    }


def tableau_sensibilite_charges(total_recettes, total_cotisations, total_locations, total_adherents, nb_locations_moyen, depense_courante):
    """Quelques niveaux de charges pour situer le scénario."""
    niveaux = [50, 150, 300, 500, 1000, 2000, 5000]
    if int(depense_courante) not in niveaux:
        niveaux.append(int(round(depense_courante)))
        niveaux = sorted(set(niveaux))

    lignes = []
    for niveau in niveaux:
        eq = evaluer_equilibre(
            total_recettes,
            total_cotisations,
            total_locations,
            total_adherents,
            niveau,
            nb_locations_moyen,
        )
        lignes.append({
            "Dépense mensuelle (€)": niveau,
            "Charges annuelles (€)": int(round(eq["depenses_annuelles"])),
            "Résultat annuel (€)": int(round(eq["resultat_annuel"])),
            "Couverture (%)": None if eq["taux_couverture"] is None else round(eq["taux_couverture"], 1),
            "Seuil d'adhérents": eq["seuil_adherents"] if eq["seuil_adherents"] is not None else "—",
            "Scénario": "Actuel" if niveau == int(round(depense_courante)) else "",
        })
    return pd.DataFrame(lignes)

# Configuration de la page
st.set_page_config(
    page_title="BOB Finance — Simulateur budgétaire",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thème graphique professionnel
st.markdown(f"<style>{apply_theme_css()}</style>", unsafe_allow_html=True)

# Cache des données
@st.cache_data
def load_cached_data():
    """Charge les données avec cache."""
    df, margins = load_data()
    df_behaviors = analyze_profile_behaviors(df)
    return df, margins, df_behaviors


@st.cache_data
def load_weighted_survey_data():
    """
    Charge et redresse les données de l'enquête pour visualisation.
    
    Returns:
        df_weighted: DataFrame avec poids calculés
        config: Configuration du projet
    """
    # Charger la configuration
    config_path = BASE_DIR / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Charger les données
    data_path = BASE_DIR / config['paths']['raw_data']
    margins_path = BASE_DIR / config['paths']['margins']
    
    df = pd.read_excel(data_path)
    margins_df = pd.read_csv(margins_path)
    
    # Filtrer sur Besançon pour le redressement
    df_besancon = df[df['is_besancon'] == 1].copy()
    
    # Mapping CSP : Numérique → Texte
    csp_mapping = {
        1: 'Actifs',
        2: 'Etudiants/Chomeurs',
        3: 'Retraites',
        1.0: 'Actifs',
        2.0: 'Etudiants/Chomeurs',
        3.0: 'Retraites'
    }
    
    # Convertir CSP en texte pour l'échantillon
    df_besancon['csp'] = df_besancon['csp'].map(csp_mapping).fillna(df_besancon['csp'])
    
    # Convertir CSP en texte pour les marges
    margins_df['csp'] = margins_df['csp'].map(csp_mapping).fillna(margins_df['csp'])
    
    # Préparer les marges au format dictionnaire
    margins_dict = {}
    for var in config['survey']['weighting_vars']:
        if var in margins_df.columns:
            var_margins = margins_df.groupby(var)['population'].sum()
            margins_dict[var] = var_margins
    
    # Créer le weighter
    weighter = RakingWeighter(
        max_iterations=config['raking']['max_iterations'],
        tolerance=config['raking']['tolerance'],
        min_weight=config['raking']['min_weight'],
        max_weight=config['raking']['max_weight']
    )
    
    # Initialiser les poids
    df_besancon['weight'] = config['raking']['initial_weight']
    
    # Appliquer le redressement
    df_weighted = weighter.rake(df_besancon, margins_dict, weight_col='weight')
    
    return df_weighted, config




def attribuer_type_cotisation(age_group, csp):
    """
    Attribue un type de cotisation selon le profil.
    
    Règles :
    - Solidaire : Étudiants/Chômeurs, Jeunes (18-24)
    - Normal : Actifs, 25-54 ans
    - Soutien : Retraités avec moyens, Actifs 45-54 ans
    
    Returns:
        str: 'solidaire', 'normale', ou 'soutien'
    """
    # Tarif solidaire pour étudiants/chômeurs et jeunes
    if csp == 'Etudiants/Chomeurs':
        return 'solidaire'
    if age_group == '18-24':
        return 'solidaire'
    
    # Tarif soutien pour les plus aisés
    if csp == 'Retraites' and age_group in ['55-64', '65+']:
        # 30% des retraités prennent le tarif soutien
        return 'soutien' if np.random.random() < 0.3 else 'normale'
    
    if csp == 'Actifs' and age_group in ['45-54', '55-64']:
        # 40% des actifs seniors prennent le tarif soutien
        return 'soutien' if np.random.random() < 0.4 else 'normale'
    
    # Tarif normal pour tous les autres
    return 'normale'


CSP_ELIGIBLES_JUSTIFICATIF = {'Etudiants/Chomeurs'}


def normaliser_csp(csp):
    """Aligne les libellés de CSP utilisés dans les profils et dans les données."""
    if csp is None:
        return None
    aliases = {
        'Retraites': 'Retraites/Inactifs',
        'Retraités': 'Retraites/Inactifs',
        'Retraites/Inactifs': 'Retraites/Inactifs',
        'Étudiants/Chômeurs': 'Etudiants/Chomeurs',
        'Etudiants/Chomeurs': 'Etudiants/Chomeurs',
    }
    return aliases.get(csp, csp)


def restreindre_solidaire_justificatif(proportions, csp):
    """
    Réserve le tarif solidaire aux publics avec justificatif.

    Étudiants, demandeurs d'emploi, minimas sociaux et allocataires AAH
    sont modélisés par la catégorie Étudiants/Chômeurs. Les autres classes
    conservent la part relative entre tarif normal et soutien.
    """
    proportions = dict(proportions)
    if normaliser_csp(csp) in CSP_ELIGIBLES_JUSTIFICATIF:
        return proportions

    normale = float(proportions.get('normale', 0))
    soutien = float(proportions.get('soutien', 0))
    reste = normale + soutien
    if reste <= 0:
        normale_part, soutien_part = 1.0, 0.0
    else:
        normale_part = normale / reste
        soutien_part = soutien / reste

    proportions['solidaire'] = 0.0
    proportions['normale'] = normale_part
    proportions['soutien'] = soutien_part
    return proportions


def repartir_parts_sans_solidaire(normale, soutien):
    """Ramène normal et soutien à 100 % en gardant leur part relative."""
    normale = int(normale)
    soutien = int(soutien)
    reste = normale + soutien
    if reste <= 0:
        return 100, 0
    normale_new = int(round(normale / reste * 100))
    normale_new = min(100, max(0, normale_new))
    return normale_new, 100 - normale_new


def profil_eligible_justificatif(config):
    return normaliser_csp(config.get('csp')) in CSP_ELIGIBLES_JUSTIFICATIF


def calculer_repartition_cotisations(
    df_result,
    cotisation_solidaire,
    cotisation_normale,
    cotisation_soutien,
    proportions_par_profil,
    mode_justificatif=False,
):
    """
    Calcule la répartition des cotisations par type pour chaque profil.
    
    Args:
        df_result: DataFrame avec les profils
        cotisation_solidaire: Tarif solidaire
        cotisation_normale: Tarif normal
        cotisation_soutien: Tarif soutien
        proportions_par_profil: Dictionnaire avec les proportions par profil
    
    Returns:
        DataFrame avec colonnes nb_solidaire, nb_normale, nb_soutien, cotisation_moyenne
    """
    df_result = df_result.copy()
    
    def trouver_profil(age_group, csp):
        """Trouve le profil correspondant dans proportions_par_profil."""
        # En mode justificatif, les publics éligibles suivent toujours
        # la grille Étudiants/Chômeurs, pas le profil d'âge plus large.
        if mode_justificatif and normaliser_csp(csp) in CSP_ELIGIBLES_JUSTIFICATIF:
            for config in proportions_par_profil.values():
                if profil_eligible_justificatif(config):
                    return config

        # Chercher d'abord les correspondances exactes (âge ET CSP)
        for nom_profil, config in proportions_par_profil.items():
            if nom_profil == 'Autres profils':
                continue
            age_match = config['age_group'] is None or config['age_group'] == age_group
            csp_match = config['csp'] is None or normaliser_csp(config['csp']) == normaliser_csp(csp)
            
            # Si les deux correspondent, utiliser ce profil
            if age_match and csp_match:
                # Préférer les profils où les deux sont spécifiés
                if config['age_group'] is not None and config['csp'] is not None:
                    return config
        
        # Ensuite chercher les correspondances partielles (âge OU CSP)
        for nom_profil, config in proportions_par_profil.items():
            if nom_profil == 'Autres profils':
                continue
            age_match = config['age_group'] is None or config['age_group'] == age_group
            csp_match = config['csp'] is None or normaliser_csp(config['csp']) == normaliser_csp(csp)
            
            if age_match and csp_match:
                return config
        
        # Si aucun match, utiliser "Autres profils"
        return proportions_par_profil.get('Autres profils', {
            'solidaire': 0.1,
            'normale': 0.8,
            'soutien': 0.1
        })
    
    for idx, row in df_result.iterrows():
        age_group = row['age_group']
        csp = row['csp']
        nb_adherents = row['nb_adherents']
        
        # Trouver les proportions pour ce profil
        proportions = trouver_profil(age_group, csp)
        if mode_justificatif:
            proportions = restreindre_solidaire_justificatif(proportions, csp)
        
        # Calculer la répartition
        nb_solidaire = int(nb_adherents * proportions['solidaire'])
        nb_normale = int(nb_adherents * proportions['normale'])
        nb_soutien = nb_adherents - nb_solidaire - nb_normale  # Pour s'assurer que le total est correct
        
        # Calculer la cotisation moyenne pour ce profil
        cotisation_moyenne = (
            nb_solidaire * cotisation_solidaire +
            nb_normale * cotisation_normale +
            nb_soutien * cotisation_soutien
        ) / nb_adherents if nb_adherents > 0 else cotisation_normale
        
        df_result.at[idx, 'nb_solidaire'] = nb_solidaire
        df_result.at[idx, 'nb_normale'] = nb_normale
        df_result.at[idx, 'nb_soutien'] = nb_soutien
        df_result.at[idx, 'cotisation_moyenne'] = cotisation_moyenne
    
    return df_result

# Fonction principale
def main():
    # Charger les données
    with st.spinner("Chargement des données..."):
        df, margins, df_behaviors = load_cached_data()
    
    population_totale = int(margins['population'].sum())
    # Calculer le nombre d'intéressés à partir du pourcentage moyen d'intérêt
    pct_interet_moyen = df_behaviors['pct_interet'].mean()
    nb_interesses_total = int(population_totale * pct_interet_moyen / 100)

    st.markdown(
        render_hero(population_totale, nb_interesses_total, format_nombre),
        unsafe_allow_html=True,
    )
    
    # Sidebar - Paramètres
    st.sidebar.markdown(
        """
        <div class="sidebar-brand">
          <p class="title">Paramètres</p>
          <p class="desc">Ajustez le scénario d'adhésion et la grille tarifaire.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    st.sidebar.markdown("##### Objectif d'adhérents")
    
    # Curseur principal : Nombre d'adhérents
    nb_adherents = st.sidebar.slider(
        "Nombre d'adhérents cible",
        min_value=10,
        max_value=500,
        value=80,
        step=10,
        help="Ajustez le nombre d'adhérents souhaité"
    )
    
    # Pourcentage par rapport aux intéressés
    pct_conversion = (nb_adherents / nb_interesses_total) * 100
    st.sidebar.metric(
        "Taux de conversion",
        f"{pct_conversion:.1f}%",
        help="% d'intéressés qui deviennent adhérents"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### Grille tarifaire")
    
    # Tarifs de cotisation par type
    st.sidebar.markdown("**Cotisation annuelle (€)**")
    cotisation_solidaire = st.sidebar.number_input(
        "Tarif Solidaire",
        min_value=0,
        max_value=50,
        value=5,
        step=1,
        help="Pour étudiants, chômeurs, petits budgets"
    )
    
    cotisation_normale = st.sidebar.number_input(
        "Tarif Normal",
        min_value=0,
        max_value=100,
        value=10,
        step=1,
        help="Tarif standard pour la plupart des adhérents"
    )
    
    cotisation_soutien = st.sidebar.number_input(
        "Tarif Soutien",
        min_value=0,
        max_value=200,
        value=20,
        step=1,
        help="Pour ceux qui souhaitent soutenir davantage le projet"
    )
    
    st.sidebar.markdown("**Prix de location (€/jour)**")
    prix_location = st.sidebar.number_input(
        "Prix moyen location",
        min_value=0.0,
        max_value=20.0,
        value=3.0,
        step=0.5,
        help="Prix moyen de location d'un objet par jour"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### Fréquence d'usage")
    
    # Nombre moyen de locations par adhérent par an
    nb_locations_moyen = st.sidebar.number_input(
        "Nombre moyen de locations par adhérent/an",
        min_value=1,
        max_value=50,
        value=2,
        step=1,
        help="Nombre moyen de locations par adhérent et par an"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### Charges de fonctionnement")
    depense_mensuelle = st.sidebar.number_input(
        "Dépense moyenne mensuelle (€)",
        min_value=0.0,
        max_value=50000.0,
        value=150.0,
        step=10.0,
        help="Charges moyennes de la structure chaque mois (local, assurance, fonctionnement). "
             "Les recettes du scénario sont comparées à cette dépense. Valeur de départ : 150 €."
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### Règle du tarif solidaire")
    mode_justificatif = st.sidebar.checkbox(
        "Tarif réduit uniquement sur justificatif",
        value=False,
        help="Réserve le tarif solidaire aux étudiant·es, minimas sociaux, "
             "demandeur·euses d'emploi et allocataires adultes handicapés."
    )
    if mode_justificatif:
        st.sidebar.caption(
            "Le tarif solidaire est réservé aux étudiant·es, minimas sociaux, "
            "demandeur·euses d'emploi et allocataires AAH (catégorie Étudiants/Chômeurs). "
            "Les autres catégories ne peuvent pas le choisir : seuls les tarifs normal et soutien restent réglables."
        )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("##### Répartition des tarifs par profil")
    
    st.sidebar.markdown("""
    Ajustez les proportions de chaque tarif selon les profils.
    Les valeurs doivent totaliser **100 %** pour chaque profil.
    """)
    
    # Définir les profils disponibles
    profils_disponibles = {
        'Jeunes (18-24)': {
            'age_group': '18-24',
            'csp': None,
            'default_solidaire': 80,
            'default_normale': 20,
            'default_soutien': 0
        },
        'Étudiants/Chômeurs': {
            'age_group': None,
            'csp': 'Etudiants/Chomeurs',
            'default_solidaire': 80,
            'default_normale': 20,
            'default_soutien': 0
        },
        'Actifs Jeunes (25-34)': {
            'age_group': '25-34',
            'csp': 'Actifs',
            'default_solidaire': 10,
            'default_normale': 80,
            'default_soutien': 10
        },
        'Actifs Adultes (35-44)': {
            'age_group': '35-44',
            'csp': 'Actifs',
            'default_solidaire': 10,
            'default_normale': 80,
            'default_soutien': 10
        },
        'Actifs Seniors (45-54)': {
            'age_group': '45-54',
            'csp': 'Actifs',
            'default_solidaire': 5,
            'default_normale': 55,
            'default_soutien': 40
        },
        'Actifs Seniors (55-64)': {
            'age_group': '55-64',
            'csp': 'Actifs',
            'default_solidaire': 5,
            'default_normale': 55,
            'default_soutien': 40
        },
        'Retraités (55-64)': {
            'age_group': '55-64',
            'csp': 'Retraites/Inactifs',
            'default_solidaire': 10,
            'default_normale': 60,
            'default_soutien': 30
        },
        'Retraités (65+)': {
            'age_group': '65+',
            'csp': 'Retraites/Inactifs',
            'default_solidaire': 10,
            'default_normale': 60,
            'default_soutien': 30
        },
        'Retraités (autres)': {
            'age_group': None,
            'csp': 'Retraites/Inactifs',
            'default_solidaire': 10,
            'default_normale': 60,
            'default_soutien': 30
        },
        'Autres profils': {
            'age_group': None,
            'csp': None,
            'default_solidaire': 10,
            'default_normale': 80,
            'default_soutien': 10
        }
    }
    
    # Stocker les proportions dans un dictionnaire
    proportions_par_profil = {}

    if mode_justificatif and not st.session_state.get("_justificatif_sliders_verrouilles"):
        for nom_profil, config in profils_disponibles.items():
            if profil_eligible_justificatif(config):
                continue
            normale = st.session_state.get(f"normale_{nom_profil}", config['default_normale'])
            soutien = st.session_state.get(f"soutien_{nom_profil}", config['default_soutien'])
            normale_new, soutien_new = repartir_parts_sans_solidaire(normale, soutien)
            st.session_state[f"solidaire_{nom_profil}"] = 0
            st.session_state[f"normale_{nom_profil}"] = normale_new
            st.session_state[f"soutien_{nom_profil}"] = soutien_new
        st.session_state["_justificatif_sliders_verrouilles"] = True
    elif not mode_justificatif and st.session_state.get("_justificatif_sliders_verrouilles"):
        for nom_profil, config in profils_disponibles.items():
            if profil_eligible_justificatif(config):
                continue
            st.session_state[f"solidaire_{nom_profil}"] = config['default_solidaire']
        st.session_state["_justificatif_sliders_verrouilles"] = False
    
    for nom_profil, config in profils_disponibles.items():
        eligible = profil_eligible_justificatif(config)
        solidaire_verrouille = mode_justificatif and not eligible
        with st.sidebar.expander(f"📋 {nom_profil}", expanded=False):
            if solidaire_verrouille:
                st.caption("Tarif solidaire indisponible pour cette catégorie.")
            solidaire = st.slider(
                f"Solidaire (%)",
                min_value=0,
                max_value=100,
                value=0 if solidaire_verrouille else config['default_solidaire'],
                step=5,
                key=f"solidaire_{nom_profil}",
                disabled=solidaire_verrouille,
            )
            if solidaire_verrouille:
                solidaire = 0
            
            normale = st.slider(
                f"Normal (%)",
                min_value=0,
                max_value=100,
                value=config['default_normale'],
                step=5,
                key=f"normale_{nom_profil}"
            )
            
            soutien = st.slider(
                f"Soutien (%)",
                min_value=0,
                max_value=100,
                value=config['default_soutien'],
                step=5,
                key=f"soutien_{nom_profil}"
            )
            
            total = solidaire + normale + soutien
            if total != 100:
                st.warning(f"⚠️ Total = {total}% (doit être 100%)")
            
            # Normaliser si nécessaire
            if total > 0:
                solidaire_norm = solidaire / total * 100
                normale_norm = normale / total * 100
                soutien_norm = soutien / total * 100
            else:
                solidaire_norm = 0
                normale_norm = 0
                soutien_norm = 0
            
            proportions_par_profil[nom_profil] = {
                'age_group': config['age_group'],
                'csp': config['csp'],
                'solidaire': solidaire_norm / 100,
                'normale': normale_norm / 100,
                'soutien': soutien_norm / 100
            }
    
    st.sidebar.markdown("---")
    
    # Bouton de réinitialisation
    if st.sidebar.button("Réinitialiser", use_container_width=True):
        st.rerun()
    
    # Calcul de la simulation
    with st.spinner("Calcul en cours..."):
        # Distribution des adhérents
        df_dist = distribute_adherents_by_profile(nb_adherents, df_behaviors, margins)
        
        # Calcul des recettes de base
        df_result = calculate_recettes_by_profile(df_dist)
        
        # Calculer la répartition des cotisations par type
        df_result = calculer_repartition_cotisations(
            df_result,
            cotisation_solidaire,
            cotisation_normale,
            cotisation_soutien,
            proportions_par_profil,
            mode_justificatif=mode_justificatif,
        )
        
        # Appliquer le nombre moyen de locations par adhérent (uniforme pour tous)
        df_result['nb_locations_an'] = nb_locations_moyen
        
        # Recalculer les recettes avec les nouveaux tarifs
        df_result['recettes_cotisations'] = df_result['nb_adherents'] * df_result['cotisation_moyenne']
        df_result['recettes_locations'] = (
            df_result['nb_adherents'] * 
            nb_locations_moyen * 
            prix_location
        )
        df_result['recettes_totales'] = df_result['recettes_cotisations'] + df_result['recettes_locations']
    
    # Métriques principales
    st.markdown(
        render_section(
            "Résultats de la simulation",
            "Indicateurs clés calculés à partir de votre scénario.",
        ),
        unsafe_allow_html=True,
    )
    
    total_adherents = df_result['nb_adherents'].sum()
    total_cotisations = df_result['recettes_cotisations'].sum()
    total_locations = df_result['recettes_locations'].sum()
    total_recettes = df_result['recettes_totales'].sum()
    recette_par_adherent = total_recettes / total_adherents if total_adherents > 0 else 0

    st.markdown(
        render_kpi_grid([
            {
                "label": "Adhérents",
                "value": format_nombre(total_adherents),
                "delta": f"{format_nombre(pct_conversion, 1)} % des intéressés",
                "accent": COLORS["primary"],
            },
            {
                "label": "Cotisations",
                "value": f"{format_nombre(total_cotisations)} €",
                "delta": f"{format_nombre(total_cotisations/total_adherents)} € / adhérent",
                "accent": COLORS["sage"],
            },
            {
                "label": "Locations",
                "value": f"{format_nombre(total_locations)} €",
                "delta": f"{nb_locations_moyen} loc. / an / adhérent",
                "accent": COLORS["male"],
            },
            {
                "label": "Recettes totales",
                "value": f"{format_nombre(total_recettes)} €",
                "delta": f"{format_nombre(recette_par_adherent)} € / adhérent",
                "accent": COLORS["accent"],
            },
        ]),
        unsafe_allow_html=True,
    )

    equilibre = evaluer_equilibre(
        total_recettes,
        total_cotisations,
        total_locations,
        total_adherents,
        depense_mensuelle,
        nb_locations_moyen,
    )

    st.markdown('<hr class="bob-divider"/>', unsafe_allow_html=True)
    st.markdown(
        render_section(
            "Recettes face aux charges",
            "La dépense moyenne mensuelle se règle dans la barre latérale (150 € par défaut).",
        ),
        unsafe_allow_html=True,
    )

    if equilibre["equilibre"]:
        titre_eq = f"Excédent de {format_nombre(equilibre['resultat_mensuel'])} € par mois"
        message_eq = (
            f"Les recettes mensuelles ({format_nombre(equilibre['recettes_mensuelles'])} €) "
            f"couvrent la dépense de {format_nombre(equilibre['depense_mensuelle'])} €. "
            f"Sur l'année, l'excédent est de {format_nombre(equilibre['resultat_annuel'])} €. "
            f"Les charges peuvent encore monter de {format_nombre(equilibre['resultat_mensuel'])} € / mois "
            f"avant le point mort."
        )
        ton_eq = "ok"
        accent_resultat = COLORS["success"]
    else:
        titre_eq = f"Déficit de {format_nombre(abs(equilibre['resultat_mensuel']))} € par mois"
        message_eq = (
            f"Les recettes mensuelles ({format_nombre(equilibre['recettes_mensuelles'])} €) "
            f"ne couvrent pas la dépense de {format_nombre(equilibre['depense_mensuelle'])} €. "
            f"Il manque {format_nombre(equilibre['besoin_annuel'])} € sur l'année."
        )
        ton_eq = "alert"
        accent_resultat = COLORS["danger"]

    st.markdown(render_status_banner(ton_eq, titre_eq, message_eq), unsafe_allow_html=True)

    couverture_label = (
        f"{format_nombre(equilibre['taux_couverture'], 1)} %"
        if equilibre["taux_couverture"] is not None
        else "—"
    )
    st.markdown(
        render_kpi_grid([
            {
                "label": "Recettes / mois",
                "value": f"{format_nombre(equilibre['recettes_mensuelles'])} €",
                "delta": f"{format_nombre(total_recettes)} € sur l'année",
                "accent": COLORS["primary"],
            },
            {
                "label": "Dépense / mois",
                "value": f"{format_nombre(equilibre['depense_mensuelle'])} €",
                "delta": f"{format_nombre(equilibre['depenses_annuelles'])} € de charges / an",
                "accent": COLORS["accent"],
            },
            {
                "label": "Résultat / mois",
                "value": f"{format_nombre(equilibre['resultat_mensuel'])} €",
                "delta": f"{format_nombre(equilibre['resultat_annuel'])} € sur l'année",
                "accent": accent_resultat,
            },
            {
                "label": "Couverture des charges",
                "value": couverture_label,
                "delta": "100 % = point mort",
                "accent": COLORS["sage"],
            },
        ]),
        unsafe_allow_html=True,
    )

    col_eq1, col_eq2 = st.columns([1.15, 0.85])
    with col_eq1:
        fig_eq = go.Figure()
        fig_eq.add_trace(go.Bar(
            name="Cotisations",
            x=["Recettes mensuelles", "Dépense mensuelle"],
            y=[total_cotisations / 12, 0],
            marker_color=COLORS["cotisations"],
        ))
        fig_eq.add_trace(go.Bar(
            name="Locations",
            x=["Recettes mensuelles", "Dépense mensuelle"],
            y=[total_locations / 12, 0],
            marker_color=COLORS["locations"],
        ))
        fig_eq.add_trace(go.Bar(
            name="Charges",
            x=["Recettes mensuelles", "Dépense mensuelle"],
            y=[0, depense_mensuelle],
            marker_color=COLORS["accent"],
        ))
        apply_plotly_theme(
            fig_eq,
            title="Recettes mensuelles et dépense moyenne",
            height=380,
            barmode="stack",
            yaxis_title="Euros / mois",
        )
        st.plotly_chart(fig_eq, use_container_width=True)

    with col_eq2:
        seuil_txt = (
            format_nombre(equilibre["seuil_adherents"])
            if equilibre["seuil_adherents"] is not None
            else "—"
        )
        if equilibre["ecart_adherents"] is None:
            ecart_txt = "La recette par adhérent est nulle : le seuil ne peut pas être calculé."
        elif equilibre["ecart_adherents"] >= 0:
            ecart_txt = (
                f"{format_nombre(equilibre['ecart_adherents'])} adhérents au-dessus du seuil."
            )
        else:
            ecart_txt = (
                f"{format_nombre(abs(equilibre['ecart_adherents']))} adhérents manquent pour couvrir les charges."
            )

        cotis_couv = equilibre["couverture_cotisations"]
        loc_couv = equilibre["couverture_locations"]
        lecture = [
            f"**Seuil de rentabilité** : {seuil_txt} adhérents, à recette constante "
            f"({format_nombre(equilibre['recette_par_adherent'])} € / adhérent / an).",
            ecart_txt,
            f"**Coût des charges** : {format_nombre(equilibre['cout_par_adherent'])} € / adhérent / an, "
            f"contre {format_nombre(equilibre['recette_par_adherent'])} € de recette.",
        ]
        if cotis_couv is not None:
            lecture.append(
                f"Les cotisations couvrent **{format_nombre(cotis_couv, 1)} %** des charges, "
                f"les locations **{format_nombre(loc_couv, 1)} %**."
            )
        if not equilibre["equilibre"]:
            if equilibre["hausse_cotisation"] is not None:
                lecture.append(
                    f"Pour revenir à l'équilibre sans changer le nombre d'adhérents : "
                    f"+{format_nombre(equilibre['hausse_cotisation'], 2)} € de cotisation moyenne / an, "
                    f"ou +{format_nombre(equilibre['hausse_prix_location'], 2)} € sur le prix de location."
                )
        else:
            lecture.append(
                "Le scénario finance le fonctionnement. Le levier utile est d'éprouver "
                "une dépense mensuelle plus haute, ou un nombre d'adhérents plus bas."
            )
        st.markdown("##### Lecture opérationnelle")
        for ligne in lecture:
            st.markdown(f"- {ligne}")

    st.markdown("##### Sensibilité aux charges")
    st.caption(
        "Même scénario d'adhérents et de tarifs, avec plusieurs niveaux de dépense mensuelle. "
        "La ligne « Actuel » correspond au montant saisi dans la barre latérale."
    )
    df_sens = tableau_sensibilite_charges(
        total_recettes,
        total_cotisations,
        total_locations,
        total_adherents,
        nb_locations_moyen,
        depense_mensuelle,
    )
    st.dataframe(df_sens, use_container_width=True, hide_index=True)
    
    # Répartition des cotisations
    st.markdown('<hr class="bob-divider"/>', unsafe_allow_html=True)
    
    # Calculer les totaux pour la répartition
    nb_solidaire_total = int(df_result['nb_solidaire'].sum())
    nb_normale_total = int(df_result['nb_normale'].sum())
    nb_soutien_total = int(df_result['nb_soutien'].sum())
    
    # Bouton d'export PDF
    col_export1, col_export2, col_export3 = st.columns([1, 2, 1])
    with col_export2:
        if REPORTLAB_AVAILABLE:
            if st.button("Exporter le scénario en PDF", use_container_width=True, type="primary"):
                with st.spinner("Génération du rapport PDF en cours..."):
                    try:
                        # Créer le répertoire de sortie temporaire pour les graphiques
                        temp_dir = BASE_DIR / "outputs" / "temp_export"
                        temp_dir.mkdir(parents=True, exist_ok=True)
                        
                        # Calculer les métriques supplémentaires
                        cotisation_moyenne = total_cotisations / total_adherents if total_adherents > 0 else 0
                        pct_solidaire = (nb_solidaire_total / total_adherents * 100) if total_adherents > 0 else 0
                        pct_normale = (nb_normale_total / total_adherents * 100) if total_adherents > 0 else 0
                        pct_soutien = (nb_soutien_total / total_adherents * 100) if total_adherents > 0 else 0
                        
                        # Préparer les données du scénario
                        scenario_data = {
                            'nb_adherents': nb_adherents,
                            'cotisation_solidaire': cotisation_solidaire,
                            'cotisation_normale': cotisation_normale,
                            'cotisation_soutien': cotisation_soutien,
                            'prix_location': prix_location,
                            'nb_locations_moyen': nb_locations_moyen,
                            'mode_justificatif': mode_justificatif,
                            'proportions_par_profil': proportions_par_profil,
                            'total_adherents': total_adherents,
                            'total_cotisations': total_cotisations,
                            'total_locations': total_locations,
                            'total_recettes': total_recettes,
                            'recette_par_adherent': recette_par_adherent,
                            'cotisation_moyenne': cotisation_moyenne,
                            'depense_mensuelle': depense_mensuelle,
                            'depenses_annuelles': equilibre['depenses_annuelles'],
                            'recettes_mensuelles': equilibre['recettes_mensuelles'],
                            'resultat_mensuel': equilibre['resultat_mensuel'],
                            'resultat_annuel': equilibre['resultat_annuel'],
                            'taux_couverture': equilibre['taux_couverture'],
                            'seuil_adherents': equilibre['seuil_adherents'],
                            'pct_solidaire': pct_solidaire,
                            'pct_normale': pct_normale,
                            'pct_soutien': pct_soutien,
                            'df_result': df_result,
                            'graphiques_paths': []
                        }
                        
                        # Générer et exporter les graphiques principaux
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        
                        # Graphique 1: Répartition des recettes
                        try:
                            fig_recettes = go.Figure(data=[go.Pie(
                                labels=['Cotisations', 'Locations'],
                                values=[total_cotisations, total_locations],
                                hole=0.45,
                                marker=dict(colors=[COLORS['cotisations'], COLORS['locations']])
                            )])
                            apply_plotly_theme(fig_recettes, title="Répartition des Recettes", height=400)
                            path_recettes = temp_dir / f"repartition_recettes_{timestamp}.png"
                            if export_plotly_figure(fig_recettes, path_recettes):
                                scenario_data['graphiques_paths'].append(("Répartition des Recettes", str(path_recettes)))
                        except Exception as e:
                            st.warning(f"⚠️ Impossible d'exporter le graphique 'Répartition des Recettes' : {e}")
                        
                        # Graphique 2: Distribution par âge
                        try:
                            age_dist = df_result.groupby('age_group')['nb_adherents'].sum().sort_values(ascending=True)
                            fig_age = px.bar(
                                x=age_dist.values,
                                y=age_dist.index,
                                orientation='h',
                                title="Distribution par Âge",
                                labels={'x': 'Nombre d\'adhérents', 'y': 'Tranche d\'âge'},
                                color=age_dist.values,
                                color_continuous_scale=SCALE_TEAL
                            )
                            apply_plotly_theme(fig_age, title="Distribution par Âge", height=400, showlegend=False)
                            path_age = temp_dir / f"distribution_age_{timestamp}.png"
                            if export_plotly_figure(fig_age, path_age):
                                scenario_data['graphiques_paths'].append(("Distribution par Âge", str(path_age)))
                        except Exception as e:
                            st.warning(f"⚠️ Impossible d'exporter le graphique 'Distribution par Âge' : {e}")
                        
                        # Graphique 3: Répartition des cotisations
                        try:
                            cotisation_data = pd.DataFrame({
                                'Type': ['Solidaire', 'Normal', 'Soutien'],
                                'Nombre': [nb_solidaire_total, nb_normale_total, nb_soutien_total],
                                'Tarif': [f'{cotisation_solidaire}€', f'{cotisation_normale}€', f'{cotisation_soutien}€']
                            })
                            fig_cotis = go.Figure(data=[go.Pie(
                                labels=[f"{row['Type']}<br>{row['Tarif']}" for _, row in cotisation_data.iterrows()],
                                values=cotisation_data['Nombre'],
                                hole=0.4,
                                marker=dict(colors=[COLORS['solidaire'], COLORS['normale'], COLORS['soutien']])
                            )])
                            apply_plotly_theme(fig_cotis, title="Répartition des Cotisations", height=400)
                            path_cotis = temp_dir / f"repartition_cotisations_{timestamp}.png"
                            if export_plotly_figure(fig_cotis, path_cotis):
                                scenario_data['graphiques_paths'].append(("Répartition des Cotisations", str(path_cotis)))
                        except Exception as e:
                            st.warning(f"⚠️ Impossible d'exporter le graphique 'Répartition des Cotisations' : {e}")
                        
                        # Générer le PDF
                        pdf_path = BASE_DIR / "outputs" / "reports" / f"scenario_bob_{timestamp}.pdf"
                        pdf_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        generate_scenario_pdf(scenario_data, pdf_path)
                        
                        # Afficher le succès et le bouton de téléchargement
                        st.success(f"✅ Rapport PDF généré avec succès !")
                        
                        # Bouton de téléchargement
                        with open(pdf_path, 'rb') as pdf_file:
                            pdf_bytes = pdf_file.read()
                            st.download_button(
                                label="Télécharger le PDF",
                                data=pdf_bytes,
                                file_name=f"scenario_bob_{timestamp}.pdf",
                                mime='application/pdf',
                                use_container_width=True
                            )
                        
                        st.info(f"📁 Fichier sauvegardé : {pdf_path}")
                        
                    except Exception as e:
                        st.error(f"Erreur lors de la génération du PDF : {e}")
                        import traceback
                        st.code(traceback.format_exc(), language='python')
        else:
            st.info("💡 Pour activer l'export PDF, installez ReportLab : `pip install reportlab kaleido`")
    
    st.markdown('<hr class="bob-divider"/>', unsafe_allow_html=True)
    st.markdown(
        render_section(
            "Répartition des cotisations",
            "Tarif réduit réservé aux publics avec justificatif (étudiant·es, minimas sociaux, demandeur·euses d'emploi, AAH). Les autres classes conservent la part normal / soutien."
            if mode_justificatif
            else "Structure tarifaire du scénario sélectionné.",
        ),
        unsafe_allow_html=True,
    )
    if mode_justificatif:
        st.markdown(
            render_status_banner(
                "ok",
                "Mode justificatif actif",
                "Le tarif solidaire est limité à la catégorie Étudiants/Chômeurs. "
                "Les autres catégories ne peuvent pas le choisir : elles restent sur "
                "les tarifs normal et soutien, selon les hypothèses de base.",
            ),
            unsafe_allow_html=True,
        )

    st.markdown(
        render_tariff_grid([
            {
                "label": f"Tarif solidaire · {cotisation_solidaire} €",
                "value": format_nombre(nb_solidaire_total),
                "delta": f"{format_nombre(nb_solidaire_total/total_adherents*100, 1)} % des adhérents",
                "accent": COLORS["solidaire"],
            },
            {
                "label": f"Tarif normal · {cotisation_normale} €",
                "value": format_nombre(nb_normale_total),
                "delta": f"{format_nombre(nb_normale_total/total_adherents*100, 1)} % des adhérents",
                "accent": COLORS["normale"],
            },
            {
                "label": f"Tarif soutien · {cotisation_soutien} €",
                "value": format_nombre(nb_soutien_total),
                "delta": f"{format_nombre(nb_soutien_total/total_adherents*100, 1)} % des adhérents",
                "accent": COLORS["soutien"],
            },
        ]),
        unsafe_allow_html=True,
    )
    
    # Graphiques
    st.markdown('<hr class="bob-divider"/>', unsafe_allow_html=True)
    
    # Onglets
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Vue d'ensemble", 
        "Profils", 
        "Recettes", 
        "Détails",
        "Résultats enquête"
    ])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Répartition des recettes
            fig_recettes = go.Figure(data=[go.Pie(
                labels=['Cotisations', 'Locations'],
                values=[total_cotisations, total_locations],
                hole=0.45,
                marker=dict(colors=[COLORS['cotisations'], COLORS['locations']]),
                textinfo='label+percent',
            )])
            apply_plotly_theme(fig_recettes, title="Répartition des recettes", height=400)
            st.plotly_chart(fig_recettes, use_container_width=True)
        
        with col2:
            # Distribution par âge
            age_dist = df_result.groupby('age_group')['nb_adherents'].sum().sort_values(ascending=True)
            fig_age = px.bar(
                x=age_dist.values,
                y=age_dist.index,
                orientation='h',
                title="Distribution par âge",
                labels={'x': 'Nombre d\'adhérents', 'y': 'Tranche d\'âge'},
                color=age_dist.values,
                color_continuous_scale=SCALE_TEAL
            )
            apply_plotly_theme(fig_age, title="Distribution par âge", height=400, showlegend=False)
            st.plotly_chart(fig_age, use_container_width=True)
        
        # Distribution par sexe et CSP
        col3, col4 = st.columns(2)
        
        with col3:
            sexe_dist = df_result.groupby('sexe')['nb_adherents'].sum()
            sexe_labels = ['Femmes' if x == 'F' else 'Hommes' for x in sexe_dist.index]
            fig_sexe = go.Figure(data=[go.Pie(
                labels=sexe_labels,
                values=sexe_dist.values,
                hole=0.4,
                marker=dict(colors=[COLORS['female'], COLORS['male']]),
                textinfo='label+percent',
            )])
            apply_plotly_theme(fig_sexe, title="Distribution par sexe", height=400)
            st.plotly_chart(fig_sexe, use_container_width=True)
        
        with col4:
            # Répartition des cotisations
            cotisation_data = pd.DataFrame({
                'Type': ['Solidaire', 'Normal', 'Soutien'],
                'Nombre': [nb_solidaire_total, nb_normale_total, nb_soutien_total],
                'Tarif': [f'{cotisation_solidaire}€', f'{cotisation_normale}€', f'{cotisation_soutien}€']
            })
            fig_cotis = go.Figure(data=[go.Pie(
                labels=[f"{row['Type']}<br>{row['Tarif']}" for _, row in cotisation_data.iterrows()],
                values=cotisation_data['Nombre'],
                hole=0.4,
                marker=dict(colors=[COLORS['solidaire'], COLORS['normale'], COLORS['soutien']]),
                textinfo='label+percent',
            )])
            apply_plotly_theme(fig_cotis, title="Répartition des cotisations", height=400)
            st.plotly_chart(fig_cotis, use_container_width=True)
        
        # Distribution par CSP
        st.markdown(
            render_section("Distribution par CSP", "Répartition des adhérents selon la situation professionnelle."),
            unsafe_allow_html=True,
        )
        col5, col6 = st.columns([2, 1])
        
        with col5:
            csp_dist = df_result.groupby('csp')['nb_adherents'].sum().sort_values(ascending=True)
            fig_csp = px.bar(
                x=csp_dist.values,
                y=csp_dist.index,
                orientation='h',
                title="Distribution par CSP",
                labels={'x': 'Nombre d\'adhérents', 'y': 'Situation professionnelle'},
                color=csp_dist.values,
                color_continuous_scale=SCALE_TEAL
            )
            apply_plotly_theme(fig_csp, title="Distribution par CSP", height=400, showlegend=False)
            st.plotly_chart(fig_csp, use_container_width=True)
    
    with tab2:
        st.markdown(
            render_section("Top 10 profils contributeurs", "Classement des segments qui génèrent le plus de recettes."),
            unsafe_allow_html=True,
        )
        
        top10 = df_result.nlargest(10, 'recettes_totales')[
            ['profil', 'nb_adherents', 'recettes_cotisations', 'recettes_locations', 'recettes_totales']
        ].copy()
        
        top10.columns = ['Profil', 'Adhérents', 'Cotisations (€)', 'Locations (€)', 'Total (€)']
        top10['Cotisations (€)'] = top10['Cotisations (€)'].round(0).astype(int)
        top10['Locations (€)'] = top10['Locations (€)'].round(0).astype(int)
        top10['Total (€)'] = top10['Total (€)'].round(0).astype(int)
        
        st.dataframe(top10, use_container_width=True, hide_index=True)
        
        # Graphique des top profils
        fig_top = px.bar(
            top10,
            x='Total (€)',
            y='Profil',
            orientation='h',
            title="Recettes par profil (Top 10)",
            color='Total (€)',
            color_continuous_scale=SCALE_TEAL
        )
        apply_plotly_theme(fig_top, title="Recettes par profil (Top 10)", height=500, showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with tab3:
        st.markdown(
            render_section("Analyse des recettes", "Lecture croisée des revenus par âge, CSP et sexe."),
            unsafe_allow_html=True,
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Recettes par âge
            recettes_age = df_result.groupby('age_group')['recettes_totales'].sum().sort_values(ascending=False)
            fig_rec_age = px.bar(
                x=recettes_age.index,
                y=recettes_age.values,
                title="Recettes par tranche d'âge",
                labels={'x': 'Âge', 'y': 'Recettes (€)'},
                color=recettes_age.values,
                color_continuous_scale=SCALE_TEAL
            )
            apply_plotly_theme(fig_rec_age, title="Recettes par tranche d'âge", showlegend=False)
            st.plotly_chart(fig_rec_age, use_container_width=True)
        
        with col2:
            # Recettes par CSP
            recettes_csp = df_result.groupby('csp')['recettes_totales'].sum().sort_values(ascending=False)
            fig_rec_csp = px.bar(
                x=recettes_csp.index,
                y=recettes_csp.values,
                title="Recettes par CSP",
                labels={'x': 'CSP', 'y': 'Recettes (€)'},
                color=recettes_csp.values,
                color_continuous_scale=SCALE_TEAL
            )
            apply_plotly_theme(fig_rec_csp, title="Recettes par CSP", showlegend=False)
            st.plotly_chart(fig_rec_csp, use_container_width=True)
        
        # Heatmap recettes par âge et sexe
        pivot_recettes = df_result.pivot_table(
            values='recettes_totales',
            index='age_group',
            columns='sexe',
            aggfunc='sum'
        )
        pivot_recettes.columns = ['Femmes', 'Hommes']
        
        fig_heatmap = px.imshow(
            pivot_recettes,
            title="Heatmap des recettes (âge × sexe)",
            labels=dict(x="Sexe", y="Âge", color="Recettes (€)"),
            color_continuous_scale=SCALE_TEAL,
            aspect='auto'
        )
        apply_plotly_theme(fig_heatmap, title="Heatmap des recettes (âge × sexe)", height=460)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab4:
        st.markdown(
            render_section("Tableau détaillé par profil", "Exportable pour analyse fine et reporting."),
            unsafe_allow_html=True,
        )
        
        # Préparer le tableau
        df_export = df_result[[
            'profil', 'age_group', 'sexe', 'csp',
            'population', 'pct_interet', 'nb_adherents',
            'nb_solidaire', 'nb_normale', 'nb_soutien', 'cotisation_moyenne',
            'nb_locations_an',
            'recettes_cotisations', 'recettes_locations', 'recettes_totales'
        ]].copy()
        
        df_export.columns = [
            'Profil', 'Âge', 'Sexe', 'CSP',
            'Population', 'Intérêt (%)', 'Adhérents',
            'Nb Solidaire', 'Nb Normal', 'Nb Soutien', 'Cotis. Moy. (€)',
            'Locations/an',
            'Rec. Cotisations (€)', 'Rec. Locations (€)', 'Rec. Totales (€)'
        ]
        
        # Arrondir
        for col in ['Cotis. Moy. (€)', 'Rec. Cotisations (€)', 'Rec. Locations (€)', 'Rec. Totales (€)']:
            df_export[col] = df_export[col].round(0).astype(int)
        
        for col in ['Nb Solidaire', 'Nb Normal', 'Nb Soutien']:
            df_export[col] = df_export[col].astype(int)
        
        df_export['Intérêt (%)'] = df_export['Intérêt (%)'].round(1)
        df_export['Population'] = df_export['Population'].round(0).astype(int)
        
        # Filtres
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age_filter = st.multiselect(
                "Filtrer par âge",
                options=sorted(df_export['Âge'].unique()),
                default=sorted(df_export['Âge'].unique())
            )
        
        with col2:
            sexe_filter = st.multiselect(
                "Filtrer par sexe",
                options=['F', 'M'],
                default=['F', 'M']
            )
        
        with col3:
            csp_filter = st.multiselect(
                "Filtrer par CSP",
                options=sorted(df_export['CSP'].unique()),
                default=sorted(df_export['CSP'].unique())
            )
        
        # Appliquer les filtres
        df_filtered = df_export[
            (df_export['Âge'].isin(age_filter)) &
            (df_export['Sexe'].isin(sexe_filter)) &
            (df_export['CSP'].isin(csp_filter))
        ]
        
        st.dataframe(
            df_filtered.sort_values('Rec. Totales (€)', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        
        # Bouton d'export
        csv = df_filtered.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="Télécharger en CSV",
            data=csv,
            file_name=f'simulation_bob_{nb_adherents}_adherents.csv',
            mime='text/csv',
        )
    
    with tab5:
        st.markdown(
            render_section(
                "Résultats de l'enquête (redressés)",
                "Visualisations pondérées après calage sur marges INSEE.",
            ),
            unsafe_allow_html=True,
        )
        
        st.markdown("""
        Cette section présente les réponses à l'enquête BOB **redressées** selon les effectifs 
        réels de la population des IRIS centre-ville de Besançon.
        
        **Pourquoi le redressement ?**
        - L'échantillon de l'enquête ne reflète pas exactement la structure démographique de la population
        - Le redressement applique des poids pour corriger ces biais
        - Les résultats redressés sont plus représentatifs de la population cible
        """)
        
        # Charger les données redressées
        with st.spinner("Chargement et redressement des données de l'enquête..."):
            try:
                df_survey, survey_config = load_weighted_survey_data()
                
                # Vérifier la taille de l'échantillon par profil
                seuil_minimum = 5  # Minimum de répondants par profil pour des résultats fiables
                
                def check_sample_size(df, var_name, seuil=seuil_minimum):
                    """Vérifie la taille de l'échantillon par catégorie et retourne les warnings."""
                    counts = df[var_name].value_counts()
                    warnings = []
                    for category, count in counts.items():
                        if count < seuil:
                            warnings.append(f"- **{category}** : {count} répondant(s) (minimum recommandé : {seuil})")
                    return warnings, counts
                
                # Vérifications par profil
                warnings_age = []
                warnings_sexe = []
                warnings_csp = []
                
                if 'age_group' in df_survey.columns:
                    warnings_age, counts_age = check_sample_size(df_survey, 'age_group', seuil_minimum)
                
                if 'sexe' in df_survey.columns:
                    warnings_sexe, counts_sexe = check_sample_size(df_survey, 'sexe', seuil_minimum)
                
                if 'csp' in df_survey.columns:
                    warnings_csp, counts_csp = check_sample_size(df_survey, 'csp', seuil_minimum)
                
                # Afficher les warnings si nécessaire
                all_warnings = warnings_age + warnings_sexe + warnings_csp
                if all_warnings:
                    st.warning("""
                    **Attention : échantillon trop petit pour certains profils**
                    
                    Les résultats redressés peuvent être peu fiables pour les catégories suivantes avec trop peu de répondants :
                    
                    """ + "\n".join(all_warnings) + f"""
                    
                    **Recommandation** : Interprétez ces résultats avec prudence. Un minimum de {seuil_minimum} répondants par catégorie est recommandé pour des résultats statistiquement fiables.
                    """)
                
                # Statistiques du redressement
                st.markdown('<hr class="bob-divider"/>', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Répondants Besançon", format_nombre(len(df_survey)))
                
                with col2:
                    st.metric("Poids min", format_nombre(df_survey['weight'].min(), 2))
                
                with col3:
                    st.metric("Poids max", format_nombre(df_survey['weight'].max(), 2))
                
                with col4:
                    st.metric("Poids moyen", format_nombre(df_survey['weight'].mean(), 2))
                
                st.markdown('<hr class="bob-divider"/>', unsafe_allow_html=True)
                
                # Sous-onglets pour différentes questions
                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "Intérêt & cotisation",
                    "Partage & usage",
                    "Prix & budget",
                    "Analyses croisées"
                ])
                
                with subtab1:
                    st.markdown("### Intérêt pour le projet et acceptation de la cotisation")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Intérêt pour le projet
                        if 'interet_projet' in df_survey.columns:
                            data_weighted = df_survey.groupby('interet_projet')['weight'].sum()
                            data_pct = (data_weighted / data_weighted.sum() * 100)
                            
                            # Utiliser des couleurs distinctes pour chaque catégorie
                            colors = get_distinct_colors(data_pct.index, color_scheme='positive_negative')
                            
                            fig = go.Figure(data=[go.Pie(
                                labels=data_pct.index,
                                values=data_pct.values,
                                marker=dict(colors=colors),
                                textinfo='label+percent',
                                textposition='auto'
                            )])
                            apply_plotly_theme(
                                fig,
                                title="Intérêt pour le projet (redressé)",
                                height=400,
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Vérifier les effectifs par réponse
                            counts_raw = df_survey['interet_projet'].value_counts()
                            small_categories = [cat for cat, count in counts_raw.items() if count < seuil_minimum]
                            if small_categories:
                                st.info(f"⚠️ **Note** : Les catégories suivantes ont moins de {seuil_minimum} répondants bruts : {', '.join([str(c) for c in small_categories])}. Interprétez ces résultats avec prudence.")
                            
                            # Comparaison avec résultats bruts
                            data_raw = df_survey['interet_projet'].value_counts()
                            data_raw_pct = (data_raw / data_raw.sum() * 100)
                            
                            st.markdown("**Comparaison Brut vs Redressé :**")
                            comp_df = pd.DataFrame({
                                'Réponse': data_pct.index,
                                'Brut (%)': [format_nombre(data_raw_pct.get(x, 0), 1) for x in data_pct.index],
                                'Redressé (%)': [format_nombre(val, 1) for val in data_pct.values]
                            })
                            st.dataframe(comp_df, hide_index=True, use_container_width=True)
                    
                    with col2:
                        # Acceptation cotisation
                        if 'accepte_cotisation' in df_survey.columns:
                            data_weighted = df_survey.groupby('accepte_cotisation')['weight'].sum()
                            data_pct = (data_weighted / data_weighted.sum() * 100)
                            
                            # Simplifier les labels
                            labels_short = [str(x)[:30] + '...' if len(str(x)) > 30 else str(x) for x in data_pct.index]
                            # Utiliser des couleurs distinctes pour chaque catégorie
                            colors = get_distinct_colors(data_pct.index, color_scheme='positive_negative')
                            
                            fig = go.Figure(data=[go.Pie(
                                labels=labels_short,
                                values=data_pct.values,
                                marker=dict(colors=colors),
                                textinfo='percent',
                                textposition='auto'
                            )])
                            apply_plotly_theme(
                                fig,
                                title="Acceptation cotisation (redressé)",
                                height=400,
                            )
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Vérifier les effectifs par réponse
                            counts_raw = df_survey['accepte_cotisation'].value_counts()
                            small_categories = [cat for cat, count in counts_raw.items() if count < seuil_minimum]
                            if small_categories:
                                st.info(f"⚠️ **Note** : {len(small_categories)} catégorie(s) ont moins de {seuil_minimum} répondants bruts. Interprétez ces résultats avec prudence.")
                            
                            # Comparaison avec résultats bruts
                            data_raw = df_survey['accepte_cotisation'].value_counts()
                            data_raw_pct = (data_raw / data_raw.sum() * 100)
                            
                            st.markdown("**Comparaison Brut vs Redressé :**")
                            comp_df = pd.DataFrame({
                                'Réponse': labels_short,
                                'Brut (%)': [format_nombre(data_raw_pct.get(x, 0), 1) for x in data_pct.index],
                                'Redressé (%)': [format_nombre(val, 1) for val in data_pct.values]
                            })
                            st.dataframe(comp_df, hide_index=True, use_container_width=True)
                
                with subtab2:
                    st.markdown("### Partage d'objets et utilisation de services")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Partage d'objets
                        if 'partage_oui' in df_survey.columns:
                            data_weighted = df_survey.groupby('partage_oui')['weight'].sum()
                            data_pct = (data_weighted / data_weighted.sum() * 100)
                            
                            fig = px.bar(
                                x=data_pct.index,
                                y=data_pct.values,
                                labels={'x': 'Réponse', 'y': 'Pourcentage (%)'},
                                title="Accepte de partager des objets (redressé)",
                                color=data_pct.values,
                                color_continuous_scale=SCALE_TEAL
                            )
                            apply_plotly_theme(fig, title="Accepte de partager des objets (redressé)", height=400, showlegend=False)
                            st.plotly_chart(fig, use_container_width=True)
                    
                    with col2:
                        # Utilisation de services
                        if 'deja_utilise_services' in df_survey.columns:
                            data_weighted = df_survey.groupby('deja_utilise_services')['weight'].sum()
                            data_pct = (data_weighted / data_weighted.sum() * 100)
                            
                            # Couleurs sémantiques pour l'utilisation de services
                            # Rouge = jamais, Orange = occasionnellement, Vert = régulièrement
                            color_map = {
                                'non, jamais': COLORS['danger'],
                                'non jamais': COLORS['danger'],
                                'jamais': COLORS['danger'],
                                'non': COLORS['female'],
                                'oui, occasionnellement': COLORS['accent'],
                                'occasionnellement': COLORS['accent'],
                                'oui, régulièrement': COLORS['sage'],
                                'régulièrement': COLORS['sage'],
                                'oui': COLORS['success']
                            }
                            
                            # Créer la liste de couleurs
                            bar_colors = []
                            for label in data_pct.index:
                                label_lower = str(label).lower()
                                color_found = None
                                
                                # Chercher la correspondance la plus spécifique
                                for key, color in sorted(color_map.items(), key=len, reverse=True):
                                    if key in label_lower:
                                        color_found = color
                                        break
                                
                                # Si pas trouvé, utiliser une couleur par défaut
                                if not color_found:
                                    color_found = COLORS['male']
                                
                                bar_colors.append(color_found)
                            
                            # Créer le graphique avec des couleurs distinctes
                            fig = go.Figure(data=[go.Bar(
                                x=data_pct.index,
                                y=data_pct.values,
                                marker=dict(color=bar_colors),
                                text=[f"{val:.1f}%" for val in data_pct.values],
                                textposition='outside'
                            )])
                            
                            apply_plotly_theme(
                                fig,
                                title="Services de location/prêt déjà utilisés (redressé)",
                                height=400,
                                showlegend=False,
                                xaxis_title="Réponse",
                                yaxis_title="Pourcentage (%)",
                            )
                            st.plotly_chart(fig, use_container_width=True)
                
                with subtab3:
                    st.markdown("### Prix maximum accepté pour la location")
                    
                    if 'prix_max_location' in df_survey.columns:
                        df_clean = df_survey[df_survey['prix_max_location'].notna()].copy()
                        
                        # Convertir prix_max_location en numérique si c'est une chaîne
                        # Supprime les caractères non numériques (€, espaces, etc.)
                        def convert_price_to_numeric(value):
                            """Convertit une valeur de prix en numérique."""
                            if pd.isna(value):
                                return np.nan
                            if isinstance(value, (int, float)):
                                return float(value)
                            # Si c'est une chaîne, extraire le nombre
                            match = re.search(r'(\d+(?:[.,]\d+)?)', str(value))
                            if match:
                                # Remplacer la virgule par un point pour la conversion
                                return float(match.group(1).replace(',', '.'))
                            return np.nan
                        
                        df_clean['prix_max_location_numeric'] = df_clean['prix_max_location'].apply(convert_price_to_numeric)
                        df_clean_numeric = df_clean[df_clean['prix_max_location_numeric'].notna()].copy()
                        
                        if len(df_clean_numeric) > 0:
                            # Calculer la moyenne pondérée
                            mean_weighted = np.average(df_clean_numeric['prix_max_location_numeric'], weights=df_clean_numeric['weight'])
                            mean_raw = df_clean_numeric['prix_max_location_numeric'].mean()
                        
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Prix moyen (Redressé)", f"{format_nombre(mean_weighted, 2)} €")
                            with col2:
                                st.metric("Prix moyen (Brut)", f"{format_nombre(mean_raw, 2)} €")
                            with col3:
                                diff = mean_weighted - mean_raw
                                signe = "+" if diff >= 0 else ""
                                st.metric("Différence", f"{signe}{format_nombre(diff, 2)} €")
                            
                            # Histogramme
                            fig = go.Figure()
                            
                            # Résultats redressés
                            fig.add_trace(go.Histogram(
                                x=df_clean_numeric['prix_max_location_numeric'],
                                histfunc='sum',
                                y=df_clean_numeric['weight'],
                                name='Redressé',
                                marker_color=COLORS['primary'],
                                opacity=0.7,
                                nbinsx=15
                            ))
                            
                            # Ligne de moyenne
                            fig.add_vline(
                                x=mean_weighted,
                                line_dash="dash",
                                line_color=COLORS['accent'],
                                annotation_text=f"Moyenne: {format_nombre(mean_weighted, 2)}€"
                            )
                            
                            apply_plotly_theme(
                                fig,
                                title="Distribution du prix maximum accepté (redressé)",
                                height=400,
                                xaxis_title="Prix (€)",
                                yaxis_title="Effectif pondéré",
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("Aucune donnée numérique valide trouvée dans la colonne 'prix_max_location'.")
                
                with subtab4:
                    st.markdown("### Analyses croisées par profil")
                    
                    # Sélection de la variable à analyser
                    analyse_vars = []
                    if 'interet_projet' in df_survey.columns:
                        analyse_vars.append('interet_projet')
                    if 'accepte_cotisation' in df_survey.columns:
                        analyse_vars.append('accepte_cotisation')
                    if 'partage_oui' in df_survey.columns:
                        analyse_vars.append('partage_oui')
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        analyse_var = st.selectbox(
                            "Variable à analyser",
                            analyse_vars if analyse_vars else ['interet_projet'],
                            format_func=lambda x: {
                                'interet_projet': 'Intérêt pour le projet',
                                'accepte_cotisation': 'Acceptation cotisation',
                                'partage_oui': 'Partage d\'objets'
                            }.get(x, x)
                        )
                    
                    with col2:
                        profile_var = st.selectbox(
                            "Variable de profil",
                            ['age_group', 'sexe', 'csp'],
                            format_func=lambda x: {
                                'age_group': 'Tranche d\'âge',
                                'sexe': 'Sexe',
                                'csp': 'Situation professionnelle'
                            }.get(x, x)
                        )
                    
                    # Créer le graphique croisé
                    if analyse_var and profile_var:
                        # Vérifier les effectifs bruts par cellule (croisement)
                        crosstab_counts = pd.crosstab(
                            df_survey[profile_var],
                            df_survey[analyse_var]
                        )
                        
                        # Détecter les cellules avec trop peu de répondants
                        cellules_peu_fiables = []
                        for i in crosstab_counts.index:
                            for j in crosstab_counts.columns:
                                count = crosstab_counts.loc[i, j]
                                if count > 0 and count < seuil_minimum:
                                    cellules_peu_fiables.append({
                                        'profil': i,
                                        'reponse': j,
                                        'nb': count
                                    })
                        
                        # Afficher un warning si nécessaire
                        if cellules_peu_fiables:
                            st.warning(f"""
                            ⚠️ **Attention : Échantillons trop petits dans certaines cellules**
                            
                            Les résultats suivants sont basés sur moins de {seuil_minimum} répondants bruts et peuvent être peu fiables :
                            
                            """ + "\n".join([
                                f"- **{cell['profil']} × {cell['reponse']}** : {cell['nb']} répondant(s)"
                                for cell in cellules_peu_fiables[:10]  # Limiter à 10 pour ne pas surcharger
                            ]) + (f"\n\n... et {len(cellules_peu_fiables) - 10} autre(s)" if len(cellules_peu_fiables) > 10 else "") + f"""
                            
                            **Effectifs bruts par cellule** (recommandé ≥ {seuil_minimum} par cellule) :
                            """)
                            
                            # Afficher le tableau des effectifs avec mise en évidence
                            st.dataframe(
                                crosstab_counts,
                                use_container_width=True
                            )
                            
                            st.caption(f"⚠️ Les valeurs en rouge dans le tableau ci-dessus indiquent des effectifs < {seuil_minimum} répondants (peu fiables).")
                        
                        # Créer le tableau des pourcentages redressés
                        crosstab = pd.crosstab(
                            df_survey[profile_var],
                            df_survey[analyse_var],
                            values=df_survey['weight'],
                            aggfunc='sum',
                            normalize='index'
                        ) * 100
                        
                        fig = go.Figure()
                        
                        for col in crosstab.columns:
                            fig.add_trace(go.Bar(
                                name=str(col)[:30],
                                x=crosstab.index,
                                y=crosstab[col],
                            ))
                        
                        apply_plotly_theme(
                            fig,
                            title=f"{analyse_var} selon {profile_var} (redressé)",
                            height=500,
                            barmode='group',
                            xaxis_title=profile_var,
                            yaxis_title="Pourcentage (%)",
                            legend_title=analyse_var,
                        )
                        
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Afficher le tableau
                        st.markdown("**Tableau détaillé (%) :**")
                        # Formater le tableau avec virgules pour décimales
                        crosstab_formatted = crosstab.map(lambda x: format_nombre(x, 1))
                        st.dataframe(crosstab_formatted, use_container_width=True)
                
            except Exception as e:
                st.error(f"Erreur lors du chargement des données de l'enquête : {e}")
                st.info("Vérifiez que les fichiers de données sont correctement configurés.")
                import traceback
                st.code(traceback.format_exc(), language='python')
    
    # Footer
    st.markdown("""
    <div class="bob-footer">
        <p><strong>BOB Finance</strong> — Bibliothèque d'Objets Besançon</p>
        <p>Ajustez les paramètres latéraux pour explorer différents scénarios budgétaires.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()

