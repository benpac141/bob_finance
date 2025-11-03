"""
Script d'analyse BOB avec gestion des filtres locaux/globaux.

Stratégie :
1. Charger TOUS les répondants (90)
2. Redresser sur Besançon uniquement (52)
3. Analyses générales : tous les répondants
4. Analyses locales : Besançon uniquement
"""

import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from utils import load_config, setup_logging
from load_clean import (
    load_survey_data, load_margins, prepare_margins_dict, add_initial_weights
)
from raking import RakingWeighter, compare_distributions
from analysis import quality_metrics, weighted_frequency
from report_pdf import plot_weight_distribution, plot_convergence, plot_comparison_distribution, plot_frequency
from pdf_report import generate_global_report


def main():
    """Fonction principale."""
    logger = setup_logging(level="INFO")
    logger.info("=" * 70)
    logger.info("ANALYSE BOB - AVEC FILTRES LOCAUX/GLOBAUX")
    logger.info("=" * 70)
    
    try:
        # 1. Configuration
        logger.info("\n[1/8] Chargement de la configuration")
        cfg = load_config('config.yaml')
        
        # 2. Charger les données
        logger.info("\n[2/8] Chargement des données")
        df_all = load_survey_data(
            cfg['paths']['raw_data'],
            cfg['survey'].get('sheet_name', 'Sheet1')
        )
        logger.info(f"  - Total répondants : {len(df_all)}")
        logger.info(f"  - Besançon : {df_all['is_besancon'].sum()}")
        logger.info(f"  - Hors Besançon : {(~df_all['is_besancon']).sum()}")
        
        margins_df = load_margins(cfg['paths']['margins'])
        
        # 3. Filtrer pour le redressement (Besançon uniquement)
        logger.info("\n[3/8] Préparation pour le redressement")
        df_besancon = df_all[df_all['is_besancon']].copy()
        logger.info(f"  - Répondants pour redressement : {len(df_besancon)}")
        
        # Ajouter poids initiaux
        df_besancon = add_initial_weights(df_besancon, initial_value=cfg['raking']['initial_weight'])
        
        # 4. Préparer les marges
        logger.info("\n[4/8] Préparation des marges")
        margins_dict = prepare_margins_dict(
            margins_df,
            cfg['survey']['weighting_vars']
        )
        
        # 5. Redressement (sur Besançon uniquement)
        logger.info("\n[5/8] Redressement par raking (Besançon uniquement)")
        weighter = RakingWeighter(
            max_iterations=cfg['raking']['max_iterations'],
            tolerance=cfg['raking']['tolerance'],
            min_weight=cfg['raking']['min_weight'],
            max_weight=cfg['raking']['max_weight']
        )
        
        df_besancon_weighted = weighter.rake(df_besancon, margins_dict)
        
        # Vérifier la qualité
        quality_df = weighter.check_margins_quality(df_besancon_weighted, margins_dict)
        
        # 6. Réintégrer les poids dans le dataframe complet
        logger.info("\n[6/8] Réintégration des poids")
        # Pour les hors Besançon, on met un poids de 1 (ou 0 si on veut les exclure des analyses)
        df_all = df_all.copy()
        df_all['weight'] = 1.0  # Poids par défaut
        
        # Copier les poids calculés pour Besançon
        df_all.loc[df_all['is_besancon'], 'weight'] = df_besancon_weighted['weight'].values
        
        logger.info(f"  - Poids min (Besançon) : {df_all[df_all['is_besancon']]['weight'].min():.3f}")
        logger.info(f"  - Poids max (Besançon) : {df_all[df_all['is_besancon']]['weight'].max():.3f}")
        logger.info(f"  - Poids moyen (Besançon) : {df_all[df_all['is_besancon']]['weight'].mean():.3f}")
        
        # 7. Analyses et figures
        logger.info("\n[7/8] Génération des figures")
        figures_dir = Path(cfg['paths']['output_figures'])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Distribution des poids (Besançon uniquement)
        plot_weight_distribution(
            df_all[df_all['is_besancon']]['weight'],
            figures_dir / f'weights_distribution_{timestamp}.png'
        )
        
        # Convergence
        plot_convergence(
            weighter.convergence_history,
            figures_dir / f'convergence_{timestamp}.png',
            tolerance=cfg['raking']['tolerance']
        )
        
        # Comparaisons avant/après (Besançon uniquement)
        for var in cfg['survey']['weighting_vars']:
            comparison = compare_distributions(df_besancon_weighted, var)
            plot_comparison_distribution(
                comparison,
                var,
                figures_dir / f'comparison_{var}_{timestamp}.png'
            )
        
        # Analyses des variables LOCALES (Besançon uniquement)
        logger.info("\n  Analyses LOCALES (Besançon uniquement) :")
        if 'variables_local' in cfg.get('analysis', {}):
            for var in cfg['analysis']['variables_local']:
                if var in df_all.columns:
                    df_local = df_all[df_all['is_besancon']]
                    freq = weighted_frequency(df_local, var, weight_col='weight')
                    plot_frequency(
                        freq,
                        f"{var} (Besançon)",
                        figures_dir / f'freq_local_{var}_{timestamp}.png',
                        top_n=10
                    )
                    logger.info(f"    - {var} : {len(freq)} modalités")
        
        # Analyses des variables GENERALES (tous)
        logger.info("\n  Analyses GENERALES (tous répondants) :")
        if 'variables_general' in cfg.get('analysis', {}):
            for var in cfg['analysis']['variables_general']:
                if var in df_all.columns:
                    # Pour les hors Besançon, on utilise poids=1
                    freq = weighted_frequency(df_all, var, weight_col='weight')
                    plot_frequency(
                        freq,
                        f"{var} (Tous)",
                        figures_dir / f'freq_general_{var}_{timestamp}.png',
                        top_n=10
                    )
                    logger.info(f"    - {var} : {len(freq)} modalités")
        
        # 8. Rapports
        logger.info("\n[8/8] Génération des rapports")
        
        # Métriques de qualité (Besançon uniquement)
        qm = quality_metrics(df_all[df_all['is_besancon']]['weight'])
        logger.info(f"  - Deff (Besançon) = {qm['deff']:.3f}")
        logger.info(f"  - n_eff (Besançon) = {qm['n_eff']:.0f}")
        logger.info(f"  - Perte d'efficacité = {qm['loss_efficiency']:.1f}%")
        
        # Rapport global PDF
        report_global_path = Path(cfg['paths']['output_reports']) / f'rapport_global_{timestamp}.pdf'
        generate_global_report(
            df_all,
            qm,
            quality_df,
            figures_dir,
            report_global_path,
            cfg
        )
        
        # Sauvegarder les données
        output_data_path = Path(cfg['paths']['output_reports']) / f'data_weighted_{timestamp}.csv'
        df_all.to_csv(output_data_path, index=False, encoding='utf-8-sig')
        logger.info(f"\nDonnées pondérées sauvegardées : {output_data_path}")
        
        # Statistiques finales
        logger.info("\n" + "=" * 70)
        logger.info("RESUME")
        logger.info("=" * 70)
        logger.info(f"Total répondants : {len(df_all)}")
        logger.info(f"  - Besançon (redressés) : {df_all['is_besancon'].sum()}")
        logger.info(f"  - Hors Besançon (non redressés) : {(~df_all['is_besancon']).sum()}")
        logger.info(f"\nAnalyses LOCALES (Besançon) :")
        logger.info(f"  - Variables : {', '.join(cfg['analysis']['variables_local'])}")
        logger.info(f"\nAnalyses GENERALES (Tous) :")
        logger.info(f"  - Variables : {', '.join(cfg['analysis']['variables_general'])}")
        logger.info("\n" + "=" * 70)
        logger.info("ANALYSE TERMINEE AVEC SUCCES")
        logger.info("=" * 70)
        
        return 0
        
    except Exception as e:
        logger.error(f"\nERREUR : {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())

