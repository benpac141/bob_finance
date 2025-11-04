"""
Simulateur de budget interactif avec ajustement du nombre d'adhérents cible.

Fonctionnalités :
- Définir un nombre d'adhérents cible
- Redistribution automatique par profil (âge, sexe, CSP)
- Calcul des recettes selon les comportements par profil
- Export Excel avec tableaux de bord
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
from datetime import datetime

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


def analyze_profile_behaviors(df):
    """
    Analyse les comportements par profil selon l'enquête.
    
    Returns:
        DataFrame avec les comportements moyens par profil
    """
    csp_labels = {1: 'Actifs', 2: 'Etudiants/Chomeurs', 3: 'Retraites/Inactifs'}
    df['csp_label'] = df['csp'].map(csp_labels)
    
    behaviors = []
    
    for age in sorted(df['age_group'].unique()):
        for sexe in ['F', 'M']:
            for csp_label in ['Actifs', 'Etudiants/Chomeurs', 'Retraites/Inactifs']:
                df_profil = df[(df['age_group'] == age) & 
                              (df['sexe'] == sexe) & 
                              (df['csp_label'] == csp_label)]
                
                if len(df_profil) > 0:
                    # % Intérêt
                    pct_interet = (df_profil['interet_projet'] == 'Oui').sum() / len(df_profil) * 100
                    
                    # % Acceptation cotisation
                    pct_cotisation = (df_profil['accepte_cotisation'].str.contains('Oui', na=False)).sum() / len(df_profil) * 100
                    
                    # Montant cotisation préféré (extraire de la réponse)
                    cotisation_pref = extract_cotisation_preference(df_profil)
                    
                    # Prix max location
                    prix_max = extract_prix_max(df_profil)
                    
                    # Déjà utilisé services (proxy pour fréquence d'usage)
                    deja_utilise = (df_profil['deja_utilise_services'].str.contains('Oui', na=False)).sum() / len(df_profil) * 100
                    
                else:
                    # Valeurs par défaut (moyenne globale)
                    pct_interet = (df['interet_projet'] == 'Oui').sum() / len(df) * 100
                    pct_cotisation = (df['accepte_cotisation'].str.contains('Oui', na=False)).sum() / len(df) * 100
                    cotisation_pref = 15
                    prix_max = 8
                    deja_utilise = 50
                
                sexe_label = 'F' if sexe == 'F' else 'M'
                
                behaviors.append({
                    'age_group': age,
                    'sexe': sexe_label,
                    'csp': csp_label,
                    'profil': f'{age}_{sexe_label}_{csp_label}',
                    'pct_interet': pct_interet,
                    'pct_cotisation': pct_cotisation,
                    'cotisation_preferee': cotisation_pref,
                    'prix_max_location': prix_max,
                    'pct_deja_utilise': deja_utilise,
                    'n_repondants': len(df_profil)
                })
    
    return pd.DataFrame(behaviors)


def extract_cotisation_preference(df_profil):
    """Extrait le montant de cotisation préféré."""
    cotisation_col = df_profil['accepte_cotisation']
    
    # Mapping des réponses vers montants
    montants = []
    for val in cotisation_col.dropna():
        if '1' in str(val) and '10' in str(val):
            montants.append(5)  # Milieu de 1-10€
        elif '10' in str(val) and '20' in str(val):
            montants.append(15)  # Milieu de 10-20€
        elif '20' in str(val) and '30' in str(val):
            montants.append(25)  # Milieu de 20-30€
        elif 'Non' in str(val):
            montants.append(0)
    
    return np.mean(montants) if montants else 15


def extract_prix_max(df_profil):
    """Extrait le prix max de location."""
    prix_col = df_profil['prix_max_location']
    
    montants = []
    for val in prix_col.dropna():
        val_str = str(val).replace('€', '').strip()
        try:
            montants.append(float(val_str))
        except:
            if '5' in val_str:
                montants.append(5)
            elif '10' in val_str:
                montants.append(10)
            elif '15' in val_str:
                montants.append(15)
            elif '20' in val_str:
                montants.append(20)
    
    return np.mean(montants) if montants else 8


def estimate_usage_frequency(pct_deja_utilise, age_group, csp):
    """
    Estime la fréquence d'usage (nb locations/an) selon le profil.
    
    Logique :
    - Si déjà utilisé → plus de locations
    - Jeunes → plus de locations
    - Actifs → plus de locations
    """
    base_frequency = 10  # Base : 10 locations/an
    
    # Ajustement selon expérience
    if pct_deja_utilise > 50:
        freq_factor = 1.3
    elif pct_deja_utilise > 30:
        freq_factor = 1.1
    else:
        freq_factor = 0.9
    
    # Ajustement selon âge
    if age_group in ['18-24', '25-34']:
        age_factor = 1.2
    elif age_group in ['35-44', '45-54']:
        age_factor = 1.0
    else:
        age_factor = 0.8
    
    # Ajustement selon CSP
    if csp == 'Actifs':
        csp_factor = 1.1
    elif csp == 'Etudiants/Chomeurs':
        csp_factor = 0.9
    else:
        csp_factor = 0.7
    
    return int(base_frequency * freq_factor * age_factor * csp_factor)


def distribute_adherents_by_profile(nb_adherents_cible, df_behaviors, margins):
    """
    Distribue le nombre d'adhérents cible selon les profils.
    
    Logique :
    1. Pondération par intérêt du profil
    2. Pondération par population du profil
    3. Normalisation pour atteindre la cible
    
    Args:
        nb_adherents_cible: Nombre d'adhérents souhaité
        df_behaviors: DataFrame avec les comportements par profil
        margins: DataFrame avec les marges INSEE
    
    Returns:
        DataFrame avec la distribution des adhérents par profil
    """
    df_dist = df_behaviors.copy()
    
    # Ajouter la population par profil
    df_dist['population'] = df_dist.apply(
        lambda row: margins[
            (margins['age_group'] == row['age_group']) & 
            (margins['sexe'] == row['sexe']) & 
            (margins['csp'] == {'Actifs': 1, 'Etudiants/Chomeurs': 2, 'Retraites/Inactifs': 3}[row['csp']])
        ]['population'].sum(),
        axis=1
    )
    
    # Calculer le score d'attractivité (intérêt × population)
    df_dist['score_attractivite'] = df_dist['pct_interet'] * df_dist['population']
    
    # Normaliser pour obtenir la distribution
    total_score = df_dist['score_attractivite'].sum()
    df_dist['pct_distribution'] = (df_dist['score_attractivite'] / total_score) * 100
    
    # Calculer le nombre d'adhérents par profil
    df_dist['nb_adherents'] = (df_dist['pct_distribution'] / 100) * nb_adherents_cible
    df_dist['nb_adherents'] = df_dist['nb_adherents'].round().astype(int)
    
    # Ajuster pour atteindre exactement la cible (arrondi)
    diff = nb_adherents_cible - df_dist['nb_adherents'].sum()
    if diff != 0:
        # Ajuster sur le profil le plus attractif
        idx_max = df_dist['score_attractivite'].idxmax()
        df_dist.loc[idx_max, 'nb_adherents'] += diff
    
    return df_dist


def calculate_recettes_by_profile(df_dist):
    """
    Calcule les recettes par profil selon les comportements.
    
    Args:
        df_dist: DataFrame avec la distribution des adhérents
    
    Returns:
        DataFrame enrichi avec les recettes
    """
    df_rev = df_dist.copy()
    
    # Estimer la fréquence d'usage par profil
    df_rev['nb_locations_an'] = df_rev.apply(
        lambda row: estimate_usage_frequency(
            row['pct_deja_utilise'],
            row['age_group'],
            row['csp']
        ),
        axis=1
    )
    
    # Recettes cotisations (selon préférence du profil)
    df_rev['recettes_cotisations'] = df_rev['nb_adherents'] * df_rev['cotisation_preferee']
    
    # Recettes locations (selon prix max accepté et fréquence)
    df_rev['recettes_locations'] = (
        df_rev['nb_adherents'] * 
        df_rev['nb_locations_an'] * 
        df_rev['prix_max_location'] * 0.8  # 80% du prix max en moyenne
    )
    
    # Recettes totales
    df_rev['recettes_totales'] = df_rev['recettes_cotisations'] + df_rev['recettes_locations']
    
    return df_rev


def generate_simulation(nb_adherents_cible, df_behaviors, margins, scenario_name="Simulation"):
    """
    Génère une simulation complète.
    
    Args:
        nb_adherents_cible: Nombre d'adhérents souhaité
        df_behaviors: DataFrame avec les comportements
        margins: DataFrame avec les marges INSEE
        scenario_name: Nom du scénario
    
    Returns:
        DataFrame avec tous les détails
    """
    # 1. Distribuer les adhérents
    df_dist = distribute_adherents_by_profile(nb_adherents_cible, df_behaviors, margins)
    
    # 2. Calculer les recettes
    df_result = calculate_recettes_by_profile(df_dist)
    
    # 3. Ajouter des métriques
    df_result['scenario'] = scenario_name
    
    return df_result


def print_simulation_summary(df_result, scenario_name):
    """Affiche le résumé d'une simulation."""
    print(f"\n{'='*70}")
    print(f"SCENARIO : {scenario_name.upper()}")
    print(f"{'='*70}")
    
    # Totaux
    total_adherents = df_result['nb_adherents'].sum()
    total_cotisations = df_result['recettes_cotisations'].sum()
    total_locations = df_result['recettes_locations'].sum()
    total_recettes = df_result['recettes_totales'].sum()
    
    # Moyennes
    cotisation_moy = df_result['cotisation_preferee'].mean()
    locations_moy = df_result['nb_locations_an'].mean()
    prix_moy = df_result['prix_max_location'].mean()
    
    print(f"\nOBJECTIF : {total_adherents:,} adherents")
    
    print(f"\nRECETTES ANNUELLES :")
    print(f"  - Cotisations : {total_cotisations:,.0f} EUR")
    print(f"  - Locations   : {total_locations:,.0f} EUR")
    print(f"  - TOTAL       : {total_recettes:,.0f} EUR")
    
    print(f"\nMOYENNES PAR ADHERENT :")
    print(f"  - Cotisation : {cotisation_moy:.1f} EUR/an")
    print(f"  - Locations  : {locations_moy:.1f} locations/an")
    print(f"  - Prix moyen : {prix_moy:.1f} EUR/location")
    print(f"  - Recette/adherent : {total_recettes/total_adherents:.0f} EUR/an")
    
    # Distribution par âge
    print(f"\nDISTRIBUTION PAR AGE :")
    age_dist = df_result.groupby('age_group')['nb_adherents'].sum().sort_values(ascending=False)
    for age, nb in age_dist.items():
        pct = nb / total_adherents * 100
        print(f"  - {age:10s} : {nb:4d} adherents ({pct:5.1f}%)")
    
    # Distribution par sexe
    print(f"\nDISTRIBUTION PAR SEXE :")
    sexe_dist = df_result.groupby('sexe')['nb_adherents'].sum()
    for sexe, nb in sexe_dist.items():
        pct = nb / total_adherents * 100
        sexe_label = 'Femmes' if sexe == 'F' else 'Hommes'
        print(f"  - {sexe_label:10s} : {nb:4d} adherents ({pct:5.1f}%)")
    
    # Distribution par CSP
    print(f"\nDISTRIBUTION PAR CSP :")
    csp_dist = df_result.groupby('csp')['nb_adherents'].sum().sort_values(ascending=False)
    for csp, nb in csp_dist.items():
        pct = nb / total_adherents * 100
        print(f"  - {csp:20s} : {nb:4d} adherents ({pct:5.1f}%)")
    
    # Top 5 profils
    print(f"\nTop 5 profils contributeurs (recettes) :")
    top5 = df_result.nlargest(5, 'recettes_totales')
    for i, (_, row) in enumerate(top5.iterrows(), 1):
        print(f"  {i}. {row['profil']:40s} : {row['recettes_totales']:8,.0f} EUR "
              f"({row['nb_adherents']:4d} adherents)")


