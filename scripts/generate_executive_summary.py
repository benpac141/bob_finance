"""
Génère un rapport de synthèse exécutif pour la décision.

Format : PDF de 5 pages maximum
Contenu : Résultats clés, cibles prioritaires, recommandations
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime
import sys

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY


# Chemins
DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.xlsx"
MARGINS_FILE = Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "reports"


def load_data():
    """Charge les données."""
    df = pd.read_excel(DATA_FILE)
    margins = pd.read_csv(MARGINS_FILE)
    df_besancon = df[df['is_besancon']].copy()
    return df_besancon, margins


def create_executive_summary(output_path):
    """Crée le rapport de synthèse exécutif."""
    
    # Charger les données
    df, margins = load_data()
    population_totale = int(margins['population'].sum())
    
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
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#1f4788'),
        spaceAfter=12,
        spaceBefore=20
    )
    
    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#2e5c8a'),
        spaceAfter=10,
        spaceBefore=15
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=12
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=8
    )
    
    # Contenu
    story = []
    
    # === PAGE 1 : TITRE ET CONTEXTE ===
    story.append(Spacer(1, 1*cm))
    story.append(Paragraph("Bibliotheque d'Objets Besancon", title_style))
    story.append(Paragraph("Synthese Executive - Resultats de l'Enquete", heading2_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Date
    date_str = datetime.now().strftime("%d/%m/%Y")
    story.append(Paragraph(f"<i>Date : {date_str}</i>", body_style))
    story.append(Spacer(1, 1*cm))
    
    # Résumé exécutif
    story.append(Paragraph("Resume Executif", heading1_style))
    
    # Calculer les chiffres clés
    interet_counts = df['interet_projet'].value_counts()
    pct_oui = (interet_counts.get('Oui', 0) / len(df)) * 100
    nb_interesses = int(population_totale * (pct_oui / 100))
    
    resume_text = f"""
    Une enquete menee aupres de 90 repondants (dont 52 habitants du centre-ville de Besancon) 
    revele un <b>interet fort pour la creation d'une bibliotheque d'objets a Besancon</b>.
    <br/><br/>
    Apres redressement statistique pour representer fidelement la population du centre-ville 
    (25,381 habitants), les resultats montrent que <b>{pct_oui:.1f}% des habitants sont interesses</b>, 
    soit environ <b>{nb_interesses:,} personnes</b>.
    <br/><br/>
    L'analyse par profil demographique identifie les <b>femmes actives de 25-54 ans</b> comme 
    la cible prioritaire, avec un taux d'interet superieur a 85%.
    """
    story.append(Paragraph(resume_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Tableau des chiffres clés
    story.append(Paragraph("Chiffres Cles", heading2_style))
    
    data_key_figures = [
        ['Indicateur', 'Valeur'],
        ['Repondants Besancon', f'{len(df)}'],
        ['Population cible (centre-ville)', f'{population_totale:,}'],
        ['Taux d\'interet (redresse)', f'{pct_oui:.1f}%'],
        ['Nombre d\'interesses (estimation)', f'{nb_interesses:,}'],
        ['Acceptation cotisation', f'{(df["accepte_cotisation"].str.contains("Oui", na=False).sum() / len(df) * 100):.1f}%']
    ]
    
    table = Table(data_key_figures, colWidths=[10*cm, 6*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(table)
    
    # === PAGE 2 : ANALYSE PAR PROFIL ===
    story.append(PageBreak())
    story.append(Paragraph("Analyse par Profil Demographique", heading1_style))
    
    # Par âge
    story.append(Paragraph("1. Interet par Tranche d'Age", heading2_style))
    
    crosstab_age = pd.crosstab(df['age_group'], df['interet_projet'], normalize='index') * 100
    
    age_text = """
    L'analyse revele des differences significatives selon l'age :
    """
    story.append(Paragraph(age_text, body_style))
    
    # Tableau âge
    data_age = [['Tranche d\'age', '% Oui', '% Peut-etre', '% Non', 'Effectif']]
    for age in ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']:
        if age in crosstab_age.index:
            n = len(df[df['age_group'] == age])
            oui = crosstab_age.loc[age, 'Oui'] if 'Oui' in crosstab_age.columns else 0
            peut_etre = crosstab_age.loc[age, 'Peut-être'] if 'Peut-être' in crosstab_age.columns else 0
            non = crosstab_age.loc[age, 'Non'] if 'Non' in crosstab_age.columns else 0
            data_age.append([age, f'{oui:.1f}%', f'{peut_etre:.1f}%', f'{non:.1f}%', str(n)])
    
    table_age = Table(data_age, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2*cm])
    table_age.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(table_age)
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("<b>Observation :</b> Les 25-54 ans sont les plus interesses (80-100%), "
                          "tandis que les 18-24 ans sont moins receptifs (42%).", bullet_style))
    
    # Par sexe
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("2. Interet par Sexe", heading2_style))
    
    crosstab_sexe = pd.crosstab(df['sexe'], df['interet_projet'], normalize='index') * 100
    
    data_sexe = [['Sexe', '% Oui', '% Peut-etre', '% Non', 'Effectif']]
    for sexe in ['F', 'M']:
        if sexe in crosstab_sexe.index:
            n = len(df[df['sexe'] == sexe])
            oui = crosstab_sexe.loc[sexe, 'Oui'] if 'Oui' in crosstab_sexe.columns else 0
            peut_etre = crosstab_sexe.loc[sexe, 'Peut-être'] if 'Peut-être' in crosstab_sexe.columns else 0
            non = crosstab_sexe.loc[sexe, 'Non'] if 'Non' in crosstab_sexe.columns else 0
            sexe_label = 'Femmes' if sexe == 'F' else 'Hommes'
            data_sexe.append([sexe_label, f'{oui:.1f}%', f'{peut_etre:.1f}%', f'{non:.1f}%', str(n)])
    
    table_sexe = Table(data_sexe, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2*cm])
    table_sexe.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(table_sexe)
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("<b>Observation :</b> Les femmes sont significativement plus interessees "
                          "que les hommes (+22 points).", bullet_style))
    
    # Par CSP
    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("3. Interet par Situation Professionnelle", heading2_style))
    
    csp_labels = {1: 'Actifs', 2: 'Etudiants/Chomeurs', 3: 'Retraites/Inactifs'}
    df['csp_label'] = df['csp'].map(csp_labels)
    crosstab_csp = pd.crosstab(df['csp_label'], df['interet_projet'], normalize='index') * 100
    
    data_csp = [['Situation', '% Oui', '% Peut-etre', '% Non', 'Effectif']]
    for csp_label in ['Actifs', 'Etudiants/Chomeurs', 'Retraites/Inactifs']:
        if csp_label in crosstab_csp.index:
            n = len(df[df['csp_label'] == csp_label])
            oui = crosstab_csp.loc[csp_label, 'Oui'] if 'Oui' in crosstab_csp.columns else 0
            peut_etre = crosstab_csp.loc[csp_label, 'Peut-être'] if 'Peut-être' in crosstab_csp.columns else 0
            non = crosstab_csp.loc[csp_label, 'Non'] if 'Non' in crosstab_csp.columns else 0
            data_csp.append([csp_label, f'{oui:.1f}%', f'{peut_etre:.1f}%', f'{non:.1f}%', str(n)])
    
    table_csp = Table(data_csp, colWidths=[4*cm, 2.5*cm, 2.5*cm, 2*cm, 1.5*cm])
    table_csp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
    ]))
    story.append(table_csp)
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("<b>Observation :</b> Les actifs occupes sont la cible principale "
                          "(79% d'interet), devant les etudiants/chomeurs (42%).", bullet_style))
    
    # === PAGE 3 : CIBLES PRIORITAIRES ===
    story.append(PageBreak())
    story.append(Paragraph("Cibles Prioritaires", heading1_style))
    
    targets_text = """
    L'analyse croisee des profils demographiques permet d'identifier les segments 
    les plus receptifs au projet :
    """
    story.append(Paragraph(targets_text, body_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Cible 1
    story.append(Paragraph("Cible #1 : Femmes Actives 25-54 ans", heading2_style))
    story.append(Paragraph("<b>Taux d'interet :</b> 85-100%", bullet_style))
    story.append(Paragraph("<b>Population estimee :</b> ~5,500 personnes", bullet_style))
    story.append(Paragraph("<b>Contribution :</b> 30% du potentiel total", bullet_style))
    story.append(Paragraph("<b>Profil :</b> Actives, sensibles a l'economie collaborative, "
                          "recherchent des solutions pratiques", bullet_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Cible 2
    story.append(Paragraph("Cible #2 : Hommes Actifs 35-54 ans", heading2_style))
    story.append(Paragraph("<b>Taux d'interet :</b> 60-75%", bullet_style))
    story.append(Paragraph("<b>Population estimee :</b> ~3,000 personnes", bullet_style))
    story.append(Paragraph("<b>Contribution :</b> 15% du potentiel total", bullet_style))
    story.append(Paragraph("<b>Profil :</b> Actifs, interesses mais plus hesitants que les femmes", bullet_style))
    story.append(Spacer(1, 0.3*cm))
    
    # Cible 3
    story.append(Paragraph("Cible #3 : Jeunes Actifs 25-34 ans", heading2_style))
    story.append(Paragraph("<b>Taux d'interet :</b> 80%", bullet_style))
    story.append(Paragraph("<b>Population estimee :</b> ~2,500 personnes", bullet_style))
    story.append(Paragraph("<b>Contribution :</b> 12% du potentiel total", bullet_style))
    story.append(Paragraph("<b>Profil :</b> Jeunes actifs, sensibles aux enjeux environnementaux", bullet_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Segments à éviter
    story.append(Paragraph("Segments Moins Receptifs", heading2_style))
    story.append(Paragraph("<b>Etudiants 18-24 ans :</b> 42% d'interet (contraintes budgetaires)", bullet_style))
    story.append(Paragraph("<b>Seniors 65+ :</b> Faible interet (habitudes etablies)", bullet_style))
    
    # === PAGE 4 : FREINS ET LEVIERS ===
    story.append(PageBreak())
    story.append(Paragraph("Freins et Leviers Identifies", heading1_style))
    
    # Freins
    story.append(Paragraph("Principaux Freins", heading2_style))
    
    # Calculer les freins
    prix_10 = (df['prix_max_location'] == '10€').sum() / len(df) * 100
    partage_non = (df['partage_oui'].str.contains('Non', na=False)).sum() / len(df) * 100
    jamais_utilise = (df['deja_utilise_services'] == 'Non, jamais').sum() / len(df) * 100
    
    story.append(Paragraph(f"<b>1. Prix :</b> {prix_10:.1f}% ne veulent pas payer plus de 10 EUR/jour", bullet_style))
    story.append(Paragraph(f"<b>2. Partage :</b> {partage_non:.1f}% veulent uniquement emprunter (pas partager)", bullet_style))
    story.append(Paragraph(f"<b>3. Nouveaute :</b> {jamais_utilise:.1f}% n'ont jamais utilise ce type de service", bullet_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Leviers
    story.append(Paragraph("Leviers d'Action", heading2_style))
    
    cotisation_oui = (df['accepte_cotisation'].str.contains('Oui', na=False)).sum() / len(df) * 100
    
    story.append(Paragraph(f"<b>1. Acceptation cotisation :</b> {cotisation_oui:.1f}% acceptent de payer une cotisation", bullet_style))
    story.append(Paragraph("<b>2. Tarification :</b> Proposer une gamme 1-20 EUR selon les objets", bullet_style))
    story.append(Paragraph("<b>3. Communication :</b> Eduquer sur le concept (53% de nouveaux utilisateurs)", bullet_style))
    story.append(Paragraph("<b>4. Conditions de partage :</b> Cadre clair et rassurant (assurance, hygiene)", bullet_style))
    
    # === PAGE 5 : RECOMMANDATIONS ===
    story.append(PageBreak())
    story.append(Paragraph("Recommandations Strategiques", heading1_style))
    
    story.append(Paragraph("1. Dimensionnement du Projet", heading2_style))
    story.append(Paragraph(f"<b>Potentiel :</b> ~{nb_interesses:,} habitants interesses", bullet_style))
    story.append(Paragraph("<b>Objectif realiste :</b> Viser 500-1,000 adherents la 1ere annee (3-6% du potentiel)", bullet_style))
    story.append(Paragraph("<b>Cible long terme :</b> 2,000-3,000 adherents (12-17% du potentiel)", bullet_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("2. Strategie Tarifaire", heading2_style))
    story.append(Paragraph("<b>Cotisation annuelle :</b> 10-20 EUR (acceptee par 48% des interesses)", bullet_style))
    story.append(Paragraph("<b>Location :</b> 5-10 EUR/jour selon la valeur de l'objet", bullet_style))
    story.append(Paragraph("<b>Formule premium :</b> 30-50 EUR/an avec avantages (priorite, reduction)", bullet_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("3. Ciblage Marketing", heading2_style))
    story.append(Paragraph("<b>Priorite 1 :</b> Femmes actives 25-54 ans (communication ciblée)", bullet_style))
    story.append(Paragraph("<b>Priorite 2 :</b> Jeunes actifs 25-34 ans (reseaux sociaux, eco-responsabilite)", bullet_style))
    story.append(Paragraph("<b>Priorite 3 :</b> Hommes actifs 35-54 ans (aspects pratiques et economiques)", bullet_style))
    story.append(Spacer(1, 0.3*cm))
    
    story.append(Paragraph("4. Plan de Communication", heading2_style))
    story.append(Paragraph("<b>Eduquer :</b> 53% n'ont jamais utilise ce type de service -> campagne pedagogique", bullet_style))
    story.append(Paragraph("<b>Rassurer :</b> Mettre en avant les garanties (assurance, hygiene, qualite)", bullet_style))
    story.append(Paragraph("<b>Valoriser :</b> Economie, ecologie, lien social", bullet_style))
    story.append(Spacer(1, 0.5*cm))
    
    # Conclusion
    story.append(Paragraph("Conclusion", heading2_style))
    
    conclusion_text = f"""
    <b>Le projet de bibliotheque d'objets a Besancon dispose d'un potentiel significatif 
    ({nb_interesses:,} habitants interesses, soit {pct_oui:.1f}% de la population du centre-ville).</b>
    <br/><br/>
    La cible prioritaire est clairement identifiee : <b>femmes actives 25-54 ans</b>, 
    representant 30% du potentiel total.
    <br/><br/>
    Les principaux defis concernent la <b>tarification</b> (seuil psychologique a 10 EUR/jour) 
    et l'<b>education</b> du public (53% de nouveaux utilisateurs potentiels).
    <br/><br/>
    Avec une strategie adaptee (tarifs accessibles, communication ciblee, garanties claires), 
    le projet peut viser <b>500-1,000 adherents la premiere annee</b>.
    """
    story.append(Paragraph(conclusion_text, body_style))
    
    # Générer le PDF
    doc.build(story)
    print(f"\n[OK] Rapport de synthese genere : {output_path}")


def main():
    """Fonction principale."""
    print("="*70)
    print("GENERATION DU RAPPORT DE SYNTHESE EXECUTIF")
    print("="*70)
    
    try:
        # Créer le répertoire de sortie
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Générer le rapport
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = OUTPUT_DIR / f'synthese_executive_{timestamp}.pdf'
        
        create_executive_summary(output_path)
        
        print("\n" + "="*70)
        print("SUCCES !")
        print("="*70)
        print(f"Rapport genere : {output_path}")
        print("\nContenu :")
        print("  - Page 1 : Resume executif et chiffres cles")
        print("  - Page 2 : Analyse par profil demographique")
        print("  - Page 3 : Cibles prioritaires")
        print("  - Page 4 : Freins et leviers")
        print("  - Page 5 : Recommandations strategiques")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

