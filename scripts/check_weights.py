"""
Script pour vérifier les poids calculés.
"""

import pandas as pd
from pathlib import Path

# Trouver le dernier fichier de poids
reports_dir = Path(__file__).parent.parent / "outputs" / "reports"
weight_files = list(reports_dir.glob("data_weighted_*.csv"))

if not weight_files:
    print("Aucun fichier de poids trouvé")
    exit(1)

latest_file = max(weight_files, key=lambda x: x.stat().st_mtime)

print("="*70)
print("VERIFICATION DES POIDS")
print("="*70)

# Charger les données pondérées
df = pd.read_csv(latest_file)

print(f"\nFichier : {latest_file.name}")
print(f"Nombre de répondants : {len(df)}")

print("\n=== STATISTIQUES DES POIDS ===")
print(df['weight'].describe())

print("\n=== POIDS UNIQUES ===")
unique_weights = df['weight'].unique()
print(f"Nombre de poids différents : {len(unique_weights)}")
print(f"Poids : {sorted(unique_weights)}")

print("\n=== COMPARAISON ECHANTILLON / POPULATION ===")
print(f"Nombre de répondants : {len(df)}")
print(f"Somme des poids : {df['weight'].sum():.0f}")

# Charger les marges
margins = pd.read_csv(Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv")
pop_cible = margins['population'].sum()
print(f"Population cible (marges) : {pop_cible:.0f}")

ratio = df['weight'].sum() / pop_cible
print(f"Ratio somme_poids / population : {ratio:.3f}")

if ratio < 0.9 or ratio > 1.1:
    print("\n⚠️ ATTENTION : La somme des poids ne correspond pas à la population cible !")
    print("Le redressement n'a probablement pas convergé correctement.")

print("\n=== DISTRIBUTION DE L'ECHANTILLON ===")

print("\nPar age_group :")
dist_age = df.groupby('age_group').agg({
    'id_repondant': 'count',
    'weight': 'sum'
}).rename(columns={'id_repondant': 'effectif', 'weight': 'poids_total'})
dist_age['pct_effectif'] = dist_age['effectif'] / dist_age['effectif'].sum() * 100
dist_age['pct_poids'] = dist_age['poids_total'] / dist_age['poids_total'].sum() * 100
print(dist_age)

print("\nPar sexe :")
dist_sexe = df.groupby('sexe').agg({
    'id_repondant': 'count',
    'weight': 'sum'
}).rename(columns={'id_repondant': 'effectif', 'weight': 'poids_total'})
dist_sexe['pct_effectif'] = dist_sexe['effectif'] / dist_sexe['effectif'].sum() * 100
dist_sexe['pct_poids'] = dist_sexe['poids_total'] / dist_sexe['poids_total'].sum() * 100
print(dist_sexe)

print("\nPar csp :")
dist_csp = df.groupby('csp').agg({
    'id_repondant': 'count',
    'weight': 'sum'
}).rename(columns={'id_repondant': 'effectif', 'weight': 'poids_total'})
dist_csp['pct_effectif'] = dist_csp['effectif'] / dist_csp['effectif'].sum() * 100
dist_csp['pct_poids'] = dist_csp['poids_total'] / dist_csp['poids_total'].sum() * 100
print(dist_csp)

print("\n=== MARGES CIBLES ===")

print("\nPar age_group (cible) :")
marge_age = margins.groupby('age_group')['population'].sum()
marge_age_pct = marge_age / marge_age.sum() * 100
for age, pop in marge_age.items():
    pct = marge_age_pct[age]
    print(f"  {age:10s} : {pop:8,.0f} ({pct:5.1f}%)")

print("\nPar sexe (cible) :")
marge_sexe = margins.groupby('sexe')['population'].sum()
marge_sexe_pct = marge_sexe / marge_sexe.sum() * 100
for sexe, pop in marge_sexe.items():
    pct = marge_sexe_pct[sexe]
    print(f"  {sexe} : {pop:8,.0f} ({pct:5.1f}%)")

print("\nPar csp (cible) :")
marge_csp = margins.groupby('csp')['population'].sum()
marge_csp_pct = marge_csp / marge_csp.sum() * 100
csp_labels = {1.0: 'Actifs occupés', 2.0: 'Chômeurs', 3.0: 'Inactifs'}
for csp, pop in marge_csp.items():
    pct = marge_csp_pct[csp]
    label = csp_labels.get(csp, 'Inconnu')
    print(f"  {int(csp)} - {label:20s} : {pop:8,.0f} ({pct:5.1f}%)")

print("\n" + "="*70)
print("DIAGNOSTIC")
print("="*70)

# Vérifier si tous les poids sont identiques
if len(unique_weights) == 1:
    print("\n⚠️ PROBLEME : Tous les poids sont identiques !")
    print("   Le redressement n'a pas fonctionné.")
    print("\nCauses possibles :")
    print("  1. Echantillon trop petit par rapport à la population")
    print("  2. Limites de poids (min_weight/max_weight) trop restrictives")
    print("  3. Echantillon non représentatif")
    print("\nSolutions :")
    print("  1. Augmenter max_weight dans config.yaml (ex: 100 ou 500)")
    print("  2. Augmenter max_iterations (ex: 500)")
    print("  3. Assouplir tolerance (ex: 0.01 ou 0.05)")
    print("  4. Réduire le nombre de variables de redressement")
else:
    print("\n✓ Les poids sont différenciés")
    print(f"  Poids min : {df['weight'].min():.2f}")
    print(f"  Poids max : {df['weight'].max():.2f}")
    print(f"  Ratio max/min : {df['weight'].max() / df['weight'].min():.2f}")

print("="*70)

