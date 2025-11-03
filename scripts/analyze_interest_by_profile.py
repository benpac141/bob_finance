"""
Analyse de l'intérêt pour le projet par profil démographique.

Compare deux méthodes :
1. Méthode SIMPLE : % global × population totale
2. Méthode PAR PROFIL : % par profil × population du profil
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Chemins
DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.xlsx"
MARGINS_FILE = Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv"


def load_data():
    """Charge les données."""
    print("Chargement des donnees...")
    df = pd.read_excel(DATA_FILE)
    margins = pd.read_csv(MARGINS_FILE)
    
    # Filtrer Besançon uniquement
    df_besancon = df[df['is_besancon']].copy()
    
    print(f"  - {len(df_besancon)} repondants Besancon")
    print(f"  - Population totale (marges) : {margins['population'].sum():,}")
    
    return df_besancon, margins


def analyze_interest_by_variable(df, variable, var_label):
    """Analyse l'intérêt par une variable."""
    print(f"\n{'='*70}")
    print(f"INTERET PAR {var_label.upper()}")
    print(f"{'='*70}")
    
    # Tableau croisé
    crosstab = pd.crosstab(
        df[variable],
        df['interet_projet'],
        margins=True
    )
    
    # Pourcentages en ligne
    crosstab_pct = pd.crosstab(
        df[variable],
        df['interet_projet'],
        normalize='index'
    ) * 100
    
    print("\nEffectifs :")
    print(crosstab)
    
    print(f"\nPourcentages (% en ligne) :")
    print(crosstab_pct.round(1))
    
    # Identifier les profils les plus/moins interesses
    if 'Oui' in crosstab_pct.columns:
        pct_oui = crosstab_pct['Oui'].sort_values(ascending=False)
        print(f"\nProfils les PLUS interesses :")
        for idx, val in pct_oui.head(3).items():
            if idx != 'All':
                n = crosstab.loc[idx, 'All']
                print(f"  - {idx:20s} : {val:5.1f}% (n={n})")
        
        print(f"\nProfils les MOINS interesses :")
        for idx, val in pct_oui.tail(3).items():
            if idx != 'All':
                n = crosstab.loc[idx, 'All']
                print(f"  - {idx:20s} : {val:5.1f}% (n={n})")


def method_simple(df, population_totale):
    """Méthode 1 : Calcul simple (% global × population)."""
    print(f"\n{'='*70}")
    print("METHODE 1 : CALCUL SIMPLE (ACTUEL)")
    print(f"{'='*70}")
    
    # Calculer le % global
    interet_counts = df['interet_projet'].value_counts()
    total = len(df)
    
    pct_oui = (interet_counts.get('Oui', 0) / total) * 100
    pct_peut_etre = (interet_counts.get('Peut-être', 0) / total) * 100
    pct_non = (interet_counts.get('Non', 0) / total) * 100
    
    print(f"\nPourcentages globaux (echantillon) :")
    print(f"  - Oui : {pct_oui:.1f}% ({interet_counts.get('Oui', 0)}/{total})")
    print(f"  - Peut-etre : {pct_peut_etre:.1f}% ({interet_counts.get('Peut-être', 0)}/{total})")
    print(f"  - Non : {pct_non:.1f}% ({interet_counts.get('Non', 0)}/{total})")
    
    # Appliquer à la population
    nb_oui = population_totale * (pct_oui / 100)
    nb_peut_etre = population_totale * (pct_peut_etre / 100)
    nb_non = population_totale * (pct_non / 100)
    
    print(f"\nExtrapolation a la population ({population_totale:,} habitants) :")
    print(f"  - Oui : {nb_oui:,.0f} personnes")
    print(f"  - Peut-etre : {nb_peut_etre:,.0f} personnes")
    print(f"  - Non : {nb_non:,.0f} personnes")
    
    return {
        'oui': nb_oui,
        'peut_etre': nb_peut_etre,
        'non': nb_non
    }


