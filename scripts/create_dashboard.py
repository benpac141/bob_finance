"""
Crée un tableau de bord visuel avec graphiques avancés.

Génère :
- Heatmap : Intérêt par (âge × sexe)
- Graphiques en barres : % intérêt par profil
- Pyramide des âges : Intéressés vs Non intéressés
- Contribution de chaque segment au potentiel total
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from datetime import datetime
import sys

# Chemins
DATA_FILE = Path(__file__).parent.parent / "data" / "raw" / "enquete_all_prepared.xlsx"
MARGINS_FILE = Path(__file__).parent.parent / "data" / "margins" / "margins_center.csv"
OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "figures"


def load_data():
    """Charge les données."""
    df = pd.read_excel(DATA_FILE)
    margins = pd.read_csv(MARGINS_FILE)
    df_besancon = df[df['is_besancon']].copy()
    return df_besancon, margins


def create_heatmap_age_sexe(df, output_path):
    """Crée une heatmap de l'intérêt par âge et sexe."""
    print("  - Creation de la heatmap age x sexe...")
    
    # Préparer les données
    pivot = pd.crosstab(
        df['age_group'],
        df['sexe'],
        values=(df['interet_projet'] == 'Oui').astype(int),
        aggfunc='mean'
    ) * 100
    
    # Créer la figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Heatmap
    sns.heatmap(
        pivot,
        annot=True,
        fmt='.1f',
        cmap='RdYlGn',
        vmin=0,
        vmax=100,
        cbar_kws={'label': '% Interet'},
        ax=ax
    )
    
    ax.set_title('Interet pour le Projet par Age et Sexe', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Sexe', fontsize=12)
    ax.set_ylabel('Tranche d\'age', fontsize=12)
    
    # Remplacer les labels
    ax.set_xticklabels(['Femmes', 'Hommes'])
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"    [OK] {output_path}")


def create_barplot_by_profile(df, output_path):
    """Crée un graphique en barres de l'intérêt par profil."""
    print("  - Creation du graphique en barres par profil...")
    
    # Calculer les % par profil
    csp_labels = {1: 'Actifs', 2: 'Etudiants/Chomeurs', 3: 'Retraites'}
    df['csp_label'] = df['csp'].map(csp_labels)
    
    # Par âge
    age_pct = df.groupby('age_group').apply(
        lambda x: (x['interet_projet'] == 'Oui').sum() / len(x) * 100
    ).sort_values(ascending=False)
    
    # Par sexe
    sexe_pct = df.groupby('sexe').apply(
        lambda x: (x['interet_projet'] == 'Oui').sum() / len(x) * 100
    )
    sexe_pct.index = ['Femmes' if x == 'F' else 'Hommes' for x in sexe_pct.index]
    
    # Par CSP
    csp_pct = df.groupby('csp_label').apply(
        lambda x: (x['interet_projet'] == 'Oui').sum() / len(x) * 100
    ).sort_values(ascending=False)
    
    # Créer la figure
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    
    # Graphique 1 : Par âge
    age_pct.plot(kind='barh', ax=axes[0], color='steelblue')
    axes[0].set_title('Interet par Age', fontsize=14, fontweight='bold')
    axes[0].set_xlabel('% Interet "Oui"', fontsize=11)
    axes[0].set_ylabel('')
    axes[0].grid(axis='x', alpha=0.3)
    axes[0].set_xlim(0, 100)
    
    # Ajouter les valeurs
    for i, v in enumerate(age_pct):
        axes[0].text(v + 2, i, f'{v:.1f}%', va='center', fontsize=10)
    
    # Graphique 2 : Par sexe
    sexe_pct.plot(kind='barh', ax=axes[1], color='coral')
    axes[1].set_title('Interet par Sexe', fontsize=14, fontweight='bold')
    axes[1].set_xlabel('% Interet "Oui"', fontsize=11)
    axes[1].set_ylabel('')
    axes[1].grid(axis='x', alpha=0.3)
    axes[1].set_xlim(0, 100)
    
    for i, v in enumerate(sexe_pct):
        axes[1].text(v + 2, i, f'{v:.1f}%', va='center', fontsize=10)
    
    # Graphique 3 : Par CSP
    csp_pct.plot(kind='barh', ax=axes[2], color='mediumseagreen')
    axes[2].set_title('Interet par Situation Pro.', fontsize=14, fontweight='bold')
    axes[2].set_xlabel('% Interet "Oui"', fontsize=11)
    axes[2].set_ylabel('')
    axes[2].grid(axis='x', alpha=0.3)
    axes[2].set_xlim(0, 100)
    
    for i, v in enumerate(csp_pct):
        axes[2].text(v + 2, i, f'{v:.1f}%', va='center', fontsize=10)
    
    plt.suptitle('Interet pour le Projet par Profil Demographique', 
                 fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"    [OK] {output_path}")


