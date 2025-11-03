"""
Script pour comparer les réponses Besançon vs Hors-Besançon.
"""

import pandas as pd
import sys
from pathlib import Path

# Chemins
DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.xlsx"


def load_data():
    """Charge les données préparées."""
    print(f"Chargement de {DATA_FILE}...")
    df = pd.read_excel(DATA_FILE)
    print(f"  - {len(df)} repondants charges")
    return df


def compare_variable(df, var_name, var_label):
    """Compare une variable entre Besançon et Hors-Besançon."""
    print(f"\n{'='*70}")
    print(f"{var_label}")
    print(f"{'='*70}")
    
    # Besançon
    df_bes = df[df['is_besancon']]
    print(f"\nBESANCON (n={len(df_bes)}) :")
    if var_name in df_bes.columns:
        counts = df_bes[var_name].value_counts()
        for val, count in counts.items():
            pct = 100 * count / len(df_bes)
            print(f"  {str(val):40s} : {count:3d} ({pct:5.1f}%)")
    else:
        print(f"  Variable '{var_name}' non trouvee")
    
    # Hors Besançon
    df_hors = df[~df['is_besancon']]
    print(f"\nHORS BESANCON (n={len(df_hors)}) :")
    if var_name in df_hors.columns:
        counts = df_hors[var_name].value_counts()
        for val, count in counts.items():
            pct = 100 * count / len(df_hors)
            print(f"  {str(val):40s} : {count:3d} ({pct:5.1f}%)")
    else:
        print(f"  Variable '{var_name}' non trouvee")


def main():
    """Fonction principale."""
    print("="*70)
    print("COMPARAISON BESANCON VS HORS-BESANCON")
    print("="*70)
    
    try:
        df = load_data()
        
        # Variables démographiques
        compare_variable(df, 'age_group', "AGE")
        compare_variable(df, 'sexe', "SEXE")
        compare_variable(df, 'csp', "CATEGORIE SOCIO-PROFESSIONNELLE")
        
        # Variables d'intérêt
        compare_variable(df, 'interet_projet', "INTERET POUR LE PROJET")
        compare_variable(df, 'accepte_cotisation', "ACCEPTATION COTISATION")
        compare_variable(df, 'deja_utilise_services', "DEJA UTILISE DES SERVICES")
        compare_variable(df, 'partage_oui', "ACCEPTE DE PARTAGER")
        compare_variable(df, 'prix_max_location', "PRIX MAX LOCATION")
        
        print("\n" + "="*70)
        print("OBSERVATIONS CLES")
        print("="*70)
        
        # Calcul intérêt
        df_bes = df[df['is_besancon']]
        df_hors = df[~df['is_besancon']]
        
        if 'interet_projet' in df.columns:
            pct_oui_bes = 100 * (df_bes['interet_projet'] == 'Oui').sum() / len(df_bes)
            pct_oui_hors = 100 * (df_hors['interet_projet'] == 'Oui').sum() / len(df_hors)
            
            print(f"\nInteret 'Oui' :")
            print(f"  - Besancon : {pct_oui_bes:.1f}%")
            print(f"  - Hors Besancon : {pct_oui_hors:.1f}%")
            print(f"  - Ecart : {pct_oui_bes - pct_oui_hors:+.1f} points")
            
            if pct_oui_bes > pct_oui_hors:
                print("\n  -> Les Besanconnais sont PLUS interesses que les hors-Besancon")
                print("     Cela valide l'approche de les analyser separement.")
            else:
                print("\n  -> Les hors-Besancon sont aussi interesses")
        
        print("\n" + "="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

