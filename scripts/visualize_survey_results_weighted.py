"""
Visualisation des résultats de l'enquête BOB redressés.

Ce script génère des graphiques pour toutes les questions de l'enquête,
en appliquant les poids du redressement (raking) pour obtenir des résultats
représentatifs de la population des IRIS centre-ville de Besançon.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import yaml
import sys
import re

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from raking import RakingWeighter


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

# Configuration de style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Chemins
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_FILE = PROJECT_ROOT / "config.yaml"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "figures" / "enquete_redresse"


def load_config():
    """Charge la configuration."""
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_and_weight_data(config):
    """
    Charge les données et applique le redressement.
    
    Returns:
        df_weighted: DataFrame avec les poids calculés
        df_besancon: DataFrame filtré sur Besançon avec poids
    """
    # Charger les données
    data_path = PROJECT_ROOT / config['paths']['raw_data']
    margins_path = PROJECT_ROOT / config['paths']['margins']
    
    df = pd.read_excel(data_path)
    margins = pd.read_csv(margins_path)
    
    print(f"[OK] Donnees chargees : {len(df)} repondants")
    
    # Filtrer sur Besançon pour le redressement
    df_besancon = df[df['is_besancon'] == 1].copy()
    print(f"[OK] Besancon : {len(df_besancon)} repondants")
    
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
    margins['csp'] = margins['csp'].map(csp_mapping).fillna(margins['csp'])
    
    # Préparer les marges au format dictionnaire
    margins_dict = {}
    for var in config['survey']['weighting_vars']:
        if var in margins.columns:
            var_margins = margins.groupby(var)['population'].sum()
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
    print(f"[OK] Redressement effectue (convergence : {weighter.has_converged})")
    print(f"  - Iterations : {weighter.n_iterations}")
    print(f"  - Poids min : {df_weighted['weight'].min():.2f}")
    print(f"  - Poids max : {df_weighted['weight'].max():.2f}")
    print(f"  - Poids moyen : {df_weighted['weight'].mean():.2f}")
    
    return df_weighted, margins


def plot_categorical_weighted(df, variable, title, output_name, weights_col='weight'):
    """
    Crée un graphique en barres pour une variable catégorielle redressée.
    
    Args:
        df: DataFrame avec les données
        variable: Nom de la colonne à visualiser
        title: Titre du graphique
        output_name: Nom du fichier de sortie
        weights_col: Nom de la colonne de poids
    """
    # Calculer les effectifs pondérés
    weighted_counts = df.groupby(variable)[weights_col].sum()
    weighted_pct = (weighted_counts / weighted_counts.sum() * 100)
    
    # Calculer les effectifs bruts pour comparaison
    raw_counts = df[variable].value_counts()
    raw_pct = (raw_counts / raw_counts.sum() * 100)
    
    # Créer le graphique
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Graphique 1 : Résultats redressés
    colors = sns.color_palette("husl", len(weighted_pct))
    bars1 = ax1.bar(range(len(weighted_pct)), weighted_pct.values, color=colors)
    ax1.set_xticks(range(len(weighted_pct)))
    ax1.set_xticklabels(weighted_pct.index, rotation=45, ha='right')
    ax1.set_ylabel('Pourcentage (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Résultats Redressés (Population IRIS)', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for i, (bar, val) in enumerate(zip(bars1, weighted_pct.values)):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%\n(n={int(weighted_counts.iloc[i])})',
                ha='center', va='bottom', fontsize=10)
    
    # Graphique 2 : Résultats bruts
    bars2 = ax2.bar(range(len(raw_pct)), raw_pct.values, color=colors, alpha=0.6)
    ax2.set_xticks(range(len(raw_pct)))
    ax2.set_xticklabels(raw_pct.index, rotation=45, ha='right')
    ax2.set_ylabel('Pourcentage (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Résultats Bruts (Échantillon)', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Ajouter les valeurs sur les barres
    for i, (bar, val) in enumerate(zip(bars2, raw_pct.values)):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{val:.1f}%\n(n={int(raw_counts.iloc[i])})',
                ha='center', va='bottom', fontsize=10)
    
    # Titre général
    fig.suptitle(title, fontsize=16, fontweight='bold', y=1.00)
    
    plt.tight_layout()
    
    # Sauvegarder
    output_path = OUTPUT_DIR / f"{output_name}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Graphique sauvegarde : {output_path}")
    plt.close()


def plot_numeric_weighted(df, variable, title, output_name, bins=10, weights_col='weight'):
    """
    Crée un histogramme pour une variable numérique redressée.
    
    Args:
        df: DataFrame avec les données
        variable: Nom de la colonne à visualiser
        title: Titre du graphique
        output_name: Nom du fichier de sortie
        bins: Nombre de bins pour l'histogramme
        weights_col: Nom de la colonne de poids
    """
    # Nettoyer les valeurs manquantes
    df_clean = df[df[variable].notna()].copy()
    
    # Convertir en numérique si c'est prix_max_location
    if variable == 'prix_max_location':
        df_clean['prix_max_location_numeric'] = df_clean[variable].apply(convert_price_to_numeric)
        df_clean = df_clean[df_clean['prix_max_location_numeric'].notna()].copy()
        variable_numeric = 'prix_max_location_numeric'
    else:
        variable_numeric = variable
    
    if len(df_clean) == 0:
        print(f"[WARN] Aucune donnee numerique valide pour {variable}")
        return
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Histogramme redressé
    ax1.hist(df_clean[variable_numeric], bins=bins, weights=df_clean[weights_col],
             color='steelblue', edgecolor='black', alpha=0.7)
    ax1.set_xlabel(variable, fontsize=12, fontweight='bold')
    ax1.set_ylabel('Effectif pondéré', fontsize=12, fontweight='bold')
    ax1.set_title('Distribution Redressée (Population IRIS)', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Statistiques redressées
    mean_weighted = np.average(df_clean[variable_numeric], weights=df_clean[weights_col])
    median_weighted = df_clean[variable_numeric].median()  # Approximation
    ax1.axvline(mean_weighted, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {mean_weighted:.2f}')
    ax1.legend()
    
    # Histogramme brut
    ax2.hist(df_clean[variable_numeric], bins=bins, color='steelblue', 
             edgecolor='black', alpha=0.6)
    ax2.set_xlabel(variable, fontsize=12, fontweight='bold')
    ax2.set_ylabel('Effectif brut', fontsize=12, fontweight='bold')
    ax2.set_title('Distribution Brute (Échantillon)', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Statistiques brutes
    mean_raw = df_clean[variable_numeric].mean()
    ax2.axvline(mean_raw, color='red', linestyle='--', linewidth=2, label=f'Moyenne: {mean_raw:.2f}')
    ax2.legend()
    
    # Titre général
    fig.suptitle(title, fontsize=16, fontweight='bold', y=1.00)
    
    plt.tight_layout()
    
    # Sauvegarder
    output_path = OUTPUT_DIR / f"{output_name}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Graphique sauvegarde : {output_path}")
    plt.close()


def plot_comparison_by_profile(df, variable, profile_var, title, output_name, weights_col='weight'):
    """
    Compare les réponses selon un profil démographique (redressé).
    
    Args:
        df: DataFrame avec les données
        variable: Variable à analyser
        profile_var: Variable de profil (age_group, sexe, csp)
        title: Titre du graphique
        output_name: Nom du fichier de sortie
        weights_col: Nom de la colonne de poids
    """
    # Calculer les proportions pondérées par profil
    crosstab = pd.crosstab(
        df[profile_var],
        df[variable],
        values=df[weights_col],
        aggfunc='sum',
        normalize='index'
    ) * 100
    
    # Créer le graphique
    fig, ax = plt.subplots(figsize=(12, 6))
    
    crosstab.plot(kind='bar', ax=ax, width=0.8)
    
    ax.set_xlabel(profile_var, fontsize=12, fontweight='bold')
    ax.set_ylabel('Pourcentage (%)', fontsize=12, fontweight='bold')
    ax.set_title(title, fontsize=14, fontweight='bold')
    ax.legend(title=variable, bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(axis='y', alpha=0.3)
    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Sauvegarder
    output_path = OUTPUT_DIR / f"{output_name}.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Graphique sauvegarde : {output_path}")
    plt.close()


def create_summary_dashboard(df, weights_col='weight'):
    """
    Crée un tableau de bord récapitulatif des principales réponses.
    """
    fig = plt.figure(figsize=(16, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
    
    # 1. Intérêt pour le projet
    ax1 = fig.add_subplot(gs[0, 0])
    if 'interet_projet' in df.columns:
        data = df.groupby('interet_projet')[weights_col].sum()
        data_pct = (data / data.sum() * 100)
        colors = ['#2ecc71' if 'Oui' in str(x) else '#e74c3c' for x in data_pct.index]
        ax1.pie(data_pct.values, labels=data_pct.index, autopct='%1.1f%%',
                colors=colors, startangle=90)
        ax1.set_title("Intérêt pour le projet", fontweight='bold')
    
    # 2. Acceptation cotisation
    ax2 = fig.add_subplot(gs[0, 1])
    if 'accepte_cotisation' in df.columns:
        data = df.groupby('accepte_cotisation')[weights_col].sum()
        data_pct = (data / data.sum() * 100)
        colors = ['#2ecc71' if 'Oui' in str(x) else '#e74c3c' for x in data_pct.index]
        ax2.pie(data_pct.values, labels=[str(x)[:20] + '...' if len(str(x)) > 20 else str(x) for x in data_pct.index],
                autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title("Acceptation cotisation", fontweight='bold')
    
    # 3. Partage d'objets
    ax3 = fig.add_subplot(gs[0, 2])
    if 'partage_oui' in df.columns:
        data = df.groupby('partage_oui')[weights_col].sum()
        data_pct = (data / data.sum() * 100)
        colors = ['#2ecc71' if x == 'Oui' else '#e74c3c' for x in data_pct.index]
        ax3.pie(data_pct.values, labels=data_pct.index, autopct='%1.1f%%',
                colors=colors, startangle=90)
        ax3.set_title("Accepte de partager des objets", fontweight='bold')
    
    # 4. Distribution par âge
    ax4 = fig.add_subplot(gs[1, 0])
    data = df.groupby('age_group')[weights_col].sum().sort_values(ascending=True)
    ax4.barh(range(len(data)), data.values, color='steelblue')
    ax4.set_yticks(range(len(data)))
    ax4.set_yticklabels(data.index)
    ax4.set_xlabel('Effectif pondéré')
    ax4.set_title("Distribution par âge", fontweight='bold')
    ax4.grid(axis='x', alpha=0.3)
    
    # 5. Distribution par sexe
    ax5 = fig.add_subplot(gs[1, 1])
    data = df.groupby('sexe')[weights_col].sum()
    colors = ['#e74c3c' if x == 'F' else '#3498db' for x in data.index]
    ax5.bar(range(len(data)), data.values, color=colors, edgecolor='black')
    ax5.set_xticks(range(len(data)))
    ax5.set_xticklabels(['Femmes' if x == 'F' else 'Hommes' for x in data.index])
    ax5.set_ylabel('Effectif pondéré')
    ax5.set_title("Distribution par sexe", fontweight='bold')
    ax5.grid(axis='y', alpha=0.3)
    
    # 6. Distribution par CSP
    ax6 = fig.add_subplot(gs[1, 2])
    data = df.groupby('csp')[weights_col].sum().sort_values(ascending=True)
    ax6.barh(range(len(data)), data.values, color='darkorange')
    ax6.set_yticks(range(len(data)))
    ax6.set_yticklabels(data.index)
    ax6.set_xlabel('Effectif pondéré')
    ax6.set_title("Distribution par CSP", fontweight='bold')
    ax6.grid(axis='x', alpha=0.3)
    
    # 7. Prix maximum de location
    ax7 = fig.add_subplot(gs[2, :])
    if 'prix_max_location' in df.columns:
        df_clean = df[df['prix_max_location'].notna()].copy()
        
        # Convertir prix_max_location en numérique
        df_clean['prix_max_location_numeric'] = df_clean['prix_max_location'].apply(convert_price_to_numeric)
        df_clean_numeric = df_clean[df_clean['prix_max_location_numeric'].notna()].copy()
        
        if len(df_clean_numeric) > 0:
            ax7.hist(df_clean_numeric['prix_max_location_numeric'], bins=15, 
                    weights=df_clean_numeric[weights_col],
                    color='mediumseagreen', edgecolor='black', alpha=0.7)
            mean_weighted = np.average(df_clean_numeric['prix_max_location_numeric'], weights=df_clean_numeric[weights_col])
            ax7.axvline(mean_weighted, color='red', linestyle='--', linewidth=2,
                       label=f'Moyenne: {mean_weighted:.2f}€')
            ax7.set_xlabel('Prix maximum (€)', fontweight='bold')
            ax7.set_ylabel('Effectif pondéré', fontweight='bold')
            ax7.set_title("Distribution du prix maximum accepté pour la location", fontweight='bold')
            ax7.legend()
            ax7.grid(axis='y', alpha=0.3)
        else:
            ax7.text(0.5, 0.5, 'Aucune donnée numérique valide', 
                    ha='center', va='center', transform=ax7.transAxes)
            ax7.set_title("Distribution du prix maximum accepté pour la location", fontweight='bold')
    
    fig.suptitle("Tableau de Bord - Enquête BOB (Résultats Redressés)",
                 fontsize=18, fontweight='bold', y=0.995)
    
    # Sauvegarder
    output_path = OUTPUT_DIR / "dashboard_enquete_redresse.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"[OK] Dashboard sauvegarde : {output_path}")
    plt.close()


def main():
    """Fonction principale."""
    print("=" * 60)
    print("VISUALISATION DES RÉSULTATS DE L'ENQUÊTE BOB (REDRESSÉS)")
    print("=" * 60)
    
    # Créer le répertoire de sortie
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Charger la configuration
    config = load_config()
    
    # Charger et redresser les données
    print("\n1. Chargement et redressement des données...")
    df_weighted, margins = load_and_weight_data(config)
    
    # Créer le dashboard récapitulatif
    print("\n2. Création du tableau de bord récapitulatif...")
    create_summary_dashboard(df_weighted)
    
    # Variables à visualiser
    print("\n3. Création des graphiques détaillés...")
    
    # Questions principales
    if 'interet_projet' in df_weighted.columns:
        plot_categorical_weighted(
            df_weighted,
            'interet_projet',
            "Une bibliothèque d'objets à Besançon vous intéresserait-elle ?",
            "01_interet_projet"
        )
    
    if 'accepte_cotisation' in df_weighted.columns:
        plot_categorical_weighted(
            df_weighted,
            'accepte_cotisation',
            "Accepteriez-vous de payer une cotisation ?",
            "02_accepte_cotisation"
        )
    
    if 'deja_utilise_services' in df_weighted.columns:
        plot_categorical_weighted(
            df_weighted,
            'deja_utilise_services',
            "Avez-vous déjà utilisé des services de location ou de prêt d'objets ?",
            "03_deja_utilise"
        )
    
    if 'partage_oui' in df_weighted.columns:
        plot_categorical_weighted(
            df_weighted,
            'partage_oui',
            "Accepteriez-vous de partager certains de vos objets personnels ?",
            "04_partage_objets"
        )
    
    # Variable numérique
    if 'prix_max_location' in df_weighted.columns:
        plot_numeric_weighted(
            df_weighted,
            'prix_max_location',
            "Prix maximum accepté pour la location d'un objet (200€ neuf)",
            "05_prix_max_location",
            bins=15
        )
    
    # Analyses croisées par profil
    print("\n4. Création des analyses croisées par profil...")
    
    if 'interet_projet' in df_weighted.columns and 'age_group' in df_weighted.columns:
        plot_comparison_by_profile(
            df_weighted,
            'interet_projet',
            'age_group',
            "Intérêt pour le projet selon l'âge (Redressé)",
            "06_interet_par_age"
        )
    
    if 'interet_projet' in df_weighted.columns and 'csp' in df_weighted.columns:
        plot_comparison_by_profile(
            df_weighted,
            'interet_projet',
            'csp',
            "Intérêt pour le projet selon la CSP (Redressé)",
            "07_interet_par_csp"
        )
    
    if 'accepte_cotisation' in df_weighted.columns and 'age_group' in df_weighted.columns:
        plot_comparison_by_profile(
            df_weighted,
            'accepte_cotisation',
            'age_group',
            "Acceptation cotisation selon l'âge (Redressé)",
            "08_cotisation_par_age"
        )
    
    if 'partage_oui' in df_weighted.columns and 'sexe' in df_weighted.columns:
        plot_comparison_by_profile(
            df_weighted,
            'partage_oui',
            'sexe',
            "Partage d'objets selon le sexe (Redressé)",
            "09_partage_par_sexe"
        )
    
    print("\n" + "=" * 60)
    print("[OK] VISUALISATIONS TERMINEES")
    print(f"[OK] Graphiques sauvegardes dans : {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

