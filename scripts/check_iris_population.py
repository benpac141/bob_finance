"""
Script pour vérifier la population des IRIS sélectionnés.
"""

import pandas as pd
from pathlib import Path

# Charger les marges créées
margins_file = Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv"
df_margins = pd.read_csv(margins_file)

print("=" * 70)
print("VERIFICATION DE LA POPULATION DES IRIS CENTRE-VILLE")
print("=" * 70)

print("\n=== MARGES CREEES (adultes 18+) ===")
print(f"Population totale : {df_margins['population'].sum():,} adultes\n")

print("Population par IRIS :")
pop_iris = df_margins.groupby('code_iris')['population'].sum().sort_values(ascending=False)
for iris, pop in pop_iris.items():
    print(f"  {iris} : {int(pop):4,} adultes")

print(f"\nNombre d'IRIS : {len(pop_iris)}")
print(f"Population moyenne par IRIS : {pop_iris.mean():.0f} adultes")
print(f"Population min par IRIS : {pop_iris.min():.0f} adultes")
print(f"Population max par IRIS : {pop_iris.max():.0f} adultes")

# Vérifier dans le recensement complet
print("\n" + "=" * 70)
print("VERIFICATION DANS LE RECENSEMENT INSEE 2022")
print("=" * 70)

census_file = Path("D:/python_work/eqasim-bfc/data/raw/census_2022.csv")
if census_file.exists():
    print("\nChargement du recensement...")
    df_census = pd.read_csv(census_file, sep=';', dtype=str, low_memory=False)
    
    iris_center = [
        '250560101', '250560102', '250560103', '250560104',
        '250560302', '250560303', '250560304',
        '250560401', '250560402',
        '250560501', '250560502'
    ]
    
    df_center = df_census[df_census['IRIS'].isin(iris_center)].copy()
    
    print(f"\nPopulation totale (tous âges) : {len(df_center):,} personnes")
    
    print("\nPopulation par IRIS (tous âges) :")
    for iris in sorted(iris_center):
        pop = len(df_center[df_center['IRIS'] == iris])
        print(f"  {iris} : {pop:5,} personnes")
    
    # Adultes 18+
    print("\n--- Adultes 18+ uniquement ---")
    df_center['age_num'] = pd.to_numeric(df_center['AGED'], errors='coerce')
    df_adults = df_center[df_center['age_num'] >= 18]
    
    print(f"Population adulte (18+) : {len(df_adults):,}")
    
    print("\nPopulation adulte par IRIS :")
    for iris in sorted(iris_center):
        pop = len(df_adults[df_adults['IRIS'] == iris])
        print(f"  {iris} : {pop:5,} adultes")
    
    # Comparaison
    print("\n" + "=" * 70)
    print("COMPARAISON")
    print("=" * 70)
    print(f"Recensement brut (18+) : {len(df_adults):,} adultes")
    print(f"Marges créées (18+)    : {df_margins['population'].sum():,.0f} adultes")
    diff = len(df_adults) - df_margins['population'].sum()
    print(f"Différence             : {diff:,.0f} adultes")
    
    if abs(diff) > 100:
        print("\n⚠️ ATTENTION : Différence importante détectée")
        print("Causes possibles :")
        print("  - Filtrage sur les valeurs manquantes (âge, sexe, CSP)")
        print("  - Exclusion de certaines modalités")
else:
    print("\n⚠️ Fichier recensement non trouvé")

print("\n" + "=" * 70)