def create_pyramid_chart(df, margins, output_path):
    """Crée une pyramide des âges : Intéressés vs Population."""
    print("  - Creation de la pyramide des ages...")
    
    # Calculer les effectifs par âge et sexe
    population_totale = margins['population'].sum()
    
    # Population INSEE
    pop_insee = margins.groupby(['age_group', 'sexe'])['population'].sum().unstack(fill_value=0)
    
    # Intéressés (estimés)
    interesses = []
    for age in pop_insee.index:
        for sexe in ['F', 'M']:
            df_seg = df[(df['age_group'] == age) & (df['sexe'] == sexe)]
            if len(df_seg) > 0:
                pct = (df_seg['interet_projet'] == 'Oui').sum() / len(df_seg)
            else:
                pct = (df['interet_projet'] == 'Oui').sum() / len(df)  # Moyenne globale
            
            pop = pop_insee.loc[age, sexe] if age in pop_insee.index and sexe in pop_insee.columns else 0
            interesses.append({
                'age_group': age,
                'sexe': sexe,
                'population': pop * pct
            })
    
    df_interesses = pd.DataFrame(interesses)
    int_pivot = df_interesses.pivot(index='age_group', columns='sexe', values='population').fillna(0)
    
    # Créer la figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Ordre des âges
    age_order = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
    y_pos = np.arange(len(age_order))
    
    # Barres pour les femmes (gauche)
    pop_f = [-pop_insee.loc[age, 'F'] if age in pop_insee.index else 0 for age in age_order]
    int_f = [-int_pivot.loc[age, 'F'] if age in int_pivot.index else 0 for age in age_order]
    
    # Barres pour les hommes (droite)
    pop_m = [pop_insee.loc[age, 'M'] if age in pop_insee.index else 0 for age in age_order]
    int_m = [int_pivot.loc[age, 'M'] if age in int_pivot.index else 0 for age in age_order]
    
    # Tracer
    ax.barh(y_pos, pop_f, height=0.8, color='lightcoral', alpha=0.5, label='Population F')
    ax.barh(y_pos, int_f, height=0.8, color='darkred', alpha=0.8, label='Interessees F')
    ax.barh(y_pos, pop_m, height=0.8, color='lightblue', alpha=0.5, label='Population M')
    ax.barh(y_pos, int_m, height=0.8, color='darkblue', alpha=0.8, label='Interesses M')
    
    # Axes
    ax.set_yticks(y_pos)
    ax.set_yticklabels(age_order)
    ax.set_xlabel('Population', fontsize=12)
    ax.set_ylabel('Tranche d\'age', fontsize=12)
    ax.set_title('Pyramide des Ages : Population vs Interesses', fontsize=16, fontweight='bold', pad=20)
    
    # Ligne centrale
    ax.axvline(0, color='black', linewidth=0.8)
    
    # Légende
    ax.legend(loc='upper right', fontsize=10)
    
    # Grille
    ax.grid(axis='x', alpha=0.3)
    
    # Labels des axes
    ax.text(-max(abs(min(pop_f)), max(pop_m))*0.5, -0.8, 'Femmes', 
            ha='center', fontsize=12, fontweight='bold')
    ax.text(max(abs(min(pop_f)), max(pop_m))*0.5, -0.8, 'Hommes', 
            ha='center', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"    [OK] {output_path}")