def method_by_profile(df, margins, profile_vars):
    """Méthode 2 : Calcul par profil (% profil × population profil)."""
    print(f"\n{'='*70}")
    print(f"METHODE 2 : CALCUL PAR PROFIL")
    print(f"{'='*70}")
    print(f"Variables de profil : {', '.join(profile_vars)}")
    
    # Créer les profils
    df['profil'] = df[profile_vars].astype(str).agg('_'.join, axis=1)
    margins['profil'] = margins[profile_vars].astype(str).agg('_'.join, axis=1)
    
    # Calculer le % d'intérêt par profil
    interet_by_profile = []
    
    for profil in margins['profil'].unique():
        # Population INSEE de ce profil
        pop_profil = margins[margins['profil'] == profil]['population'].sum()
        
        # Répondants de ce profil
        df_profil = df[df['profil'] == profil]
        n_profil = len(df_profil)
        
        if n_profil > 0:
            # Calculer les %
            pct_oui = (df_profil['interet_projet'] == 'Oui').sum() / n_profil * 100
            pct_peut_etre = (df_profil['interet_projet'] == 'Peut-être').sum() / n_profil * 100
            pct_non = (df_profil['interet_projet'] == 'Non').sum() / n_profil * 100
            
            # Extrapoler
            nb_oui = pop_profil * (pct_oui / 100)
            nb_peut_etre = pop_profil * (pct_peut_etre / 100)
            nb_non = pop_profil * (pct_non / 100)
        else:
            # Pas de répondant pour ce profil → utiliser la moyenne globale
            pct_global_oui = (df['interet_projet'] == 'Oui').sum() / len(df) * 100
            pct_global_peut_etre = (df['interet_projet'] == 'Peut-être').sum() / len(df) * 100
            pct_global_non = (df['interet_projet'] == 'Non').sum() / len(df) * 100
            
            nb_oui = pop_profil * (pct_global_oui / 100)
            nb_peut_etre = pop_profil * (pct_global_peut_etre / 100)
            nb_non = pop_profil * (pct_global_non / 100)
            
            pct_oui = pct_global_oui
            pct_peut_etre = pct_global_peut_etre
            pct_non = pct_global_non
        
        interet_by_profile.append({
            'profil': profil,
            'pop_insee': pop_profil,
            'n_repondants': n_profil,
            'pct_oui': pct_oui,
            'pct_peut_etre': pct_peut_etre,
            'pct_non': pct_non,
            'nb_oui': nb_oui,
            'nb_peut_etre': nb_peut_etre,
            'nb_non': nb_non
        })
    
    df_profils = pd.DataFrame(interet_by_profile)
    
    # Statistiques
    print(f"\nNombre de profils : {len(df_profils)}")
    print(f"Profils avec repondants : {(df_profils['n_repondants'] > 0).sum()}")
    print(f"Profils sans repondants : {(df_profils['n_repondants'] == 0).sum()}")
    print(f"Repondants moyen par profil : {df_profils['n_repondants'].mean():.1f}")
    
    # Totaux
    total_oui = df_profils['nb_oui'].sum()
    total_peut_etre = df_profils['nb_peut_etre'].sum()
    total_non = df_profils['nb_non'].sum()
    total_pop = df_profils['pop_insee'].sum()
    
    print(f"\nExtrapolation a la population ({total_pop:,.0f} habitants) :")
    print(f"  - Oui : {total_oui:,.0f} personnes")
    print(f"  - Peut-etre : {total_peut_etre:,.0f} personnes")
    print(f"  - Non : {total_non:,.0f} personnes")
    
    # Top profils contributeurs
    print(f"\nTop 5 profils contributeurs (nb Oui) :")
    top5 = df_profils.nlargest(5, 'nb_oui')
    for _, row in top5.iterrows():
        print(f"  - {row['profil']:30s} : {row['nb_oui']:6.0f} personnes "
              f"({row['pct_oui']:5.1f}%, n={row['n_repondants']}, pop={row['pop_insee']:,})")
    
    return {
        'oui': total_oui,
        'peut_etre': total_peut_etre,
        'non': total_non,
        'details': df_profils
    }


