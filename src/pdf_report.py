"""
Module de génération de rapports PDF complets avec ReportLab.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY

logger = logging.getLogger(__name__)


class PDFReportGenerator:
    """
    Générateur de rapports PDF pour l'analyse d'enquête BOB.
    """
    
    def __init__(self, title: str = "Rapport d'analyse BOB", author: str = ""):
        """
        Initialise le générateur de rapport.
        
        Args:
            title: Titre du rapport
            author: Auteur du rapport
        """
        self.title = title
        self.author = author
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
        self.story = []
    
    def _setup_custom_styles(self):
        """Configure les styles personnalisés."""
        # Titre principal
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Sous-sous-titre
        self.styles.add(ParagraphStyle(
            name='CustomHeading3',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=colors.HexColor('#34495e'),
            spaceAfter=10,
            spaceBefore=10,
            fontName='Helvetica-Bold'
        ))
        
        # Corps de texte
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))
        
        # Métrique en gras
        self.styles.add(ParagraphStyle(
            name='Metric',
            parent=self.styles['BodyText'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            fontName='Helvetica-Bold'
        ))
    
    def add_title_page(self, subtitle: str = None, date: str = None):
        """
        Ajoute une page de titre.
        
        Args:
            subtitle: Sous-titre optionnel
            date: Date du rapport
        """
        if date is None:
            date = datetime.now().strftime('%d/%m/%Y')
        
        self.story.append(Spacer(1, 5*cm))
        self.story.append(Paragraph(self.title, self.styles['CustomTitle']))
        
        if subtitle:
            self.story.append(Spacer(1, 0.5*cm))
            self.story.append(Paragraph(subtitle, self.styles['Heading2']))
        
        self.story.append(Spacer(1, 2*cm))
        self.story.append(Paragraph(f"<b>Date :</b> {date}", self.styles['CustomBody']))
        
        if self.author:
            self.story.append(Paragraph(f"<b>Auteur :</b> {self.author}", self.styles['CustomBody']))
        
        self.story.append(PageBreak())
    
    def add_section(self, title: str, level: int = 2):
        """
        Ajoute un titre de section.
        
        Args:
            title: Titre de la section
            level: Niveau de titre (2 ou 3)
        """
        style = 'CustomHeading2' if level == 2 else 'CustomHeading3'
        self.story.append(Paragraph(title, self.styles[style]))
    
    def add_paragraph(self, text: str):
        """
        Ajoute un paragraphe de texte.
        
        Args:
            text: Texte du paragraphe
        """
        self.story.append(Paragraph(text, self.styles['CustomBody']))
        self.story.append(Spacer(1, 0.3*cm))
    
    def add_metrics_box(self, metrics: Dict[str, Any]):
        """
        Ajoute un encadré avec des métriques clés.
        
        Args:
            metrics: Dictionnaire {label: valeur}
        """
        data = []
        for label, value in metrics.items():
            if isinstance(value, float):
                value_str = f"{value:,.2f}".replace(',', ' ')
            elif isinstance(value, int):
                value_str = f"{value:,}".replace(',', ' ')
            else:
                value_str = str(value)
            
            data.append([label, value_str])
        
        table = Table(data, colWidths=[10*cm, 5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2c3e50')),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.white)
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_table(self, df: pd.DataFrame, title: str = None, max_rows: int = None):
        """
        Ajoute un tableau depuis un DataFrame.
        
        Args:
            df: DataFrame à afficher
            title: Titre du tableau
            max_rows: Nombre maximum de lignes à afficher
        """
        if title:
            self.add_section(title, level=3)
        
        if max_rows and len(df) > max_rows:
            df = df.head(max_rows)
            self.add_paragraph(f"<i>Affichage des {max_rows} premières lignes sur {len(df)}</i>")
        
        # Préparer les données
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Formater les nombres
        for i in range(1, len(data)):
            for j in range(len(data[i])):
                val = data[i][j]
                if isinstance(val, float):
                    if abs(val) < 1 and val != 0:
                        data[i][j] = f"{val:.3f}"
                    else:
                        data[i][j] = f"{val:.2f}"
                elif pd.isna(val):
                    data[i][j] = "-"
        
        # Calculer les largeurs de colonnes
        n_cols = len(df.columns)
        col_width = 15 * cm / n_cols
        
        table = Table(data, colWidths=[col_width] * n_cols)
        table.setStyle(TableStyle([
            # En-tête
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498db')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            
            # Corps
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Grille
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            
            # Alternance de couleurs
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f2f2f2')])
        ]))
        
        self.story.append(table)
        self.story.append(Spacer(1, 0.5*cm))
    
    def add_image(self, image_path: str, width: float = 15*cm, title: str = None):
        """
        Ajoute une image au rapport.
        
        Args:
            image_path: Chemin vers l'image
            width: Largeur de l'image
            title: Titre de l'image
        """
        if title:
            self.add_section(title, level=3)
        
        if Path(image_path).exists():
            img = Image(image_path, width=width)
            self.story.append(img)
            self.story.append(Spacer(1, 0.5*cm))
        else:
            logger.warning(f"Image non trouvée : {image_path}")
            self.add_paragraph(f"<i>Image non disponible : {image_path}</i>")
    
    def add_quality_section(self, quality_metrics: Dict[str, float]):
        """
        Ajoute une section sur la qualité du redressement.
        
        Args:
            quality_metrics: Métriques de qualité (Deff, n_eff, etc.)
        """
        self.add_section("Qualité du redressement", level=2)
        
        self.add_paragraph(
            "Les métriques suivantes permettent d'évaluer la qualité du redressement statistique :"
        )
        
        # Métriques principales
        main_metrics = {
            "Nombre d'observations": int(quality_metrics.get('n_observations', 0)),
            "Taille effective (n_eff)": quality_metrics.get('n_eff', 0),
            "Effet de plan (Deff)": quality_metrics.get('deff', 0),
            "Perte d'efficacité (%)": quality_metrics.get('loss_efficiency', 0)
        }
        
        self.add_metrics_box(main_metrics)
        
        # Interprétation
        deff = quality_metrics.get('deff', 1)
        n_eff = quality_metrics.get('n_eff', 0)
        
        interpretation = f"""
        <b>Interprétation :</b><br/>
        • <b>Deff = {deff:.2f}</b> : L'effet de plan indique que la variance est multipliée par {deff:.2f} 
        par rapport à un échantillon aléatoire simple. Une valeur proche de 1 est idéale.<br/>
        • <b>n_eff = {n_eff:.0f}</b> : L'échantillon pondéré équivaut à un échantillon aléatoire simple 
        de {n_eff:.0f} observations en termes de précision.<br/>
        """
        
        if deff < 1.5:
            interpretation += "• ✓ La qualité du redressement est <b>excellente</b>.<br/>"
        elif deff < 2.0:
            interpretation += "• ⚠ La qualité du redressement est <b>acceptable</b>.<br/>"
        else:
            interpretation += "• ⚠ La qualité du redressement est <b>médiocre</b>. Les poids sont très dispersés.<br/>"
        
        self.add_paragraph(interpretation)
        
        # Statistiques des poids
        self.add_section("Statistiques des poids", level=3)
        
        weight_stats = {
            "Poids moyen": quality_metrics.get('mean_weight', 0),
            "Écart-type": quality_metrics.get('std_weight', 0),
            "CV (%)": quality_metrics.get('cv_weight', 0) * 100,
            "Poids minimum": quality_metrics.get('min_weight', 0),
            "Poids maximum": quality_metrics.get('max_weight', 0)
        }
        
        self.add_metrics_box(weight_stats)
    
    def add_page_break(self):
        """Ajoute un saut de page."""
        self.story.append(PageBreak())
    
    def add_spacer(self, height: float = 0.5):
        """
        Ajoute un espace vertical.
        
        Args:
            height: Hauteur en cm
        """
        self.story.append(Spacer(1, height*cm))
    
    def save(self, output_path: str):
        """
        Sauvegarde le rapport PDF.
        
        Args:
            output_path: Chemin de sortie
        """
        # Convertir Path en string si nécessaire
        output_path_str = str(output_path)
        
        doc = SimpleDocTemplate(
            output_path_str,
            pagesize=A4,
            rightMargin=2*cm,
            leftMargin=2*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        doc.build(self.story)
        logger.info(f"Rapport PDF sauvegardé : {output_path_str}")


def generate_global_report(
    df: pd.DataFrame,
    quality_metrics: Dict[str, float],
    margins_quality: pd.DataFrame,
    figures_dir: Path,
    output_path: str,
    config: Dict[str, Any]
) -> str:
    """
    Génère le rapport global de l'enquête BOB.
    
    Args:
        df: DataFrame avec données pondérées
        quality_metrics: Métriques de qualité
        margins_quality: DataFrame de qualité du calage
        figures_dir: Répertoire des figures
        output_path: Chemin de sortie
        config: Configuration
    
    Returns:
        Chemin du fichier créé
    """
    report = PDFReportGenerator(
        title="Enquête BOB - Rapport Global",
        author=config.get('report', {}).get('author', '')
    )
    
    # Page de titre
    report.add_title_page(subtitle="Analyse complète avec redressement")
    
    # 1. Résumé exécutif
    report.add_section("1. Résumé exécutif", level=2)
    report.add_paragraph(
        f"Ce rapport présente les résultats de l'enquête BOB menée auprès de "
        f"{len(df)} répondants. Les données ont été redressées selon les marges "
        f"IRIS centre-ville pour assurer la représentativité de l'échantillon."
    )
    
    summary_metrics = {
        "Nombre de répondants": len(df),
        "Variables de redressement": len(config['survey']['weighting_vars']),
        "Somme des poids": df['weight'].sum()
    }
    report.add_metrics_box(summary_metrics)
    
    # 2. Qualité du redressement
    report.add_quality_section(quality_metrics)
    
    # Graphiques de qualité
    weight_dist_fig = figures_dir / 'weights_distribution.png'
    if weight_dist_fig.exists():
        report.add_image(str(weight_dist_fig), title="Distribution des poids")
    
    convergence_fig = figures_dir / 'convergence.png'
    if convergence_fig.exists():
        report.add_image(str(convergence_fig), title="Convergence du raking")
    
    # 3. Qualité du calage sur marges
    report.add_page_break()
    report.add_section("3. Qualité du calage sur marges", level=2)
    
    if not margins_quality.empty:
        # Résumé par variable
        summary = margins_quality.groupby('variable').agg({
            'ecart_relatif': lambda x: x.abs().max()
        }).reset_index()
        summary.columns = ['Variable', 'Écart relatif max']
        
        report.add_table(summary, title="Écarts maximaux par variable")
    
    # 4. Analyses descriptives
    report.add_page_break()
    report.add_section("4. Analyses descriptives", level=2)
    
    # Ajouter les graphiques de comparaison
    for var in config['survey']['weighting_vars']:
        comparison_fig = figures_dir / f'comparison_{var}.png'
        if comparison_fig.exists():
            report.add_image(str(comparison_fig), title=f"Distribution de {var}")
    
    # Sauvegarder
    report.save(output_path)
    return output_path


def generate_subgroup_report(
    df: pd.DataFrame,
    filter_condition: pd.Series,
    subgroup_name: str,
    quality_metrics: Dict[str, float],
    figures_dir: Path,
    output_path: str,
    config: Dict[str, Any]
) -> str:
    """
    Génère un rapport pour un sous-groupe spécifique.
    
    Args:
        df: DataFrame complet
        filter_condition: Condition de filtrage (Series booléenne)
        subgroup_name: Nom du sous-groupe
        quality_metrics: Métriques de qualité
        figures_dir: Répertoire des figures
        output_path: Chemin de sortie
        config: Configuration
    
    Returns:
        Chemin du fichier créé
    """
    df_sub = df[filter_condition].copy()
    
    report = PDFReportGenerator(
        title=f"Enquête BOB - Rapport {subgroup_name}",
        author=config.get('report', {}).get('author', '')
    )
    
    # Page de titre
    report.add_title_page(subtitle=f"Analyse du sous-groupe : {subgroup_name}")
    
    # Résumé
    report.add_section("1. Caractéristiques du sous-groupe", level=2)
    
    metrics = {
        "Nombre de répondants": len(df_sub),
        "% de l'échantillon total": len(df_sub) / len(df) * 100,
        "Somme des poids": df_sub['weight'].sum()
    }
    report.add_metrics_box(metrics)
    
    # Qualité
    report.add_quality_section(quality_metrics)
    
    # Analyses spécifiques au sous-groupe
    report.add_page_break()
    report.add_section("2. Analyses descriptives", level=2)
    
    # Ajouter les analyses pertinentes pour ce sous-groupe
    
    report.save(output_path)
    return output_path

