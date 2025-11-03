"""
Script pour préparer les marges de référence à partir de la base infracommunale INSEE 2022.
Cette base contient déjà les données agrégées par IRIS.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Configuration
BASE_IC_FILE = r"D:\python_work\bob-enquete\data\base-ic-evol-struct-pop-2022_csv\base-ic-evol-struct-pop-2022.CSV"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv"

# IRIS centre-ville de Besançon
IRIS_CENTER = [
    '250560101', '250560102', '250560103', '250560104',
    '250560302', '250560303', '250560304',
    '250560401', '250560402',
    '250560501', '250560502'
]


def load_base_ic(file_path: str) -> pd.DataFrame:
    """
    Charge la base infracommunale INSEE.
    
    Args:
        file_path: Chemin vers le fichier CSV
    
    Returns:
        DataFrame de la base IC
    """
    print(f"Chargement de la base infracommunale : {file_path}")
    df = pd.read_csv(file_path, sep=';', dtype={'IRIS': str})
    print(f"  - {len(df):,} IRIS chargés")
    return df


def filter_center_iris(df: pd.DataFrame, iris_list: list) -> pd.DataFrame:
    """
    Filtre sur les IRIS centre-ville.
    
    Args:
        df: DataFrame de la base IC
        iris_list: Liste des codes IRIS
    
    Returns:
        DataFrame filtré
    """
    print(f"\nFiltrage sur {len(iris_list)} IRIS centre-ville...")
    
    df_center = df[df['IRIS'].isin(iris_list)].copy()
    
    print(f"  - {len(df_center)} IRIS trouvés")
    print(f"  - IRIS : {sorted(df_center['IRIS'].tolist())}")
    
    return df_center


def create_margins_from_base_ic(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée les marges à partir de la base infracommunale.
    
    La base IC contient :
    - P22_POP1824 : Population 18-24 ans
    - P22_POP2539 : Population 25-39 ans
    - P22_POP4054 : Population 40-54 ans
    - P22_POP5564 : Population 55-64 ans
    - P22_POP65P : Population 65 ans et plus
    - P22_POPH : Population hommes
    - P22_POPF : Population femmes
    - C22_POP15P_STAT_GSEC* : Population 15+ par statut d'activité
    
    Args:
        df: DataFrame filtré sur les IRIS
    
    Returns:
        DataFrame des marges
    """
    print("\nCréation des marges...")
    
    margins_list = []
    
    for _, row in df.iterrows():
        iris = row['IRIS']
        
        # Population totale par âge
        pop_1824 = row['P22_POP1824']
        pop_2539 = row['P22_POP2539']
        pop_4054 = row['P22_POP4054']
        pop_5564 = row['P22_POP5564']
        pop_65p = row['P22_POP65P']
        
        # Population par sexe
        pop_h = row['P22_POPH']
        pop_f = row['P22_POPF']
        
        # Population 15+ par activité
        pop_15p = row['C22_POP15P']
        # Actifs occupés (codes 11-21 à 16-26)
        actifs = (row['C22_POP15P_STAT_GSEC11_21'] + row['C22_POP15P_STAT_GSEC12_22'] + 
                  row['C22_POP15P_STAT_GSEC13_23'] + row['C22_POP15P_STAT_GSEC14_24'] +
                  row['C22_POP15P_STAT_GSEC15_25'] + row['C22_POP15P_STAT_GSEC16_26'])
        # Chômeurs
        chomeurs = row['C22_POP15P_STAT_GSEC32']
        # Inactifs
        inactifs = row['C22_POP15P_STAT_GSEC40']
        
        # Calculer les proportions d'activité
        if pop_15p > 0:
            pct_actifs = actifs / pop_15p
            pct_chomeurs = chomeurs / pop_15p
            pct_inactifs = inactifs / pop_15p
        else:
            pct_actifs = pct_chomeurs = pct_inactifs = 0
        
        # Calculer la proportion H/F
        pop_total = pop_h + pop_f
        if pop_total > 0:
            pct_h = pop_h / pop_total
            pct_f = pop_f / pop_total
        else:
            pct_h = pct_f = 0.5
        
        # Créer les marges pour chaque combinaison
        # On va découper 25-39 en 25-34 et 35-39, et 40-54 en 40-44 et 45-54
        
        age_groups = {
            '18-24': pop_1824,
            '25-34': pop_2539 * 0.6,  # Approximation : 60% de 25-39
            '35-44': pop_2539 * 0.4 + pop_4054 * 0.33,  # 40% de 25-39 + 33% de 40-54
            '45-54': pop_4054 * 0.67,  # 67% de 40-54
            '55-64': pop_5564,
            '65+': pop_65p
        }
        
        for age_group, pop_age in age_groups.items():
            if pop_age <= 0:
                continue
            
            for sexe, pct_sexe in [('M', pct_h), ('F', pct_f)]:
                pop_age_sexe = pop_age * pct_sexe
                
                if pop_age_sexe <= 0:
                    continue
                
                # Répartir selon l'activité
                for csp, pct_csp in [(1, pct_actifs), (2, pct_chomeurs), (3, pct_inactifs)]:
                    pop_final = pop_age_sexe * pct_csp
                    
                    if pop_final > 0.5:  # Garder seulement si > 0.5 personne
                        margins_list.append({
                            'code_iris': iris,
                            'age_group': age_group,
                            'sexe': sexe,
                            'csp': float(csp),
                            'population': round(pop_final, 2)
                        })
    
    margins_df = pd.DataFrame(margins_list)
    
    print(f"  - {len(margins_df)} cellules créées")
    print(f"  - Population totale : {margins_df['population'].sum():,.0f}")
    
    return margins_df