def export_simulation_excel(simulations, output_path):
    """Exporte les simulations dans Excel."""
    print(f"\nExport vers Excel : {output_path}")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Feuille de synthèse
        summary_data = []
        for scenario_name, df_result in simulations.items():
            summary_data.append({
                'Scenario': scenario_name,
                'Nb_Adherents': int(df_result['nb_adherents'].sum()),
                'Cotisation_Moyenne_EUR': df_result['cotisation_preferee'].mean(),
                'Locations_Moyenne_An': df_result['nb_locations_an'].mean(),
                'Prix_Moyen_EUR': df_result['prix_max_location'].mean(),
                'Recettes_Cotisations_EUR': int(df_result['recettes_cotisations'].sum()),
                'Recettes_Locations_EUR': int(df_result['recettes_locations'].sum()),
                'Recettes_Totales_EUR': int(df_result['recettes_totales'].sum()),
                'Recette_Par_Adherent_EUR': int(df_result['recettes_totales'].sum() / df_result['nb_adherents'].sum())
            })
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Synthese', index=False)
        
        # Une feuille par simulation
        for scenario_name, df_result in simulations.items():
            df_export = df_result[[
                'profil', 'age_group', 'sexe', 'csp',
                'population', 'pct_interet', 'pct_distribution',
                'nb_adherents', 'cotisation_preferee', 'nb_locations_an',
                'prix_max_location', 'recettes_cotisations', 'recettes_locations', 'recettes_totales'
            ]].copy()
            
            df_export.columns = [
                'Profil', 'Age', 'Sexe', 'CSP',
                'Population', 'Interet_%', 'Distribution_%',
                'Nb_Adherents', 'Cotisation_EUR', 'Locations_An',
                'Prix_Moyen_EUR', 'Recettes_Cotisations_EUR', 'Recettes_Locations_EUR', 'Recettes_Totales_EUR'
            ]
            
            # Ajouter les totaux
            totals = pd.DataFrame([{
                'Profil': 'TOTAL',
                'Age': '',
                'Sexe': '',
                'CSP': '',
                'Population': df_export['Population'].sum(),
                'Interet_%': '',
                'Distribution_%': 100.0,
                'Nb_Adherents': df_export['Nb_Adherents'].sum(),
                'Cotisation_EUR': df_export['Cotisation_EUR'].mean(),
                'Locations_An': df_export['Locations_An'].mean(),
                'Prix_Moyen_EUR': df_export['Prix_Moyen_EUR'].mean(),
                'Recettes_Cotisations_EUR': df_export['Recettes_Cotisations_EUR'].sum(),
                'Recettes_Locations_EUR': df_export['Recettes_Locations_EUR'].sum(),
                'Recettes_Totales_EUR': df_export['Recettes_Totales_EUR'].sum()
            }])
            
            df_export = pd.concat([df_export, totals], ignore_index=True)
            
            df_export.to_excel(writer, sheet_name=scenario_name[:31], index=False)
    
    print(f"  [OK] Fichier Excel cree avec {len(simulations)} simulations")


