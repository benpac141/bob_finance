"""
Module d'analyse statistique des données pondérées.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


def weighted_frequency(
    df: pd.DataFrame,
    variable: str,
    weight_col: str = "weight"
) -> pd.DataFrame:
    """
    Calcule la distribution de fréquence pondérée.
    
    Args:
        df: DataFrame
        variable: Variable à analyser
        weight_col: Colonne des poids
    
    Returns:
        DataFrame avec effectifs et pourcentages pondérés
    """
    freq = df.groupby(variable)[weight_col].sum()
    total = freq.sum()
    
    result = pd.DataFrame({
        'effectif': freq,
        'pourcentage': freq / total * 100
    })
    
    result = result.sort_values('effectif', ascending=False)
    
    return result


def weighted_crosstab(
    df: pd.DataFrame,
    var1: str,
    var2: str,
    weight_col: str = "weight",
    normalize: str = None
) -> pd.DataFrame:
    """
    Calcule un tableau croisé pondéré.
    
    Args:
        df: DataFrame
        var1: Première variable (lignes)
        var2: Deuxième variable (colonnes)
        weight_col: Colonne des poids
        normalize: 'index', 'columns', 'all', ou None
    
    Returns:
        DataFrame du tableau croisé
    """
    # Créer le tableau croisé
    crosstab = df.groupby([var1, var2])[weight_col].sum().unstack(fill_value=0)
    
    # Normaliser si demandé
    if normalize == 'index':
        crosstab = crosstab.div(crosstab.sum(axis=1), axis=0) * 100
    elif normalize == 'columns':
        crosstab = crosstab.div(crosstab.sum(axis=0), axis=1) * 100
    elif normalize == 'all':
        crosstab = crosstab / crosstab.sum().sum() * 100
    
    return crosstab


def weighted_mean(
    df: pd.DataFrame,
    variable: str,
    weight_col: str = "weight"
) -> float:
    """
    Calcule la moyenne pondérée.
    
    Args:
        df: DataFrame
        variable: Variable numérique
        weight_col: Colonne des poids
    
    Returns:
        Moyenne pondérée
    """
    return np.average(df[variable], weights=df[weight_col])


def weighted_std(
    df: pd.DataFrame,
    variable: str,
    weight_col: str = "weight"
) -> float:
    """
    Calcule l'écart-type pondéré.
    
    Args:
        df: DataFrame
        variable: Variable numérique
        weight_col: Colonne des poids
    
    Returns:
        Écart-type pondéré
    """
    mean = weighted_mean(df, variable, weight_col)
    variance = np.average((df[variable] - mean) ** 2, weights=df[weight_col])
    return np.sqrt(variance)


def weighted_quantile(
    df: pd.DataFrame,
    variable: str,
    quantile: float,
    weight_col: str = "weight"
) -> float:
    """
    Calcule un quantile pondéré.
    
    Args:
        df: DataFrame
        variable: Variable numérique
        quantile: Quantile à calculer (entre 0 et 1)
        weight_col: Colonne des poids
    
    Returns:
        Valeur du quantile
    """
    # Trier par valeur
    df_sorted = df.sort_values(variable)
    
    # Calculer les poids cumulés
    cumsum = df_sorted[weight_col].cumsum()
    total = df_sorted[weight_col].sum()
    
    # Trouver le quantile
    target = quantile * total
    idx = (cumsum >= target).idxmax()
    
    return df_sorted.loc[idx, variable]


def weighted_statistics(
    df: pd.DataFrame,
    variable: str,
    weight_col: str = "weight"
) -> Dict[str, float]:
    """
    Calcule des statistiques descriptives pondérées.
    
    Args:
        df: DataFrame
        variable: Variable numérique
        weight_col: Colonne des poids
    
    Returns:
        Dictionnaire de statistiques
    """
    stats = {
        'count': len(df),
        'sum_weights': df[weight_col].sum(),
        'mean': weighted_mean(df, variable, weight_col),
        'std': weighted_std(df, variable, weight_col),
        'min': df[variable].min(),
        'q25': weighted_quantile(df, variable, 0.25, weight_col),
        'median': weighted_quantile(df, variable, 0.50, weight_col),
        'q75': weighted_quantile(df, variable, 0.75, weight_col),
        'max': df[variable].max()
    }
    
    return stats


def analyze_by_group(
    df: pd.DataFrame,
    variable: str,
    group_by: str,
    weight_col: str = "weight",
    stat_func: str = "mean"
) -> pd.DataFrame:
    """
    Analyse une variable par groupes.
    
    Args:
        df: DataFrame
        variable: Variable à analyser
        group_by: Variable de regroupement
        weight_col: Colonne des poids
        stat_func: Fonction statistique ('mean', 'sum', 'count')
    
    Returns:
        DataFrame avec les statistiques par groupe
    """
    results = []
    
    for group_value in df[group_by].unique():
        df_group = df[df[group_by] == group_value]
        
        if stat_func == "mean":
            value = weighted_mean(df_group, variable, weight_col)
        elif stat_func == "sum":
            value = df_group[weight_col].sum()
        elif stat_func == "count":
            value = len(df_group)
        else:
            raise ValueError(f"Fonction non supportée : {stat_func}")
        
        results.append({
            group_by: group_value,
            variable: value,
            'effectif': len(df_group),
            'poids_total': df_group[weight_col].sum()
        })
    
    return pd.DataFrame(results).sort_values(variable, ascending=False)


def compare_groups(
    df: pd.DataFrame,
    variable: str,
    group_var: str,
    weight_col: str = "weight"
) -> pd.DataFrame:
    """
    Compare les distributions d'une variable entre groupes.
    
    Args:
        df: DataFrame
        variable: Variable à comparer
        group_var: Variable de groupement
        weight_col: Colonne des poids
    
    Returns:
        DataFrame de comparaison
    """
    results = []
    
    for group in df[group_var].unique():
        df_group = df[df[group_var] == group]
        
        # Calculer les statistiques pour ce groupe
        stats = weighted_statistics(df_group, variable, weight_col)
        stats[group_var] = group
        
        results.append(stats)
    
    comparison_df = pd.DataFrame(results)
    
    # Réorganiser les colonnes
    cols = [group_var] + [col for col in comparison_df.columns if col != group_var]
    comparison_df = comparison_df[cols]
    
    return comparison_df


def calculate_design_effect(weights: pd.Series) -> float:
    """
    Calcule l'effet de plan (Design Effect - Deff).
    
    Le Deff mesure l'augmentation de la variance due au plan de sondage.
    Deff = 1 + CV²(weights) où CV est le coefficient de variation.
    
    Args:
        weights: Series des poids
    
    Returns:
        Effet de plan (Deff)
    """
    n = len(weights)
    mean_weight = weights.mean()
    
    if mean_weight == 0:
        return np.nan
    
    # Coefficient de variation au carré
    cv_squared = (weights.std() / mean_weight) ** 2
    
    deff = 1 + cv_squared
    
    return deff


def calculate_effective_sample_size(weights: pd.Series) -> float:
    """
    Calcule la taille d'échantillon effective (n_eff).
    
    n_eff = (Σw)² / Σ(w²)
    
    Représente la taille d'un échantillon aléatoire simple qui donnerait
    la même précision que l'échantillon pondéré.
    
    Args:
        weights: Series des poids
    
    Returns:
        Taille d'échantillon effective
    """
    sum_weights = weights.sum()
    sum_weights_squared = (weights ** 2).sum()
    
    if sum_weights_squared == 0:
        return np.nan
    
    n_eff = (sum_weights ** 2) / sum_weights_squared
    
    return n_eff


def quality_metrics(weights: pd.Series) -> Dict[str, float]:
    """
    Calcule les métriques de qualité du redressement.
    
    Args:
        weights: Series des poids
    
    Returns:
        Dictionnaire avec Deff, n_eff, CV, etc.
    """
    n = len(weights)
    mean_weight = weights.mean()
    std_weight = weights.std()
    
    deff = calculate_design_effect(weights)
    n_eff = calculate_effective_sample_size(weights)
    
    cv = std_weight / mean_weight if mean_weight > 0 else np.nan
    
    metrics = {
        'n_observations': n,
        'mean_weight': mean_weight,
        'std_weight': std_weight,
        'cv_weight': cv,
        'min_weight': weights.min(),
        'max_weight': weights.max(),
        'deff': deff,
        'n_eff': n_eff,
        'loss_efficiency': (1 - n_eff / n) * 100  # % de perte d'efficacité
    }
    
    return metrics


def create_summary_report(
    df: pd.DataFrame,
    variables: List[str],
    weight_col: str = "weight"
) -> pd.DataFrame:
    """
    Crée un rapport récapitulatif pour plusieurs variables.
    
    Args:
        df: DataFrame
        variables: Liste des variables à analyser
        weight_col: Colonne des poids
    
    Returns:
        DataFrame récapitulatif
    """
    summary = []
    
    for var in variables:
        if var not in df.columns:
            logger.warning(f"Variable '{var}' non trouvée")
            continue
        
        # Déterminer le type de variable
        if pd.api.types.is_numeric_dtype(df[var]):
            # Variable numérique
            stats = weighted_statistics(df, var, weight_col)
            stats['variable'] = var
            stats['type'] = 'numérique'
            summary.append(stats)
        else:
            # Variable catégorielle
            n_categories = df[var].nunique()
            most_common = df.groupby(var)[weight_col].sum().idxmax()
            
            summary.append({
                'variable': var,
                'type': 'catégorielle',
                'n_categories': n_categories,
                'most_common': most_common,
                'count': len(df),
                'sum_weights': df[weight_col].sum()
            })
    
    return pd.DataFrame(summary)