def display_statistics(margins: pd.DataFrame):
    """
    Affiche les statistiques des marges.
    
    Args:
        margins: DataFrame des marges
    """
    print("\n" + "="*70)
    print("STATISTIQUES DES MARGES")
    print("="*70)
    
    print(f"\nPopulation totale : {margins['population'].sum():,.0f}")
    print(f"Nombre d'IRIS : {margins['code_iris'].nunique()}")
    print(f"Nombre de cellules : {len(margins)}")
    
    print("\nPopulation par IRIS :")
    pop_iris = margins.groupby('code_iris')['population'].sum().sort_values(ascending=False)
    for iris, pop in pop_iris.items():
        print(f"  {iris} : {pop:6,.0f}")
    
    print("\nRépartition par âge :")
    pop_age = margins.groupby('age_group')['population'].sum()
    total = pop_age.sum()
    for age, pop in pop_age.items():
        pct = pop / total * 100
        print(f"  {age:10s} : {pop:6,.0f} ({pct:5.1f}%)")
    
    print("\nRépartition par sexe :")
    pop_sexe = margins.groupby('sexe')['population'].sum()
    for sexe, pop in pop_sexe.items():
        pct = pop / total * 100
        print(f"  {sexe} : {pop:6,.0f} ({pct:5.1f}%)")
    
    print("\nRépartition par CSP :")
    pop_csp = margins.groupby('csp')['population'].sum()
    csp_labels = {1.0: 'Actifs occupés', 2.0: 'Chômeurs', 3.0: 'Inactifs'}
    for csp, pop in pop_csp.items():
        label = csp_labels.get(csp, 'Inconnu')
        pct = pop / total * 100
        print(f"  {int(csp)} - {label:20s} : {pop:6,.0f} ({pct:5.1f}%)")
    
    print("\nStatistiques des cellules :")
    print(f"  - Population min : {margins['population'].min():.1f}")
    print(f"  - Population max : {margins['population'].max():.1f}")
    print(f"  - Population moyenne : {margins['population'].mean():.1f}")


def save_margins(margins: pd.DataFrame, output_path: Path):
    """
    Sauvegarde les marges.
    
    Args:
        margins: DataFrame des marges
        output_path: Chemin de sortie
    """
    print(f"\nSauvegarde des marges : {output_path}")
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    margins.to_csv(output_path, index=False)
    
    print(f"  [OK] Fichier sauvegardé")


def main():
    """Fonction principale."""
    print("="*70)
    print("PREPARATION DES MARGES DEPUIS LA BASE INFRACOMMUNALE INSEE 2022")
    print("="*70)
    
    try:
        # 1. Charger la base IC
        df = load_base_ic(BASE_IC_FILE)
        
        # 2. Filtrer sur les IRIS centre-ville
        df_center = filter_center_iris(df, IRIS_CENTER)
        
        # 3. Créer les marges
        margins = create_margins_from_base_ic(df_center)
        
        # 4. Afficher les statistiques
        display_statistics(margins)
        
        # 5. Sauvegarder
        save_margins(margins, OUTPUT_FILE)
        
        # Résumé final
        print("\n" + "="*70)
        print("SUCCES !")
        print("="*70)
        print(f"Fichier de marges créé : {OUTPUT_FILE}")
        print(f"Population totale : {margins['population'].sum():,.0f}")
        print(f"Nombre d'IRIS : {margins['code_iris'].nunique()}")
        print(f"Nombre de cellules : {len(margins)}")
        print("\nVous pouvez maintenant relancer le redressement :")
        print("  python src/cli.py run --config config.yaml")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

