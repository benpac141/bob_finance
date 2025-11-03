"""
Script pour lister tous les IRIS de Besançon avec leur population.
Permet d'identifier les IRIS du centre-ville.
"""

import pandas as pd
from pathlib import Path

CENSUS_FILE = r"D:\python_work\eqasim-bfc\data\raw\census_2022.csv"

print("Chargement du recensement...")
df = pd.read_csv(CENSUS_FILE, sep=";", dtype=str, low_memory=False)

# Filtrer sur Besançon (commune 25056)
df_besancon = df[df['ARM'] == '251'].copy()  # ARM = arrondissement

print(f"\nPopulation de Besancon : {len(df_besancon):,} individus")

# Grouper par IRIS
iris_stats = df_besancon.groupby('IRIS').agg({
    'IRIS': 'count'
}).rename(columns={'IRIS': 'population'})

iris_stats = iris_stats[iris_stats.index != 'ZZZZZZZZZ']
iris_stats = iris_stats.sort_index()

print(f"\nNombre d'IRIS a Besancon : {len(iris_stats)}")
print("\nListe des IRIS avec population :")
print("=" * 60)

for iris_code, row in iris_stats.iterrows():
    pop = row['population']
    print(f"{iris_code} : {pop:6,} habitants")

# Sauvegarder dans un fichier
output_file = Path(__file__).parent.parent / "data" / "iris_besancon_list.csv"
iris_stats.to_csv(output_file)
print(f"\n[OK] Liste sauvegardee : {output_file}")

print("\n" + "=" * 60)
print("Pour identifier les IRIS centre-ville, vous pouvez :")
print("1. Consulter le site de l'INSEE")
print("2. Utiliser une carte des IRIS")
print("3. Selectionner les IRIS avec les codes les plus proches du centre")
print("=" * 60)

