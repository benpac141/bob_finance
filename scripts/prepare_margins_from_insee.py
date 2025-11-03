"""
Script pour préparer les marges de référence à partir du recensement INSEE 2022.

Ce script :
1. Charge le fichier individu du recensement 2022
2. Filtre sur les IRIS centre-ville de Besançon
3. Crée les marges par âge, sexe, et autres variables
4. Export vers data/margins/margins_center.csv
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Configuration
CENSUS_FILE = r"D:\python_work\eqasim-bfc\data\raw\census_2022.csv"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv"

# IRIS centre-ville de Besançon
IRIS_CENTER = [
    '250560101', '250560102', '250560103', '250560104',
    '250560302', '250560303', '250560304',
    '250560401', '250560402',
    '250560501', '250560502'
]

# Mapping des tranches d'âge
AGE_GROUPS = {
    '18-24': (18, 24),
    '25-34': (25, 34),
    '35-44': (35, 44),
    '45-54': (45, 54),
    '55-64': (55, 64),
    '65+': (65, 120)
}


def load_census_data(file_path: str) -> pd.DataFrame:
    """
    Charge le fichier de recensement.
    
    Args:
        file_path: Chemin vers le fichier CSV
    
    Returns:
        DataFrame du recensement
    """
    print(f"Chargement du fichier : {file_path}")
    df = pd.read_csv(file_path, sep=";", dtype=str)
    print(f"  - {len(df):,} individus charges")
    print(f"  - {len(df.columns)} colonnes")
    return df


def filter_center_iris(df: pd.DataFrame, iris_list: list) -> pd.DataFrame:
    """
    Filtre les données sur les IRIS centre-ville.
    
    Args:
        df: DataFrame du recensement
        iris_list: Liste des codes IRIS
    
    Returns:
        DataFrame filtré
    """
    print(f"\nFiltrage sur {len(iris_list)} IRIS centre-ville...")
    
    # Filtrer directement sur les codes IRIS (format string)
    df_center = df[df['IRIS'].isin(iris_list)].copy()
    
    # Garder le code IRIS en string
    df_center['code_iris'] = df_center['IRIS']
    
    print(f"  - {len(df_center):,} individus dans le centre-ville")
    print(f"  - {len(df_center['code_iris'].unique())} IRIS trouves")
    
    # Afficher les IRIS trouvés
    iris_found = sorted(df_center['code_iris'].unique())
    print(f"  - IRIS trouves : {iris_found}")
    
    return df_center


def create_age_groups(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée les tranches d'âge.
    
    Args:
        df: DataFrame
    
    Returns:
        DataFrame avec colonne age_group
    """
    print("\nCreation des tranches d'age...")
    
    # Convertir l'âge en numérique
    df['age_numeric'] = pd.to_numeric(df['AGED'], errors='coerce')
    
    # Créer les tranches
    def assign_age_group(age):
        if pd.isna(age):
            return None
        for group_name, (min_age, max_age) in AGE_GROUPS.items():
            if min_age <= age <= max_age:
                return group_name
        return None
    
    df['age_group'] = df['age_numeric'].apply(assign_age_group)
    
    # Filtrer les adultes (18+)
    df = df[df['age_group'].notna()].copy()
    
    print(f"  - {len(df):,} adultes (18+) conserves")
    print(f"  - Repartition par age :")
    for group in AGE_GROUPS.keys():
        count = (df['age_group'] == group).sum()
        pct = count / len(df) * 100
        print(f"    {group:10s} : {count:6,} ({pct:5.1f}%)")
    
    return df