def main():
    """Fonction principale."""
    print("="*70)
    print("SIMULATEUR DE BUDGET INTERACTIF")
    print("="*70)
    
    try:
        # 1. Charger les données
        print("\nChargement des donnees...")
        df, margins = load_data()
        
        # 2. Analyser les comportements par profil
        print("Analyse des comportements par profil...")
        df_behaviors = analyze_profile_behaviors(df)
        
        print(f"  - {len(df_behaviors)} profils analyses")
        print(f"  - Cotisation moyenne preferee : {df_behaviors['cotisation_preferee'].mean():.1f} EUR")
        print(f"  - Prix max moyen : {df_behaviors['prix_max_location'].mean():.1f} EUR")
        
        # 3. Générer plusieurs simulations avec différents objectifs
        print("\nGeneration des simulations...")
        
        simulations = {}
        
        # Simulation 1 : 500 adhérents (Année 1)
        simulations['500_adherents_An1'] = generate_simulation(
            500, df_behaviors, margins, "500 adherents (Annee 1)"
        )
        
        # Simulation 2 : 1000 adhérents (Année 2)
        simulations['1000_adherents_An2'] = generate_simulation(
            1000, df_behaviors, margins, "1000 adherents (Annee 2)"
        )
        
        # Simulation 3 : 1500 adhérents (Année 3)
        simulations['1500_adherents_An3'] = generate_simulation(
            1500, df_behaviors, margins, "1500 adherents (Annee 3)"
        )
        
        # Simulation 4 : 2000 adhérents (Objectif long terme)
        simulations['2000_adherents_LT'] = generate_simulation(
            2000, df_behaviors, margins, "2000 adherents (Long terme)"
        )
        
        # 4. Afficher les résumés
        for scenario_name, df_result in simulations.items():
            print_simulation_summary(df_result, scenario_name)
        
        # 5. Exporter vers Excel
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        output_excel = OUTPUT_DIR / f'budget_interactif_{timestamp}.xlsx'
        export_simulation_excel(simulations, output_excel)
        
        # Résumé final
        print(f"\n{'='*70}")
        print("SUCCES !")
        print(f"{'='*70}")
        print(f"\nFichier genere : {output_excel}")
        print(f"\nContenu :")
        print(f"  - Onglet 'Synthese' : Comparaison des 4 simulations")
        print(f"  - 4 onglets detailles : Distribution par profil")
        print(f"\nPour chaque simulation :")
        print(f"  - Nombre d'adherents par profil (age, sexe, CSP)")
        print(f"  - Cotisation preferee par profil")
        print(f"  - Nombre de locations/an par profil")
        print(f"  - Prix moyen par profil")
        print(f"  - Recettes detailles (cotisations + locations)")
        
        print(f"\n{'='*70}")
        print("POUR CREER VOS PROPRES SIMULATIONS :")
        print(f"{'='*70}")
        print("Modifiez le script et ajoutez :")
        print("  simulations['mon_objectif'] = generate_simulation(")
        print("      1200,  # Votre objectif d'adherents")
        print("      df_behaviors, margins, 'Mon scenario'")
        print("  )")
        print(f"{'='*70}")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

