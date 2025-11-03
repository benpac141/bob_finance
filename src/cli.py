"""
Interface en ligne de commande pour bob-enquete.
"""

import click
import logging
from pathlib import Path
from datetime import datetime

from utils import load_config, validate_config, create_output_dirs, setup_logging
from load_clean import (
    load_survey_data, load_margins, validate_survey_data,
    clean_survey_data, prepare_margins_dict, add_initial_weights
)
from raking import RakingWeighter, compare_distributions
from analysis import (
    weighted_frequency, weighted_statistics, create_summary_report,
    compare_groups
)
from report_pdf import (
    plot_weight_distribution, plot_convergence, plot_comparison_distribution,
    plot_frequency, generate_html_report
)
from pdf_report import generate_global_report, generate_subgroup_report
from analysis import quality_metrics


@click.group()
def cli():
    """Bob-Enquête : Outil d'analyse et de redressement d'enquêtes."""
    pass


@cli.command()
@click.option('--config', default='config.yaml', help='Chemin du fichier de configuration')
def run(config):
    """Exécute l'analyse complète."""
    
    # Configuration du logging
    logger = setup_logging(level="INFO")
    logger.info("=" * 60)
    logger.info("BOB-ENQUETE - Analyse complète")
    logger.info("=" * 60)
    
    try:
        # 1. Charger la configuration
        logger.info("\n[1/7] Chargement de la configuration")
        cfg = load_config(config)
        validate_config(cfg)
        create_output_dirs(cfg)
        
        # 2. Charger les données
        logger.info("\n[2/7] Chargement des données")
        df = load_survey_data(
            cfg['paths']['raw_data'],
            cfg['survey'].get('sheet_name', 'Enquete')
        )
        
        margins_df = load_margins(cfg['paths']['margins'])
        
        # 3. Valider et nettoyer
        logger.info("\n[3/7] Validation et nettoyage")
        required_cols = (
            cfg['survey']['weighting_vars'] + 
            [cfg['survey']['id_column'], cfg['margins']['geo_id_column']]
        )
        
        is_valid, errors = validate_survey_data(df, required_cols, cfg['survey']['id_column'])
        
        if not is_valid:
            logger.warning("Attention : des problèmes ont été détectés dans les données")
        
        df_clean = clean_survey_data(df, cfg['survey']['weighting_vars'])
        df_clean = add_initial_weights(df_clean, initial_value=cfg['raking']['initial_weight'])
        
        # 4. Préparer les marges
        logger.info("\n[4/7] Préparation des marges")
        margins_dict = prepare_margins_dict(
            margins_df,
            cfg['survey']['weighting_vars']
        )
        
        # 5. Effectuer le raking
        logger.info("\n[5/7] Redressement par raking")
        weighter = RakingWeighter(
            max_iterations=cfg['raking']['max_iterations'],
            tolerance=cfg['raking']['tolerance'],
            min_weight=cfg['raking']['min_weight'],
            max_weight=cfg['raking']['max_weight']
        )
        
        df_weighted = weighter.rake(df_clean, margins_dict)
        
        # Vérifier la qualité
        quality_df = weighter.check_margins_quality(df_weighted, margins_dict)
        
        # 6. Analyses
        logger.info("\n[6/7] Analyses statistiques")
        
        # Créer les graphiques
        figures_dir = Path(cfg['paths']['output_figures'])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Distribution des poids
        plot_weight_distribution(
            df_weighted['weight'],
            figures_dir / f'weights_distribution_{timestamp}.png'
        )
        
        # Convergence
        plot_convergence(
            weighter.convergence_history,
            figures_dir / f'convergence_{timestamp}.png',
            tolerance=cfg['raking']['tolerance']
        )
        
        # Comparaisons avant/après pour chaque variable
        for var in cfg['survey']['weighting_vars']:
            comparison = compare_distributions(df_weighted, var)
            plot_comparison_distribution(
                comparison,
                var,
                figures_dir / f'comparison_{var}_{timestamp}.png'
            )
        
        # Analyses des variables d'intérêt
        if 'variables_of_interest' in cfg.get('analysis', {}):
            for var in cfg['analysis']['variables_of_interest']:
                if var in df_weighted.columns:
                    freq = weighted_frequency(df_weighted, var)
                    plot_frequency(
                        freq,
                        var,
                        figures_dir / f'freq_{var}_{timestamp}.png',
                        top_n=10
                    )
        
        # 7. Générer les rapports
        logger.info("\n[7/7] Génération des rapports")
        
        # Calculer les métriques de qualité
        qm = quality_metrics(df_weighted['weight'])
        logger.info(f"  - Deff = {qm['deff']:.3f}")
        logger.info(f"  - n_eff = {qm['n_eff']:.0f}")
        logger.info(f"  - Perte d'efficacité = {qm['loss_efficiency']:.1f}%")
        
        # Rapport global PDF
        report_global_path = Path(cfg['paths']['output_reports']) / f'rapport_global_{timestamp}.pdf'
        generate_global_report(
            df_weighted,
            qm,
            quality_df,
            figures_dir,
            report_global_path,
            cfg
        )
        
        # Rapport HTML (léger)
        results = {
            'n_respondents': len(df_weighted),
            'n_weighting_vars': len(cfg['survey']['weighting_vars']),
            'converged': weighter.has_converged,
            'n_iterations': weighter.n_iterations
        }
        
        report_html_path = Path(cfg['paths']['output_reports']) / f'report_{timestamp}.html'
        generate_html_report(cfg, results, report_html_path)
        
        # Rapports par sous-groupes (si configurés)
        if 'subgroups' in cfg.get('analysis', {}):
            logger.info("  - Génération des rapports par sous-groupes")
            
            for subgroup_config in cfg['analysis']['subgroups']:
                subgroup_name = subgroup_config['name']
                filter_var = subgroup_config['filter_variable']
                filter_value = subgroup_config['filter_value']
                
                # Filtrer les données
                filter_condition = df_weighted[filter_var] == filter_value
                df_sub = df_weighted[filter_condition]
                
                if len(df_sub) > 0:
                    # Métriques de qualité pour ce sous-groupe
                    qm_sub = quality_metrics(df_sub['weight'])
                    
                    # Générer le rapport
                    report_sub_path = Path(cfg['paths']['output_reports']) / f'rapport_{subgroup_name}_{timestamp}.pdf'
                    generate_subgroup_report(
                        df_weighted,
                        filter_condition,
                        subgroup_name,
                        qm_sub,
                        figures_dir,
                        report_sub_path,
                        cfg
                    )
                    logger.info(f"    • Rapport '{subgroup_name}' généré")
                else:
                    logger.warning(f"    • Aucune donnée pour le sous-groupe '{subgroup_name}'")
        
        # Sauvegarder les données pondérées
        output_data_path = Path(cfg['paths']['output_reports']) / f'data_weighted_{timestamp}.csv'
        df_weighted.to_csv(output_data_path, index=False, encoding='utf-8-sig')
        logger.info(f"Données pondérées sauvegardées : {output_data_path}")
        
        # Sauvegarder la qualité du calage
        quality_path = Path(cfg['paths']['output_reports']) / f'quality_{timestamp}.csv'
        quality_df.to_csv(quality_path, index=False, encoding='utf-8-sig')
        logger.info(f"Qualité du calage sauvegardée : {quality_path}")
        
        logger.info("\n" + "=" * 60)
        logger.info("ANALYSE TERMINÉE AVEC SUCCÈS")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"\nERREUR : {e}", exc_info=True)
        raise click.ClickException(str(e))


@cli.command()
@click.option('--config', default='config.yaml', help='Chemin du fichier de configuration')
def analyze(config):
    """Exécute uniquement l'analyse (sans redressement)."""
    click.echo("Analyse en cours...")
    # À implémenter si besoin


@cli.command()
@click.option('--config', default='config.yaml', help='Chemin du fichier de configuration')
def report(config):
    """Génère uniquement le rapport."""
    click.echo("Génération du rapport...")
    # À implémenter si besoin


if __name__ == '__main__':
    cli()

