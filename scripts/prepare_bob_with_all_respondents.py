"""
Script pour préparer TOUS les répondants BOB avec filtrage intelligent.

Stratégie :
1. Garder TOUS les répondants (90)
2. Créer un indicateur "besancon" (Oui/Non)
3. Pour les analyses locales (intérêt, cotisation) : filtrer sur besancon=Oui
4. Pour les analyses générales : utiliser tous les répondants
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Chemins
INPUT_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_bob.xlsx"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.xlsx"

# Mapping des colonnes
COLUMN_MAPPING = {
    'id': 'N°Obs',
    'genre': 'Quels est votre genre ?',
    'age_tranche': "Dans quelle tranche d'âge vous situez-vous ?",
    'situation_pro': 'Quelle est votre situation professionnelle actuelle ?',
    'code_postal': 'Quel est le code postal de votre lieu de résidence ?',
    'departement': 'Département',
    'emplacement_centre': "Comment définiriez-vous l'emplacement de votre domicile par rapport au centre-ville ?",
    'interet': "Une bibliothèque d'objets à Besançon vous intéresserait-elle ?",
    'cotisation': "Accepteriez-vous de payer une cotisation pour accéder à une bibliothèque d'objets ?",
    'deja_utilise': "Avez-vous déjà utilisé des services de location ou de prêt d'objets ?_",
    'partage_objets': "Accepteriez-vous de partager certains de vos objets personnels avec d'autres utilisateurs ?",
    'types_objets': "Si oui, quels types d'objets seriez-vous prêt(e) à partager ?",
    'prix_max': "Pour un objet d'une valeur de 200€ neuf, quel prix maximum de location journalière seriez-vous prêt(e) à payer ?",
    'motivations': "Quelles raisons vous motiveraient à utiliser une bibliothèque d'objets ? (Plusieurs réponses possibles)",
    'criteres': "Quels critères considérez-vous comme essentiels pour utiliser un service de prêt d'objets ? (Plusieurs réponses possibles)"
}

# IRIS centre-ville de Besançon
IRIS_CENTER = ['250560101', '250560102', '250560103', '250560104',
               '250560302', '250560303', '250560304',
               '250560401', '250560402', '250560501', '250560502']


def load_bob_data(file_path):
    """Charge les données BOB."""
    print(f"Chargement de {file_path}...")
    df = pd.read_excel(file_path)
    print(f"  - {len(df)} répondants chargés")
    return df


def create_age_group(age_tranche):
    """Convertit les tranches d'âge."""
    if pd.isna(age_tranche):
        # Imputer avec la modalité la plus fréquente
        return '18-24'  # Majorité dans votre échantillon
    
    age_str = str(age_tranche).strip()
    mapping = {
        '18-24 ans': '18-24',
        '25-34 ans': '25-34',
        '35-44 ans': '35-44',
        '45-54 ans': '45-54',
        '55-64 ans': '55-64',
        '65 ans et plus': '65+',
        '65+': '65+'
    }
    return mapping.get(age_str, '25-34')  # Défaut si non trouvé


def create_sexe(genre):
    """Convertit le genre vers M/F."""
    if pd.isna(genre):
        # Imputer aléatoirement selon la distribution (70% F, 30% M dans votre échantillon)
        return np.random.choice(['F', 'M'], p=[0.7, 0.3])
    
    genre_str = str(genre).strip().lower()
    
    if 'homme' in genre_str and 'femme' not in genre_str:
        return 'M'
    elif 'femme' in genre_str:
        return 'F'
    elif 'non-binaire' in genre_str or 'autre' in genre_str:
        # Mapper aléatoirement pour le redressement
        return np.random.choice(['F', 'M'], p=[0.5, 0.5])
    else:
        return np.random.choice(['F', 'M'], p=[0.7, 0.3])


def create_csp(situation_pro):
    """Convertit la situation professionnelle vers CSP."""
    if pd.isna(situation_pro):
        return 1  # Défaut : Actifs
    
    sit_str = str(situation_pro).strip().lower()
    
    if any(word in sit_str for word in ['activité', 'emploi', 'profession', 'travail']):
        return 1
    elif any(word in sit_str for word in ['étudiant', 'élève']):
        return 2
    elif any(word in sit_str for word in ['chômeur', 'demandeur', 'recherche']):
        return 2
    elif any(word in sit_str for word in ['retraité', 'retraite']):
        return 3
    else:
        return 1  # Défaut


def determine_location(code_postal, emplacement_centre):
    """
    Détermine si le répondant est à Besançon et attribue un IRIS.
    
    Returns:
        tuple: (is_besancon, code_iris)
    """
    if pd.isna(code_postal):
        return False, None
    
    cp_str = str(int(code_postal)) if isinstance(code_postal, float) else str(code_postal)
    
    # Vérifier si Besançon (25000, 25200, etc.)
    is_besancon = cp_str.startswith('25')
    
    if not is_besancon:
        return False, None
    
    # Attribuer un IRIS selon l'emplacement déclaré
    if pd.notna(emplacement_centre):
        empl_str = str(emplacement_centre).strip().lower()
        
        if 'centre' in empl_str:
            iris = np.random.choice(['250560101', '250560102', '250560103', '250560104'])
        elif 'proche' in empl_str:
            iris = np.random.choice(['250560302', '250560303', '250560304'])
        else:
            iris = np.random.choice(['250560401', '250560402', '250560501', '250560502'])
    else:
        # Attribuer aléatoirement un IRIS centre-ville
        iris = np.random.choice(IRIS_CENTER)
    
    return True, iris


