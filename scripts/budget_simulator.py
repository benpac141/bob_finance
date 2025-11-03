"""
Simulateur de budget prévisionnel pour la bibliothèque d'objets.

Calcule les revenus potentiels (cotisations + locations) par profil
en fonction de paramètres variables.
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


def calculate_potential_by_profile(df, margins):
    """
    Calcule le potentiel (nombre d'intéressés) par profil.
    
    Returns:
        DataFrame avec colonnes: profil, age_group, sexe, csp, population, pct_interet, nb_interesses
    """
    csp_labels = {1: 'Actifs', 2: 'Etudiants/Chomeurs', 3: 'Retraites/Inactifs'}
    
    potentials = []
    
    for age in sorted(df['age_group'].unique()):
        for sexe in ['F', 'M']:
            for csp in [1, 2, 3]:
                # Filtrer les répondants de ce profil
                df_profil = df[(df['age_group'] == age) & 
                              (df['sexe'] == sexe) & 
                              (df['csp'] == csp)]
                
                # Calculer le % d'intérêt
                if len(df_profil) > 0:
                    pct_interet = (df_profil['interet_projet'] == 'Oui').sum() / len(df_profil) * 100
                    pct_cotisation = (df_profil['accepte_cotisation'].str.contains('Oui', na=False)).sum() / len(df_profil) * 100
                else:
                    # Utiliser la moyenne globale
                    pct_interet = (df['interet_projet'] == 'Oui').sum() / len(df) * 100
                    pct_cotisation = (df['accepte_cotisation'].str.contains('Oui', na=False)).sum() / len(df) * 100
                
                # Population INSEE de ce profil
                pop_profil = margins[(margins['age_group'] == age) & 
                                    (margins['sexe'] == sexe) & 
                                    (margins['csp'] == csp)]['population'].sum()
                
                # Nombre d'intéressés
                nb_interesses = pop_profil * (pct_interet / 100)
                nb_accepte_cotisation = pop_profil * (pct_cotisation / 100)
                
                sexe_label = 'F' if sexe == 'F' else 'M'
                csp_label = csp_labels[csp]
                
                potentials.append({
                    'profil': f'{age}_{sexe_label}_{csp_label}',
                    'age_group': age,
                    'sexe': sexe_label,
                    'csp': csp_label,
                    'population': pop_profil,
                    'pct_interet': pct_interet,
                    'nb_interesses': nb_interesses,
                    'pct_cotisation': pct_cotisation,
                    'nb_accepte_cotisation': nb_accepte_cotisation
                })
    
    return pd.DataFrame(potentials).sort_values('nb_interesses', ascending=False)


def simulate_budget(df_potential, params):
    """
    Simule le budget avec des paramètres variables.
    
    Args:
        df_potential: DataFrame avec le potentiel par profil
        params: Dict avec les paramètres de simulation
            - taux_conversion: % d'intéressés qui deviennent adhérents
            - cotisation_annuelle: Montant de la cotisation (€)
            - nb_locations_an: Nombre moyen de locations par adhérent par an
            - prix_location_moyen: Prix moyen d'une location (€)
            - taux_cotisation_par_profil: Dict optionnel {profil: taux}
    
    Returns:
        DataFrame avec les revenus par profil
    """
    df_budget = df_potential.copy()
    
    # Paramètres par défaut
    taux_conversion = params.get('taux_conversion', 5)  # 5% par défaut
    cotisation_annuelle = params.get('cotisation_annuelle', 15)  # 15€ par défaut
    nb_locations_an = params.get('nb_locations_an', 10)  # 10 locations/an par défaut
    prix_location_moyen = params.get('prix_location_moyen', 8)  # 8€ par défaut
    
    # Taux de conversion variable par profil (optionnel)
    taux_conversion_profil = params.get('taux_conversion_par_profil', {})
    
    # Calculer le nombre d'adhérents
    df_budget['taux_conversion'] = df_budget['profil'].map(
        lambda p: taux_conversion_profil.get(p, taux_conversion)
    )
    df_budget['nb_adherents'] = df_budget['nb_interesses'] * (df_budget['taux_conversion'] / 100)
    
    # Revenus cotisations
    df_budget['revenus_cotisations'] = df_budget['nb_adherents'] * cotisation_annuelle
    
    # Revenus locations
    df_budget['revenus_locations'] = df_budget['nb_adherents'] * nb_locations_an * prix_location_moyen
    
    # Revenus totaux
    df_budget['revenus_totaux'] = df_budget['revenus_cotisations'] + df_budget['revenus_locations']
    
    return df_budget


def generate_scenarios(df_potential):
    """
    Génère plusieurs scénarios budgétaires.
    
    Returns:
        Dict de DataFrames (un par scénario)
    """
    scenarios = {}
    
    # Scénario 1 : Pessimiste
    scenarios['pessimiste'] = simulate_budget(df_potential, {
        'taux_conversion': 3,  # 3% d'adhésion
        'cotisation_annuelle': 10,  # 10€/an
        'nb_locations_an': 5,  # 5 locations/an
        'prix_location_moyen': 6  # 6€/location
    })
    
    # Scénario 2 : Réaliste
    scenarios['realiste'] = simulate_budget(df_potential, {
        'taux_conversion': 5,  # 5% d'adhésion
        'cotisation_annuelle': 15,  # 15€/an
        'nb_locations_an': 10,  # 10 locations/an
        'prix_location_moyen': 8  # 8€/location
    })
    
    # Scénario 3 : Optimiste
    scenarios['optimiste'] = simulate_budget(df_potential, {
        'taux_conversion': 8,  # 8% d'adhésion
        'cotisation_annuelle': 20,  # 20€/an
        'nb_locations_an': 15,  # 15 locations/an
        'prix_location_moyen': 10  # 10€/location
    })
    
    # Scénario 4 : Ciblé (taux variables par profil)
    taux_conversion_cible = {}
    for _, row in df_potential.iterrows():
        profil = row['profil']
        # Taux plus élevés pour les profils les plus intéressés
        if row['pct_interet'] > 80:
            taux_conversion_cible[profil] = 10
        elif row['pct_interet'] > 60:
            taux_conversion_cible[profil] = 7
        else:
            taux_conversion_cible[profil] = 3
    
    scenarios['cible'] = simulate_budget(df_potential, {
        'taux_conversion': 5,  # Défaut
        'cotisation_annuelle': 15,
        'nb_locations_an': 10,
        'prix_location_moyen': 8,
        'taux_conversion_par_profil': taux_conversion_cible
    })
    
    return scenarios


def print_scenario_summary(scenario_name, df_budget):
    """Affiche le résumé d'un scénario."""
    print(f"\n{'='*70}")
    print(f"SCENARIO : {scenario_name.upper()}")
    print(f"{'='*70}")
    
    # Totaux
    total_adherents = df_budget['nb_adherents'].sum()
    total_cotisations = df_budget['revenus_cotisations'].sum()
    total_locations = df_budget['revenus_locations'].sum()
    total_revenus = df_budget['revenus_totaux'].sum()
    
    print(f"\nNombre d'adherents : {total_adherents:,.0f}")
    print(f"\nREVENUS ANNUELS :")
    print(f"  - Cotisations : {total_cotisations:,.0f} EUR")
    print(f"  - Locations   : {total_locations:,.0f} EUR")
    print(f"  - TOTAL       : {total_revenus:,.0f} EUR")
    
    # Top 5 profils contributeurs
    print(f"\nTop 5 profils contributeurs (revenus totaux) :")
    top5 = df_budget.nlargest(5, 'revenus_totaux')
    for i, (_, row) in enumerate(top5.iterrows(), 1):
        print(f"  {i}. {row['profil']:40s} : {row['revenus_totaux']:8,.0f} EUR "
              f"({row['nb_adherents']:5.0f} adherents)")


def export_budget_excel(scenarios, output_path):
    """Exporte tous les scénarios dans un fichier Excel."""
    print(f"\nExport vers Excel : {output_path}")
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Feuille de synthèse
        summary_data = []
        for scenario_name, df_budget in scenarios.items():
            summary_data.append({
                'Scenario': scenario_name.capitalize(),
                'Nb_Adherents': int(df_budget['nb_adherents'].sum()),
                'Revenus_Cotisations_EUR': int(df_budget['revenus_cotisations'].sum()),
                'Revenus_Locations_EUR': int(df_budget['revenus_locations'].sum()),
                'Revenus_Totaux_EUR': int(df_budget['revenus_totaux'].sum()),
                'Taux_Conversion_Moyen_%': df_budget['taux_conversion'].mean()
            })
        
        df_summary = pd.DataFrame(summary_data)
        df_summary.to_excel(writer, sheet_name='Synthese', index=False)
        
        # Une feuille par scénario
        for scenario_name, df_budget in scenarios.items():
            df_export = df_budget[[
                'profil', 'age_group', 'sexe', 'csp',
                'population', 'pct_interet', 'nb_interesses',
                'taux_conversion', 'nb_adherents',
                'revenus_cotisations', 'revenus_locations', 'revenus_totaux'
            ]].copy()
            
            df_export.columns = [
                'Profil', 'Age', 'Sexe', 'CSP',
                'Population', 'Interet_%', 'Nb_Interesses',
                'Taux_Conversion_%', 'Nb_Adherents',
                'Revenus_Cotisations_EUR', 'Revenus_Locations_EUR', 'Revenus_Totaux_EUR'
            ]
            
            df_export.to_excel(writer, sheet_name=scenario_name.capitalize(), index=False)
    
    print(f"  [OK] Fichier Excel cree avec {len(scenarios)} scenarios")


def create_budget_template(output_path):
    """Crée un template Excel pour paramétrer les scénarios."""
    print(f"\nCreation du template de parametrage : {output_path}")
    
    # Template de paramètres
    params_data = {
        'Parametre': [
            'taux_conversion_%',
            'cotisation_annuelle_EUR',
            'nb_locations_an',
            'prix_location_moyen_EUR'
        ],
        'Pessimiste': [3, 10, 5, 6],
        'Realiste': [5, 15, 10, 8],
        'Optimiste': [8, 20, 15, 10],
        'Description': [
            '% d\'interesses qui deviennent adherents',
            'Montant de la cotisation annuelle',
            'Nombre moyen de locations par adherent par an',
            'Prix moyen d\'une location'
        ]
    }
    
    df_params = pd.DataFrame(params_data)
    
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        df_params.to_excel(writer, sheet_name='Parametres', index=False)
        
        # Instructions
        instructions = pd.DataFrame({
            'Instructions': [
                'Ce fichier permet de parametrer les scenarios budgetaires.',
                '',
                '1. Modifiez les valeurs dans les colonnes Pessimiste/Realiste/Optimiste',
                '2. Ajoutez de nouvelles colonnes pour creer d\'autres scenarios',
                '3. Relancez le script budget_simulator.py',
                '',
                'Parametres disponibles :',
                '- taux_conversion_% : Pourcentage d\'interesses qui deviennent adherents (3-10%)',
                '- cotisation_annuelle_EUR : Montant de la cotisation annuelle (10-30 EUR)',
                '- nb_locations_an : Nombre moyen de locations par adherent par an (5-20)',
                '- prix_location_moyen_EUR : Prix moyen d\'une location (5-15 EUR)',
            ]
        })
        instructions.to_excel(writer, sheet_name='Instructions', index=False)
    
    print(f"  [OK] Template cree")


def main():
    """Fonction principale."""
    print("="*70)
    print("SIMULATEUR DE BUDGET PREVISIONNEL")
    print("="*70)
    
    try:
        # 1. Charger les données
        print("\nChargement des donnees...")
        df, margins = load_data()
        
        # 2. Calculer le potentiel par profil
        print("Calcul du potentiel par profil...")
        df_potential = calculate_potential_by_profile(df, margins)
        
        print(f"  - {len(df_potential)} profils analyses")
        print(f"  - Population totale : {df_potential['population'].sum():,.0f}")
        print(f"  - Interesses estimes : {df_potential['nb_interesses'].sum():,.0f}")
        
        # 3. Générer les scénarios
        print("\nGeneration des scenarios...")
        scenarios = generate_scenarios(df_potential)
        
        # 4. Afficher les résumés
        for scenario_name, df_budget in scenarios.items():
            print_scenario_summary(scenario_name, df_budget)
        
        # 5. Exporter vers Excel
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        output_excel = OUTPUT_DIR / f'budget_previsionnel_{timestamp}.xlsx'
        export_budget_excel(scenarios, output_excel)
        
        # 6. Créer le template de paramétrage
        template_path = OUTPUT_DIR / 'budget_template_parametres.xlsx'
        create_budget_template(template_path)
        
        # Résumé final
        print(f"\n{'='*70}")
        print("SUCCES !")
        print(f"{'='*70}")
        print(f"\nFichiers generes :")
        print(f"  1. {output_excel}")
        print(f"     -> Budget previsionnel avec 4 scenarios")
        print(f"  2. {template_path}")
        print(f"     -> Template pour parametrer vos propres scenarios")
        
        print(f"\n{'='*70}")
        print("PROCHAINES ETAPES :")
        print(f"{'='*70}")
        print("1. Ouvrir le fichier Excel du budget previsionnel")
        print("2. Consulter l'onglet 'Synthese' pour comparer les scenarios")
        print("3. Consulter les onglets par scenario pour le detail par profil")
        print("4. Modifier le template de parametres pour creer vos propres scenarios")
        print(f"{'='*70}")
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