def create_contribution_chart(df, margins, output_path):
    """Crée un graphique de contribution de chaque segment."""
    print("  - Creation du graphique de contribution...")
    
    # Calculer les contributions par profil (âge × sexe)
    contributions = []
    
    for age in sorted(df['age_group'].unique()):
        for sexe in ['F', 'M']:
            df_seg = df[(df['age_group'] == age) & (df['sexe'] == sexe)]
            
            if len(df_seg) > 0:
                pct = (df_seg['interet_projet'] == 'Oui').sum() / len(df_seg)
            else:
                pct = (df['interet_projet'] == 'Oui').sum() / len(df)
            
            pop = margins[(margins['age_group'] == age) & (margins['sexe'] == sexe)]['population'].sum()
            nb_interesses = pop * pct
            
            sexe_label = 'F' if sexe == 'F' else 'M'
            contributions.append({
                'profil': f'{age} {sexe_label}',
                'nb_interesses': nb_interesses,
                'age': age,
                'sexe': sexe
            })
    
    df_contrib = pd.DataFrame(contributions).sort_values('nb_interesses', ascending=False)
    
    # Créer la figure
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Couleurs selon le sexe
    colors_map = {'F': 'coral', 'M': 'steelblue'}
    colors_list = [colors_map[row['sexe']] for _, row in df_contrib.iterrows()]
    
    # Graphique en barres
    bars = ax.barh(df_contrib['profil'], df_contrib['nb_interesses'], color=colors_list)
    
    ax.set_xlabel('Nombre d\'interesses (estimation)', fontsize=12)
    ax.set_ylabel('Profil (Age + Sexe)', fontsize=12)
    ax.set_title('Contribution de Chaque Segment au Potentiel Total', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Ajouter les valeurs
    for i, (_, row) in enumerate(df_contrib.iterrows()):
        ax.text(row['nb_interesses'] + 30, i, f"{int(row['nb_interesses']):,}", 
                va='center', fontsize=9)
    
    # Légende
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='coral', label='Femmes'),
        Patch(facecolor='steelblue', label='Hommes')
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"    [OK] {output_path}")


