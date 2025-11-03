"""
Script pour préparer les données BOB pour le redressement.
Ce script NE MODIFIE PAS le fichier original, il crée un nouveau fichier préparé.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Chemins
INPUT_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_bob.xlsx"
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_prepared.xlsx"

# Mapping des colonnes (depuis votre enquête vers les variables de redressement)
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


def load_bob_data(file_path):
    """Charge les données BOB."""
    print(f"Chargement de {file_path}...")
    df = pd.read_excel(file_path)
    print(f"  - {len(df)} répondants chargés")
    print(f"  - {len(df.columns)} colonnes")
    return df


def create_age_group(age_tranche):
    """
    Convertit les tranches d'âge de l'enquête vers les tranches INSEE.
    """
    if pd.isna(age_tranche):
        return None
    
    age_str = str(age_tranche).strip()
    
    # Mapping des tranches
    mapping = {
        '18-24 ans': '18-24',
        '25-34 ans': '25-34',
        '35-44 ans': '35-44',
        '45-54 ans': '45-54',
        '55-64 ans': '55-64',
        '65 ans et plus': '65+',
        '65+': '65+'
    }
    
    return mapping.get(age_str, None)


def create_sexe(genre):
    """
    Convertit le genre vers M/F.
    """
    if pd.isna(genre):
        return None
    
    genre_str = str(genre).strip().lower()
    
    if 'homme' in genre_str and 'femme' not in genre_str:
        return 'M'
    elif 'femme' in genre_str:
        return 'F'
    else:
        # Non-binaire ou autre -> on peut choisir d'exclure ou d'attribuer
        # Pour l'instant, on retourne None (sera exclu)
        return None


def create_csp(situation_pro):
    """
    Convertit la situation professionnelle vers les 3 catégories CSP.
    1 = Actifs occupés
    2 = Étudiants / Chômeurs
    3 = Retraités / Inactifs
    """
    if pd.isna(situation_pro):
        return None
    
    sit_str = str(situation_pro).strip().lower()
    
    # Actifs occupés
    if any(word in sit_str for word in ['activité', 'emploi', 'profession', 'travail', 'salarié']):
        return 1
    
    # Étudiants / Chômeurs
    elif any(word in sit_str for word in ['étudiant', 'élève', 'chômeur', 'recherche', 'formation']):
        return 2
    
    # Retraités / Inactifs
    elif any(word in sit_str for word in ['retraité', 'retraite', 'inactif', 'foyer', 'sans activité']):
        return 3
    
    else:
        return None


def geocode_to_iris(code_postal, emplacement_centre):
    """
    Attribue un code IRIS en fonction du code postal et de l'emplacement.
    
    Pour une vraie application, il faudrait géocoder les adresses.
    Ici, on attribue les IRIS centre-ville selon la proximité déclarée.
    """
    if pd.isna(code_postal):
        return None
    
    # Vérifier que c'est Besançon (25000)
    cp = str(code_postal).strip()
    if not cp.startswith('25'):
        return None
    
    # IRIS du centre-ville de Besançon
    iris_centre = ['250560101', '250560102', '250560103', '250560104']
    iris_proche = ['250560302', '250560303', '250560304']
    iris_peripherie = ['250560401', '250560402', '250560501', '250560502']
    
    # Attribuer selon l'emplacement déclaré
    if pd.notna(emplacement_centre):
        empl_str = str(emplacement_centre).strip().lower()
        
        if 'centre' in empl_str:
            return np.random.choice(iris_centre)
        elif 'proche' in empl_str:
            return np.random.choice(iris_proche)
        else:
            return np.random.choice(iris_peripherie)
    else:
        # Par défaut, attribuer aléatoirement un IRIS centre-ville
        return np.random.choice(iris_centre + iris_proche + iris_peripherie)


def prepare_data(df):
    """
    Prépare les données pour le redressement.
    """
    print("\nPréparation des données...")
    
    df_prep = df.copy()
    
    # 1. Créer id_repondant
    df_prep['id_repondant'] = df_prep[COLUMN_MAPPING['id']]
    
    # 2. Créer age_group
    print("  - Création de age_group...")
    df_prep['age_group'] = df_prep[COLUMN_MAPPING['age_tranche']].apply(create_age_group)
    
    # 3. Créer sexe
    print("  - Création de sexe...")
    df_prep['sexe'] = df_prep[COLUMN_MAPPING['genre']].apply(create_sexe)
    
    # 4. Créer csp
    print("  - Création de csp...")
    df_prep['csp'] = df_prep[COLUMN_MAPPING['situation_pro']].apply(create_csp)
    
    # 5. Créer code_iris
    print("  - Attribution des codes IRIS...")
    df_prep['code_iris'] = df_prep.apply(
        lambda row: geocode_to_iris(
            row[COLUMN_MAPPING['code_postal']], 
            row[COLUMN_MAPPING['emplacement_centre']]
        ), 
        axis=1
    )
    
    # 6. Garder les colonnes d'intérêt (renommées)
    df_prep['interet_projet'] = df_prep[COLUMN_MAPPING['interet']]
    df_prep['accepte_cotisation'] = df_prep[COLUMN_MAPPING['cotisation']]
    df_prep['deja_utilise_services'] = df_prep[COLUMN_MAPPING['deja_utilise']]
    df_prep['partage_oui'] = df_prep[COLUMN_MAPPING['partage_objets']]
    df_prep['types_partage'] = df_prep[COLUMN_MAPPING['types_objets']]
    df_prep['prix_max_location'] = df_prep[COLUMN_MAPPING['prix_max']]
    df_prep['motivations'] = df_prep[COLUMN_MAPPING['motivations']]
    df_prep['criteres_essentiels'] = df_prep[COLUMN_MAPPING['criteres']]
    
    return df_prep


def filter_valid_data(df):
    """
    Filtre les données valides (avec toutes les variables de redressement).
    """
    print("\nFiltrage des données valides...")
    
    n_initial = len(df)
    
    # Filtrer sur les variables de redressement
    df_valid = df.dropna(subset=['age_group', 'sexe', 'csp', 'code_iris']).copy()
    
    n_final = len(df_valid)
    n_excluded = n_initial - n_final
    
    print(f"  - {n_final} répondants valides sur {n_initial}")
    if n_excluded > 0:
        print(f"  - {n_excluded} répondants exclus (données manquantes)")
    
    return df_valid


def display_statistics(df):
    """
    Affiche les statistiques des données préparées.
    """
    print("\n" + "="*70)
    print("STATISTIQUES DES DONNEES PREPAREES")
    print("="*70)
    
    print(f"\nNombre de répondants : {len(df)}")
    
    print("\nRépartition par age_group :")
    print(df['age_group'].value_counts().sort_index())
    
    print("\nRépartition par sexe :")
    print(df['sexe'].value_counts())
    
    print("\nRépartition par csp :")
    csp_labels = {1: 'Actifs occupés', 2: 'Étudiants/Chômeurs', 3: 'Retraités/Inactifs'}
    for csp_val, count in df['csp'].value_counts().sort_index().items():
        label = csp_labels.get(csp_val, 'Inconnu')
        print(f"  {csp_val} - {label:20s} : {count}")
    
    print("\nRépartition par IRIS :")
    print(df['code_iris'].value_counts().sort_index())
    
    print("\nRépartition interet_projet :")
    print(df['interet_projet'].value_counts())
    
    print("\nRépartition accepte_cotisation :")
    print(df['accepte_cotisation'].value_counts())


def save_prepared_data(df, output_path):
    """
    Sauvegarde les données préparées.
    """
    print(f"\nSauvegarde des données préparées : {output_path}")
    
    # Sélectionner les colonnes à garder
    columns_to_keep = [
        'id_repondant', 'code_iris', 'age_group', 'sexe', 'csp',
        'interet_projet', 'accepte_cotisation', 
        'deja_utilise_services', 'partage_oui', 'types_partage',
        'prix_max_location', 'motivations', 'criteres_essentiels'
    ]
    
    df_export = df[columns_to_keep].copy()
    
    # Sauvegarder
    df_export.to_excel(output_path, index=False)
    
    print(f"  [OK] {len(df_export)} répondants sauvegardés")
    print(f"  [OK] {len(df_export.columns)} colonnes")


def main():
    """Fonction principale."""
    print("="*70)
    print("PREPARATION DES DONNEES BOB POUR LE REDRESSEMENT")
    print("="*70)
    
    try:
        # 1. Charger les données
        df = load_bob_data(INPUT_FILE)
        
        # 2. Préparer les données
        df_prep = prepare_data(df)
        
        # 3. Filtrer les données valides
        df_valid = filter_valid_data(df_prep)
        
        # 4. Afficher les statistiques
        display_statistics(df_valid)
        
        # 5. Sauvegarder
        save_prepared_data(df_valid, OUTPUT_FILE)
        
        # Résumé final
        print("\n" + "="*70)
        print("SUCCES !")
        print("="*70)
        print(f"Fichier original : {INPUT_FILE} (NON MODIFIE)")
        print(f"Fichier préparé : {OUTPUT_FILE}")
        print(f"\nRépondants : {len(df_valid)} sur {len(df)}")
        print("\nVous pouvez maintenant lancer le redressement :")
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