def map_gender(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mappe le sexe (1=H, 2=F vers M/F).
    
    Args:
        df: DataFrame
    
    Returns:
        DataFrame avec colonne sexe
    """
    print("\nMapping du sexe...")
    
    # Mapping INSEE : 1=Homme, 2=Femme
    gender_map = {'1': 'M', '2': 'F'}
    df['sexe'] = df['SEXE'].map(gender_map)
    
    # Supprimer les valeurs manquantes
    df = df[df['sexe'].notna()].copy()
    
    print(f"  - Repartition par sexe :")
    for sex in ['M', 'F']:
        count = (df['sexe'] == sex).sum()
        pct = count / len(df) * 100
        print(f"    {sex} : {count:6,} ({pct:5.1f}%)")
    
    return df


def map_csp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mappe les catégories socio-professionnelles à partir de TACT.
    
    Simplification en 3 catégories basées sur le type d'activité :
    1 = Actifs occupés (emploi)
    2 = Étudiants, apprentis
    3 = Retraités, autres inactifs
    
    Args:
        df: DataFrame
    
    Returns:
        DataFrame avec colonne csp
    """
    print("\nMapping des CSP (basé sur TACT - type d'activité)...")
    
    # TACT : 11=Actifs occupés, 12=Chômeurs, 21=Retraités, 22=Élèves/étudiants, 23=Autres inactifs
    df['tact_num'] = pd.to_numeric(df['TACT'], errors='coerce')
    
    # Mapping simplifié basé sur l'activité
    def map_csp_from_tact(tact):
        if pd.isna(tact):
            return None
        tact_str = str(int(tact))
        if tact_str == '11':  # Actifs occupés
            return 1
        elif tact_str in ['12', '22']:  # Chômeurs, Étudiants
            return 2
        elif tact_str in ['21', '23']:  # Retraités, Autres inactifs
            return 3
        else:
            return None
    
    df['csp'] = df['tact_num'].apply(map_csp_from_tact)
    
    # Supprimer les valeurs manquantes
    initial_count = len(df)
    df = df[df['csp'].notna()].copy()
    
    print(f"  - {len(df):,} individus avec CSP valide ({len(df)/initial_count*100:.1f}%)")
    print(f"  - Repartition par CSP :")
    csp_labels = {1: 'Actifs occupés', 2: 'Étudiants/Chômeurs', 3: 'Retraités/Inactifs'}
    for csp_code, label in csp_labels.items():
        count = (df['csp'] == csp_code).sum()
        pct = count / len(df) * 100 if len(df) > 0 else 0
        print(f"    {csp_code} - {label:20s} : {count:6,} ({pct:5.1f}%)")
    
    return df


def create_margins(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée le tableau de marges.
    
    Args:
        df: DataFrame préparé
    
    Returns:
        DataFrame des marges
    """
    print("\nCreation des marges...")
    
    # Grouper par IRIS, âge, sexe, CSP
    margins = df.groupby(['code_iris', 'age_group', 'sexe', 'csp']).size().reset_index(name='population')
    
    print(f"  - {len(margins)} combinaisons IRIS x age x sexe x CSP")
    print(f"  - Population totale : {margins['population'].sum():,}")
    
    # Statistiques
    print(f"\nStatistiques des marges :")
    print(f"  - Population min par cellule : {margins['population'].min()}")
    print(f"  - Population max par cellule : {margins['population'].max()}")
    print(f"  - Population moyenne par cellule : {margins['population'].mean():.1f}")
    
    return margins


def save_margins(margins: pd.DataFrame, output_path: Path):
    """
    Sauvegarde les marges.
    
    Args:
        margins: DataFrame des marges
        output_path: Chemin de sortie
    """
    print(f"\nSauvegarde des marges : {output_path}")
    
    # Créer le répertoire si nécessaire
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Sauvegarder
    margins.to_csv(output_path, index=False)
    
    print(f"  [OK] Fichier sauvegarde : {len(margins)} lignes")


def main():
    """Fonction principale."""
    print("=" * 70)
    print("PREPARATION DES MARGES DEPUIS LE RECENSEMENT INSEE 2022")
    print("=" * 70)
    
    try:
        # 1. Charger les données
        df = load_census_data(CENSUS_FILE)
        
        # Afficher les colonnes disponibles
        print(f"\nColonnes disponibles : {list(df.columns)}")
        
        # 2. Filtrer sur les IRIS centre-ville
        df_center = filter_center_iris(df, IRIS_CENTER)
        
        # 3. Créer les tranches d'âge
        df_center = create_age_groups(df_center)
        
        # 4. Mapper le sexe
        df_center = map_gender(df_center)
        
        # 5. Mapper les CSP
        df_center = map_csp(df_center)
        
        # 6. Créer les marges
        margins = create_margins(df_center)
        
        # 7. Sauvegarder
        save_margins(margins, OUTPUT_FILE)
        
        # Résumé final
        print("\n" + "=" * 70)
        print("SUCCES !")
        print("=" * 70)
        print(f"Fichier de marges cree : {OUTPUT_FILE}")
        print(f"Population totale centre-ville : {margins['population'].sum():,} adultes")
        print(f"Nombre d'IRIS : {margins['code_iris'].nunique()}")
        print(f"Nombre de cellules : {len(margins)}")
        print("\nVous pouvez maintenant utiliser ce fichier pour le redressement BOB.")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