def create_summary_dashboard(df, margins, output_path):
    """Crée un tableau de bord récapitulatif."""
    print("  - Creation du tableau de bord recapitulatif...")
    
    fig = plt.figure(figsize=(16, 10))
    gs = fig.add_gridspec(3, 3, hspace=0.4, wspace=0.3)
    
    # 1. Chiffres clés (en haut à gauche)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.axis('off')
    
    population_totale = int(margins['population'].sum())
    pct_oui = (df['interet_projet'] == 'Oui').sum() / len(df) * 100
    nb_interesses = int(population_totale * (pct_oui / 100))
    pct_cotisation = (df['accepte_cotisation'].str.contains('Oui', na=False)).sum() / len(df) * 100
    
    text_stats = f"""
    CHIFFRES CLES
    
    Repondants : {len(df)}
    Population : {population_totale:,}
    
    Interet : {pct_oui:.1f}%
    Nb interesses : {nb_interesses:,}
    
    Accepte cotisation : {pct_cotisation:.1f}%
    """
    
    ax1.text(0.1, 0.5, text_stats, fontsize=12, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    # 2. Répartition globale (en haut au centre)
    ax2 = fig.add_subplot(gs[0, 1])
    interet_counts = df['interet_projet'].value_counts()
    colors_pie = ['#2ecc71', '#f39c12', '#e74c3c']
    ax2.pie(interet_counts, labels=interet_counts.index, autopct='%1.1f%%',
            colors=colors_pie, startangle=90)
    ax2.set_title('Repartition de l\'Interet', fontsize=12, fontweight='bold')
    
    # 3. Par âge (en haut à droite)
    ax3 = fig.add_subplot(gs[0, 2])
    age_pct = df.groupby('age_group').apply(
        lambda x: (x['interet_projet'] == 'Oui').sum() / len(x) * 100
    ).sort_values()
    age_pct.plot(kind='barh', ax=ax3, color='steelblue')
    ax3.set_title('Interet par Age', fontsize=12, fontweight='bold')
    ax3.set_xlabel('% Oui')
    ax3.grid(axis='x', alpha=0.3)
    
    # 4. Par sexe (milieu gauche)
    ax4 = fig.add_subplot(gs[1, 0])
    sexe_pct = df.groupby('sexe').apply(
        lambda x: (x['interet_projet'] == 'Oui').sum() / len(x) * 100
    )
    sexe_pct.index = ['Femmes' if x == 'F' else 'Hommes' for x in sexe_pct.index]
    sexe_pct.plot(kind='bar', ax=ax4, color=['coral', 'steelblue'])
    ax4.set_title('Interet par Sexe', fontsize=12, fontweight='bold')
    ax4.set_ylabel('% Oui')
    ax4.set_xticklabels(sexe_pct.index, rotation=0)
    ax4.grid(axis='y', alpha=0.3)
    
    # 5. Par CSP (milieu centre)
    ax5 = fig.add_subplot(gs[1, 1])
    csp_labels = {1: 'Actifs', 2: 'Etud/Chom', 3: 'Retraites'}
    df['csp_label'] = df['csp'].map(csp_labels)
    csp_pct = df.groupby('csp_label').apply(
        lambda x: (x['interet_projet'] == 'Oui').sum() / len(x) * 100
    ).sort_values()
    csp_pct.plot(kind='barh', ax=ax5, color='mediumseagreen')
    ax5.set_title('Interet par CSP', fontsize=12, fontweight='bold')
    ax5.set_xlabel('% Oui')
    ax5.grid(axis='x', alpha=0.3)
    
    # 6. Prix max (milieu droite)
    ax6 = fig.add_subplot(gs[1, 2])
    prix_counts = df['prix_max_location'].value_counts().head(5)
    prix_counts.plot(kind='bar', ax=ax6, color='orange')
    ax6.set_title('Prix Max Location', fontsize=12, fontweight='bold')
    ax6.set_ylabel('Nombre')
    ax6.set_xticklabels(prix_counts.index, rotation=45, ha='right')
    ax6.grid(axis='y', alpha=0.3)
    
    # 7. Heatmap (bas, 2 colonnes)
    ax7 = fig.add_subplot(gs[2, :2])
    pivot = pd.crosstab(
        df['age_group'],
        df['sexe'],
        values=(df['interet_projet'] == 'Oui').astype(int),
        aggfunc='mean'
    ) * 100
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', vmin=0, vmax=100,
                cbar_kws={'label': '% Interet'}, ax=ax7)
    ax7.set_title('Interet par Age x Sexe', fontsize=12, fontweight='bold')
    ax7.set_xticklabels(['Femmes', 'Hommes'])
    
    # 8. Top segments (bas droite)
    ax8 = fig.add_subplot(gs[2, 2])
    ax8.axis('off')
    
    top_text = """
    TOP 3 SEGMENTS
    
    1. Femmes 25-54 ans
       85-100% interet
    
    2. Actifs 35-54 ans
       80-100% interet
    
    3. Jeunes 25-34 ans
       80% interet
    """
    
    ax8.text(0.1, 0.5, top_text, fontsize=11, verticalalignment='center',
             bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    
    # Titre général
    fig.suptitle('Tableau de Bord - Enquete BOB', fontsize=18, fontweight='bold')
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"    [OK] {output_path}")


def main():
    """Fonction principale."""
    print("="*70)
    print("CREATION DU TABLEAU DE BORD INTERACTIF")
    print("="*70)
    
    try:
        # Charger les données
        print("\nChargement des donnees...")
        df, margins = load_data()
        
        # Créer le répertoire de sortie
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Générer les visualisations
        print("\nGeneration des visualisations...")
        
        create_heatmap_age_sexe(df, OUTPUT_DIR / f'dashboard_heatmap_{timestamp}.png')
        create_barplot_by_profile(df, OUTPUT_DIR / f'dashboard_barplot_{timestamp}.png')
        create_pyramid_chart(df, margins, OUTPUT_DIR / f'dashboard_pyramid_{timestamp}.png')
        create_contribution_chart(df, margins, OUTPUT_DIR / f'dashboard_contribution_{timestamp}.png')
        create_summary_dashboard(df, margins, OUTPUT_DIR / f'dashboard_summary_{timestamp}.png')
        
        print("\n" + "="*70)
        print("SUCCES !")
        print("="*70)
        print(f"Visualisations generees dans : {OUTPUT_DIR}")
        print("\nFichiers crees :")
        print(f"  - dashboard_heatmap_{timestamp}.png")
        print(f"  - dashboard_barplot_{timestamp}.png")
        print(f"  - dashboard_pyramid_{timestamp}.png")
        print(f"  - dashboard_contribution_{timestamp}.png")
        print(f"  - dashboard_summary_{timestamp}.png (TABLEAU DE BORD COMPLET)")
        print("="*70)
        
        return 0
        
    except Exception as e:
        print(f"\n[ERREUR] {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