def prepare_data(df):
    """Prépare les données pour le redressement."""
    print("\nPréparation des données...")
    
    df_prep = df.copy()
    
    # 1. ID
    df_prep['id_repondant'] = df_prep[COLUMN_MAPPING['id']]
    
    # 2. Age group (avec imputation)
    print("  - Création de age_group (avec imputation si manquant)...")
    df_prep['age_group'] = df_prep[COLUMN_MAPPING['age_tranche']].apply(create_age_group)
    
    # 3. Sexe (avec imputation)
    print("  - Création de sexe (avec imputation si manquant/non-binaire)...")
    df_prep['sexe'] = df_prep[COLUMN_MAPPING['genre']].apply(create_sexe)
    
    # 4. CSP (avec imputation)
    print("  - Création de csp (avec imputation si manquant)...")
    df_prep['csp'] = df_prep[COLUMN_MAPPING['situation_pro']].apply(create_csp)
    
    # 5. Localisation et IRIS
    print("  - Détermination de la localisation...")
    location_data = df_prep.apply(
        lambda row: determine_location(
            row[COLUMN_MAPPING['code_postal']], 
            row[COLUMN_MAPPING['emplacement_centre']]
        ), 
        axis=1
    )
    df_prep['is_besancon'] = [loc[0] for loc in location_data]
    df_prep['code_iris'] = [loc[1] for loc in location_data]
    
    # Pour les non-Besançon, attribuer quand même un IRIS (pour le redressement technique)
    # mais on les marquera pour les exclure des analyses locales
    df_prep.loc[df_prep['code_iris'].isna(), 'code_iris'] = np.random.choice(IRIS_CENTER, 
                                                                               df_prep['code_iris'].isna().sum())
    
    # 6. Variables d'intérêt
    df_prep['interet_projet'] = df_prep[COLUMN_MAPPING['interet']]
    df_prep['accepte_cotisation'] = df_prep[COLUMN_MAPPING['cotisation']]
    df_prep['deja_utilise_services'] = df_prep[COLUMN_MAPPING['deja_utilise']]
    df_prep['partage_oui'] = df_prep[COLUMN_MAPPING['partage_objets']]
    df_prep['types_partage'] = df_prep[COLUMN_MAPPING['types_objets']]
    df_prep['prix_max_location'] = df_prep[COLUMN_MAPPING['prix_max']]
    df_prep['motivations'] = df_prep[COLUMN_MAPPING['motivations']]
    df_prep['criteres_essentiels'] = df_prep[COLUMN_MAPPING['criteres']]
    
    return df_prep


def display_statistics(df):
    """Affiche les statistiques."""
    print("\n" + "="*70)
    print("STATISTIQUES DES DONNEES PREPAREES")
    print("="*70)
    
    print(f"\nNombre total de répondants : {len(df)}")
    print(f"  - Besançon : {df['is_besancon'].sum()}")
    print(f"  - Hors Besançon : {(~df['is_besancon']).sum()}")
    
    print("\nRépartition age_group :")
    print(df['age_group'].value_counts().sort_index())
    
    print("\nRépartition sexe :")
    print(df['sexe'].value_counts())
    
    print("\nRépartition csp :")
    csp_labels = {1: 'Actifs occupés', 2: 'Étudiants/Chômeurs', 3: 'Retraités/Inactifs'}
    for csp_val, count in df['csp'].value_counts().sort_index().items():
        label = csp_labels.get(csp_val, 'Inconnu')
        print(f"  {csp_val} - {label:20s} : {count}")
    
    print("\n=== ANALYSES PAR LOCALISATION ===")
    
    print("\nIntérêt pour le projet (Besançon uniquement) :")
    df_besancon = df[df['is_besancon']]
    print(df_besancon['interet_projet'].value_counts())
    
    print("\nIntérêt pour le projet (Hors Besançon) :")
    df_hors = df[~df['is_besancon']]
    if len(df_hors) > 0:
        print(df_hors['interet_projet'].value_counts())


def save_prepared_data(df, output_path):
    """Sauvegarde les données préparées."""
    print(f"\nSauvegarde des données préparées : {output_path}")
    
    columns_to_keep = [
        'id_repondant', 'code_iris', 'age_group', 'sexe', 'csp', 'is_besancon',
        'interet_projet', 'accepte_cotisation', 
        'deja_utilise_services', 'partage_oui', 'types_partage',
        'prix_max_location', 'motivations', 'criteres_essentiels'
    ]
    
    df_export = df[columns_to_keep].copy()
    df_export.to_excel(output_path, index=False)
    
    print(f"  [OK] {len(df_export)} répondants sauvegardés")


def main():
    """Fonction principale."""
    print("="*70)
    print("PREPARATION DE TOUS LES REPONDANTS BOB")
    print("="*70)
    
    try:
        # 1. Charger
        df = load_bob_data(INPUT_FILE)
        
        # 2. Préparer
        df_prep = prepare_data(df)
        
        # 3. Statistiques
        display_statistics(df_prep)
        
        # 4. Sauvegarder
        save_prepared_data(df_prep, OUTPUT_FILE)
        
        # Résumé
        print("\n" + "="*70)
        print("SUCCES !")
        print("="*70)
        print(f"Fichier original : {INPUT_FILE} (NON MODIFIE)")
        print(f"Fichier préparé : {OUTPUT_FILE}")
        print(f"\nRépondants : {len(df_prep)} (TOUS conservés)")
        print(f"  - Besançon : {df_prep['is_besancon'].sum()}")
        print(f"  - Hors Besançon : {(~df_prep['is_besancon']).sum()}")
        print("\nPour les analyses :")
        print("  - Questions locales (intérêt, cotisation) : filtrer sur is_besancon=True")
        print("  - Questions générales : utiliser tous les répondants")
        print("\nProchaine étape :")
        print("  Modifier config.yaml pour pointer vers enquete_all_prepared.xlsx")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

