"""
Script pour corriger les fonctions de redressement dans l'application.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import sys

# Ajouter les chemins
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR / "src"))

from raking import RakingWeighter


def prepare_margins_for_raking(margins_df, weighting_vars):
    """
    Prépare les marges au format attendu par RakingWeighter.
    
    Args:
        margins_df: DataFrame avec colonnes [age_group, sexe, csp, population]
        weighting_vars: Liste des variables de redressement
    
    Returns:
        Dict[str, pd.Series]: Dictionnaire {variable: Series(index=catégorie, values=effectif)}
    """
    # Mapper les CSP numériques vers les labels
    csp_mapping = {
        1.0: 'Actifs',
        2.0: 'Etudiants/Chomeurs',
        3.0: 'Retraites'
    }
    
    # Créer une copie pour ne pas modifier l'original
    margins = margins_df.copy()
    
    # Convertir CSP si nécessaire
    if 'csp' in margins.columns and margins['csp'].dtype in [np.float64, np.int64]:
        margins['csp'] = margins['csp'].map(csp_mapping)
    
    # Créer le dictionnaire de marges
    margins_dict = {}
    
    for var in weighting_vars:
        if var in margins.columns:
            # Agréger par variable
            var_margins = margins.groupby(var)['population'].sum()
            margins_dict[var] = var_margins
    
    return margins_dict


def load_and_weight_survey_data():
    """
    Charge et redresse les données de l'enquête.
    
    Returns:
        df_weighted: DataFrame avec poids
        config: Configuration
    """
    # Charger la configuration
    config_path = BASE_DIR / "config.yaml"
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    # Charger les données
    data_path = BASE_DIR / config['paths']['raw_data']
    margins_path = BASE_DIR / config['paths']['margins']
    
    print(f"Chargement de {data_path}...")
    df = pd.read_excel(data_path)
    print(f"  - {len(df)} répondants chargés")
    
    print(f"Chargement de {margins_path}...")
    margins_df = pd.read_csv(margins_path)
    print(f"  - {len(margins_df)} lignes de marges")
    
    # Filtrer sur Besançon
    df_besancon = df[df['is_besancon'] == 1].copy()
    print(f"  - {len(df_besancon)} répondants de Besançon")
    
    # Préparer les marges
    margins_dict = prepare_margins_for_raking(margins_df, config['survey']['weighting_vars'])
    
    print("\nMarges préparées :")
    for var, margins in margins_dict.items():
        print(f"  - {var}: {len(margins)} catégories, total = {margins.sum():.0f}")
    
    # Créer le weighter
    weighter = RakingWeighter(
        max_iterations=config['raking']['max_iterations'],
        tolerance=config['raking']['tolerance'],
        min_weight=config['raking']['min_weight'],
        max_weight=config['raking']['max_weight']
    )
    
    # Initialiser les poids
    df_besancon['weight'] = config['raking']['initial_weight']
    
    print(f"\nRedressement en cours...")
    df_weighted = weighter.rake(df_besancon, margins_dict, weight_col='weight')
    
    print(f"✓ Redressement terminé")
    print(f"  - Convergence: {weighter.has_converged}")
    print(f"  - Itérations: {weighter.n_iterations}")
    print(f"  - Poids min: {df_weighted['weight'].min():.2f}")
    print(f"  - Poids max: {df_weighted['weight'].max():.2f}")
    print(f"  - Poids moyen: {df_weighted['weight'].mean():.2f}")
    
    return df_weighted, config


if __name__ == "__main__":
    print("=" * 60)
    print("TEST DE LA FONCTION DE REDRESSEMENT")
    print("=" * 60)
    
    try:
        df_weighted, config = load_and_weight_survey_data()
        print("\n✓ Test réussi !")
    except Exception as e:
        print(f"\n✗ Erreur: {e}")
        import traceback
        traceback.print_exc()

