"""
Module de génération de rapports PDF.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import List, Dict, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Configuration du style des graphiques
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10


def plot_weight_distribution(
    weights: pd.Series,
    output_path: str,
    title: str = "Distribution des poids"
) -> str:
    """
    Crée un graphique de la distribution des poids.
    
    Args:
        weights: Series des poids
        output_path: Chemin de sortie
        title: Titre du graphique
    
    Returns:
        Chemin du fichier créé
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogramme
    ax1.hist(weights, bins=50, edgecolor='black', alpha=0.7)
    ax1.set_xlabel('Poids')
    ax1.set_ylabel('Fréquence')
    ax1.set_title('Histogramme des poids')
    ax1.axvline(weights.mean(), color='red', linestyle='--', 
                label=f'Moyenne: {weights.mean():.2f}')
    ax1.axvline(weights.median(), color='green', linestyle='--', 
                label=f'Médiane: {weights.median():.2f}')
    ax1.legend()
    
    # Boxplot
    ax2.boxplot(weights, vert=True)
    ax2.set_ylabel('Poids')
    ax2.set_title('Boxplot des poids')
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle(title, fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sauvegardé : {output_path}")
    return output_path


def plot_convergence(
    convergence_history: List[float],
    output_path: str,
    tolerance: float = None
) -> str:
    """
    Crée un graphique de convergence du raking.
    
    Args:
        convergence_history: Historique des écarts
        output_path: Chemin de sortie
        tolerance: Seuil de tolérance (optionnel)
    
    Returns:
        Chemin du fichier créé
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    iterations = range(1, len(convergence_history) + 1)
    ax.plot(iterations, convergence_history, marker='o', linewidth=2)
    
    if tolerance is not None:
        ax.axhline(tolerance, color='red', linestyle='--', 
                   label=f'Tolérance: {tolerance}')
        ax.legend()
    
    ax.set_xlabel('Itération')
    ax.set_ylabel('Écart maximum')
    ax.set_title('Convergence du raking', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sauvegardé : {output_path}")
    return output_path


def plot_comparison_distribution(
    comparison_df: pd.DataFrame,
    variable: str,
    output_path: str
) -> str:
    """
    Compare les distributions avant/après redressement.
    
    Args:
        comparison_df: DataFrame de comparaison
        variable: Nom de la variable
        output_path: Chemin de sortie
    
    Returns:
        Chemin du fichier créé
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = range(len(comparison_df))
    width = 0.35
    
    ax.bar([i - width/2 for i in x], comparison_df['pct_initial'], 
           width, label='Avant redressement', alpha=0.8)
    ax.bar([i + width/2 for i in x], comparison_df['pct_final'], 
           width, label='Après redressement', alpha=0.8)
    
    ax.set_xlabel('Modalités')
    ax.set_ylabel('Pourcentage (%)')
    ax.set_title(f'Comparaison des distributions - {variable}', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(comparison_df.index, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sauvegardé : {output_path}")
    return output_path


def plot_frequency(
    freq_df: pd.DataFrame,
    variable: str,
    output_path: str,
    top_n: int = None
) -> str:
    """
    Crée un graphique de fréquence.
    
    Args:
        freq_df: DataFrame avec colonnes 'effectif' et 'pourcentage'
        variable: Nom de la variable
        output_path: Chemin de sortie
        top_n: Nombre de modalités à afficher (None = toutes)
    
    Returns:
        Chemin du fichier créé
    """
    if top_n is not None:
        freq_df = freq_df.head(top_n)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique en barres
    freq_df['effectif'].plot(kind='bar', ax=ax1, color='steelblue', alpha=0.8)
    ax1.set_xlabel('Modalités')
    ax1.set_ylabel('Effectif pondéré')
    ax1.set_title('Effectifs')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Graphique circulaire
    ax2.pie(freq_df['pourcentage'], labels=freq_df.index, autopct='%1.1f%%',
            startangle=90)
    ax2.set_title('Répartition')
    
    plt.suptitle(f'Distribution de {variable}', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sauvegardé : {output_path}")
    return output_path


def plot_crosstab(
    crosstab_df: pd.DataFrame,
    var1: str,
    var2: str,
    output_path: str
) -> str:
    """
    Crée une heatmap pour un tableau croisé.
    
    Args:
        crosstab_df: DataFrame du tableau croisé
        var1: Nom de la première variable
        var2: Nom de la deuxième variable
        output_path: Chemin de sortie
    
    Returns:
        Chemin du fichier créé
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(crosstab_df, annot=True, fmt='.1f', cmap='YlOrRd', 
                cbar_kws={'label': 'Effectif pondéré'}, ax=ax)
    
    ax.set_xlabel(var2)
    ax.set_ylabel(var1)
    ax.set_title(f'Tableau croisé : {var1} × {var2}', 
                 fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sauvegardé : {output_path}")
    return output_path


def plot_group_comparison(
    comparison_df: pd.DataFrame,
    variable: str,
    group_var: str,
    output_path: str
) -> str:
    """
    Compare une variable entre groupes.
    
    Args:
        comparison_df: DataFrame de comparaison
        variable: Variable analysée
        group_var: Variable de groupement
        output_path: Chemin de sortie
    
    Returns:
        Chemin du fichier créé
    """
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x = range(len(comparison_df))
    
    ax.bar(x, comparison_df['mean'], alpha=0.8, color='steelblue')
    ax.errorbar(x, comparison_df['mean'], yerr=comparison_df['std'], 
                fmt='none', color='black', capsize=5)
    
    ax.set_xlabel(group_var)
    ax.set_ylabel(f'{variable} (moyenne)')
    ax.set_title(f'Comparaison de {variable} par {group_var}', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(comparison_df[group_var], rotation=45, ha='right')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    logger.info(f"Graphique sauvegardé : {output_path}")
    return output_path


def generate_html_report(
    config: Dict[str, Any],
    results: Dict[str, Any],
    output_path: str
) -> str:
    """
    Génère un rapport HTML.
    
    Args:
        config: Configuration du projet
        results: Résultats de l'analyse
        output_path: Chemin de sortie
    
    Returns:
        Chemin du fichier créé
    """
    html_content = f"""
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{config.get('report', {}).get('title', 'Rapport d\'analyse')}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            th {{
                background-color: #3498db;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .metric {{
                display: inline-block;
                margin: 10px 20px;
                padding: 15px;
                background-color: #ecf0f1;
                border-radius: 5px;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
            }}
            .metric-label {{
                font-size: 14px;
                color: #7f8c8d;
            }}
            img {{
                max-width: 100%;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <h1>{config.get('report', {}).get('title', 'Rapport d\'analyse d\'enquête')}</h1>
        <p><strong>Date :</strong> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        <p><strong>Auteur :</strong> {config.get('report', {}).get('author', 'N/A')}</p>
        
        <h2>1. Résumé</h2>
        <div class="metric">
            <div class="metric-label">Nombre de répondants</div>
            <div class="metric-value">{results.get('n_respondents', 'N/A')}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Variables de redressement</div>
            <div class="metric-value">{results.get('n_weighting_vars', 'N/A')}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Convergence</div>
            <div class="metric-value">{'Oui' if results.get('converged', False) else 'Non'}</div>
        </div>
        
        <h2>2. Qualité du redressement</h2>
        <p>Le redressement a convergé en <strong>{results.get('n_iterations', 'N/A')}</strong> itérations.</p>
        
        <h2>3. Figures</h2>
        <!-- Les figures seront insérées ici -->
        
        <h2>4. Conclusion</h2>
        <p>Rapport généré automatiquement par bob-enquete.</p>
    </body>
    </html>
    """
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    logger.info(f"Rapport HTML sauvegardé : {output_path}")
    return output_path