def compare_methods(result_simple, result_profile):
    """Compare les deux méthodes."""
    print(f"\n{'='*70}")
    print("COMPARAISON DES DEUX METHODES")
    print(f"{'='*70}")
    
    print(f"\n{'Reponse':<15s} {'Simple':>12s} {'Par Profil':>12s} {'Ecart':>12s} {'Ecart %':>10s}")
    print("-" * 70)
    
    for key in ['oui', 'peut_etre', 'non']:
        simple = result_simple[key]
        profile = result_profile[key]
        ecart = profile - simple
        ecart_pct = (ecart / simple * 100) if simple > 0 else 0
        
        print(f"{key.capitalize():<15s} {simple:>12,.0f} {profile:>12,.0f} "
              f"{ecart:>+12,.0f} {ecart_pct:>+9.1f}%")
    
    print("\nInterpretation :")
    ecart_oui_pct = ((result_profile['oui'] - result_simple['oui']) / result_simple['oui'] * 100)
    
    if abs(ecart_oui_pct) < 5:
        print("  Les deux methodes donnent des resultats TRES SIMILAIRES (<5% ecart)")
        print("  -> La methode simple est suffisante")
    elif abs(ecart_oui_pct) < 15:
        print("  Les deux methodes donnent des resultats SIMILAIRES (5-15% ecart)")
        print("  -> La methode simple est acceptable, mais la methode par profil est plus precise")
    else:
        print("  Les deux methodes donnent des resultats DIFFERENTS (>15% ecart)")
        print("  -> Privilegier la methode par profil si l'echantillon le permet")


def main():
    """Fonction principale."""
    print("="*70)
    print("ANALYSE DE L'INTERET PAR PROFIL DEMOGRAPHIQUE")
    print("="*70)
    
    try:
        # 1. Charger les données
        df, margins = load_data()
        population_totale = margins['population'].sum()
        
        # 2. Analyses univariées
        analyze_interest_by_variable(df, 'age_group', 'AGE')
        analyze_interest_by_variable(df, 'sexe', 'SEXE')
        
        # Convertir CSP en labels
        csp_labels = {1: 'Actifs', 2: 'Etudiants/Chomeurs', 3: 'Retraites/Inactifs'}
        df['csp_label'] = df['csp'].map(csp_labels)
        analyze_interest_by_variable(df, 'csp_label', 'CSP')
        
        # 3. Méthode simple
        result_simple = method_simple(df, population_totale)
        
        # 4. Méthode par profil (âge + sexe uniquement, car 52/36 = 1.4 répondants/profil)
        print("\n" + "="*70)
        print("NOTE : Avec 52 repondants et 36 profils possibles (6 ages x 2 sexes x 3 CSP),")
        print("       on a en moyenne 1.4 repondants par profil -> TROP PEU")
        print("       -> On utilise AGE + SEXE uniquement (12 profils, 4.3 repondants/profil)")
        print("="*70)
        
        result_profile = method_by_profile(df, margins, ['age_group', 'sexe'])
        
        # 5. Comparaison
        compare_methods(result_simple, result_profile)
        
        # 6. Recommandations
        print(f"\n{'='*70}")
        print("RECOMMANDATIONS")
        print(f"{'='*70}")
        
        print("\n1. ESTIMATION GLOBALE :")
        print(f"   Utiliser la methode SIMPLE : ~{result_simple['oui']:,.0f} personnes interessees")
        print(f"   Fourchette prudente : {result_simple['oui']*0.85:,.0f} - {result_simple['oui']*1.15:,.0f}")
        
        print("\n2. SEGMENTATION :")
        print("   Analyser separement par AGE, SEXE, CSP (univarie)")
        print("   -> Identifier les cibles prioritaires")
        
        print("\n3. POUR AMELIORER :")
        print("   Augmenter l'echantillon a 200+ repondants Besancon")
        print("   -> Permettrait une analyse fiable par profil complet (agexsexexcsp)")
        
        print("\n" + "="*70)
        print("ANALYSE TERMINEE")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

