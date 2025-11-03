"""
Module de chargement et nettoyage des données d'enquête.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Any
import logging

logger = logging.getLogger(__name__)


def load_survey_data(
    file_path: str,
    sheet_name: str = "Enquete",
    **kwargs
) -> pd.DataFrame:
    """
    Charge les données d'enquête depuis un fichier Excel.
    
    Args:
        file_path: Chemin vers le fichier Excel
        sheet_name: Nom de la feuille à charger
        **kwargs: Arguments supplémentaires pour pd.read_excel
    
    Returns:
        DataFrame contenant les données
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si la feuille n'existe pas
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier non trouvé : {file_path}")
    
    logger.info(f"Chargement des données depuis {file_path}")
    
    try:
        df = pd.read_excel(file_path, sheet_name=sheet_name, **kwargs)
        logger.info(f"Données chargées : {len(df)} lignes, {len(df.columns)} colonnes")
        return df
    except Exception as e:
        logger.error(f"Erreur lors du chargement : {e}")
        raise


def load_margins(file_path: str) -> pd.DataFrame:
    """
    Charge les marges de référence depuis un fichier CSV.
    
    Args:
        file_path: Chemin vers le fichier CSV
    
    Returns:
        DataFrame contenant les marges
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        raise FileNotFoundError(f"Fichier de marges non trouvé : {file_path}")
    
    logger.info(f"Chargement des marges depuis {file_path}")
    
    df = pd.read_csv(file_path)
    logger.info(f"Marges chargées : {len(df)} lignes")
    
    return df


def validate_survey_data(
    df: pd.DataFrame,
    required_columns: List[str],
    id_column: str
) -> Tuple[bool, List[str]]:
    """
    Valide les données d'enquête.
    
    Args:
        df: DataFrame à valider
        required_columns: Liste des colonnes requises
        id_column: Nom de la colonne identifiant
    
    Returns:
        Tuple (is_valid, errors) où errors est une liste des erreurs détectées
    """
    errors = []
    
    # Vérifier les colonnes manquantes
    missing_cols = set(required_columns) - set(df.columns)
    if missing_cols:
        errors.append(f"Colonnes manquantes : {', '.join(missing_cols)}")
    
    # Vérifier l'identifiant
    if id_column not in df.columns:
        errors.append(f"Colonne identifiant manquante : {id_column}")
    elif df[id_column].duplicated().any():
        n_duplicates = df[id_column].duplicated().sum()
        errors.append(f"Identifiants dupliqués : {n_duplicates} doublons")
    
    # Vérifier les valeurs manquantes
    for col in required_columns:
        if col in df.columns:
            n_missing = df[col].isna().sum()
            if n_missing > 0:
                pct_missing = n_missing / len(df) * 100
                errors.append(
                    f"Valeurs manquantes dans '{col}' : {n_missing} ({pct_missing:.1f}%)"
                )
    
    is_valid = len(errors) == 0
    
    if is_valid:
        logger.info("Validation des données : OK")
    else:
        logger.warning(f"Validation des données : {len(errors)} erreur(s) détectée(s)")
        for error in errors:
            logger.warning(f"  - {error}")
    
    return is_valid, errors


def clean_survey_data(
    df: pd.DataFrame,
    weighting_vars: List[str],
    drop_missing: bool = True
) -> pd.DataFrame:
    """
    Nettoie les données d'enquête.
    
    Args:
        df: DataFrame à nettoyer
        weighting_vars: Variables de redressement
        drop_missing: Si True, supprime les lignes avec valeurs manquantes
    
    Returns:
        DataFrame nettoyé
    """
    df_clean = df.copy()
    n_initial = len(df_clean)
    
    logger.info(f"Nettoyage des données : {n_initial} lignes initiales")
    
    # Supprimer les doublons
    df_clean = df_clean.drop_duplicates()
    n_after_duplicates = len(df_clean)
    if n_after_duplicates < n_initial:
        logger.info(f"  - {n_initial - n_after_duplicates} doublons supprimés")
    
    # Traiter les valeurs manquantes
    if drop_missing:
        df_clean = df_clean.dropna(subset=weighting_vars)
        n_after_missing = len(df_clean)
        if n_after_missing < n_after_duplicates:
            logger.info(
                f"  - {n_after_duplicates - n_after_missing} lignes avec "
                f"valeurs manquantes supprimées"
            )
    
    logger.info(f"Nettoyage terminé : {len(df_clean)} lignes conservées")
    
    return df_clean


def prepare_margins_dict(
    margins_df: pd.DataFrame,
    weighting_vars: List[str],
    population_col: str = "population"
) -> Dict[str, pd.Series]:
    """
    Prépare un dictionnaire de marges pour le raking.
    
    Args:
        margins_df: DataFrame contenant les marges
        weighting_vars: Variables de redressement
        population_col: Nom de la colonne contenant les effectifs
    
    Returns:
        Dictionnaire {variable: Series des marges}
    """
    margins_dict = {}
    
    for var in weighting_vars:
        if var not in margins_df.columns:
            logger.warning(f"Variable '{var}' non trouvée dans les marges")
            continue
        
        # Agréger les marges par modalité
        margin = margins_df.groupby(var)[population_col].sum()
        margins_dict[var] = margin
        
        logger.info(f"Marges pour '{var}' : {len(margin)} modalités, "
                   f"total = {margin.sum():,.0f}")
    
    return margins_dict


def add_initial_weights(
    df: pd.DataFrame,
    weight_col: str = "weight",
    initial_value: float = 1.0
) -> pd.DataFrame:
    """
    Ajoute une colonne de poids initiaux au DataFrame.
    
    Args:
        df: DataFrame
        weight_col: Nom de la colonne de poids
        initial_value: Valeur initiale des poids
    
    Returns:
        DataFrame avec colonne de poids
    """
    df = df.copy()
    df[weight_col] = initial_value
    return df

