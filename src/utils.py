"""
Fonctions utilitaires pour le projet d'analyse d'enquête.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any


def setup_logging(log_file: str = None, level: str = "INFO") -> logging.Logger:
    """
    Configure le système de logging.
    
    Args:
        log_file: Chemin du fichier de log (optionnel)
        level: Niveau de logging (DEBUG, INFO, WARNING, ERROR)
    
    Returns:
        Logger configuré
    """
    log_level = getattr(logging, level.upper(), logging.INFO)
    
    # Configuration de base
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger = logging.getLogger(__name__)
    
    # Ajout d'un handler fichier si spécifié
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
    """
    Charge le fichier de configuration YAML.
    
    Args:
        config_path: Chemin vers le fichier de configuration
    
    Returns:
        Dictionnaire contenant la configuration
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        yaml.YAMLError: Si le fichier est mal formaté
    """
    config_file = Path(config_path)
    
    if not config_file.exists():
        raise FileNotFoundError(f"Fichier de configuration non trouvé : {config_path}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def validate_config(config: Dict[str, Any]) -> bool:
    """
    Valide la structure du fichier de configuration.
    
    Args:
        config: Dictionnaire de configuration
    
    Returns:
        True si la configuration est valide
    
    Raises:
        ValueError: Si la configuration est invalide
    """
    required_sections = ['paths', 'survey', 'raking', 'margins']
    
    for section in required_sections:
        if section not in config:
            raise ValueError(f"Section manquante dans la configuration : {section}")
    
    # Validation des chemins
    required_paths = ['raw_data', 'margins', 'output_figures', 'output_reports']
    for path_key in required_paths:
        if path_key not in config['paths']:
            raise ValueError(f"Chemin manquant dans la configuration : {path_key}")
    
    # Validation des paramètres de l'enquête
    if 'weighting_vars' not in config['survey']:
        raise ValueError("Variables de redressement non spécifiées")
    
    if 'id_column' not in config['survey']:
        raise ValueError("Colonne d'identifiant non spécifiée")
    
    return True


def create_output_dirs(config: Dict[str, Any]) -> None:
    """
    Crée les répertoires de sortie s'ils n'existent pas.
    
    Args:
        config: Dictionnaire de configuration
    """
    output_dirs = [
        config['paths']['output_figures'],
        config['paths']['output_reports']
    ]
    
    for dir_path in output_dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)


def format_number(value: float, decimals: int = 2) -> str:
    """
    Formate un nombre avec le nombre de décimales spécifié.
    
    Args:
        value: Valeur à formater
        decimals: Nombre de décimales
    
    Returns:
        Chaîne formatée
    """
    return f"{value:,.{decimals}f}".replace(',', ' ')


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Formate un pourcentage.
    
    Args:
        value: Valeur (entre 0 et 1)
        decimals: Nombre de décimales
    
    Returns:
        Chaîne formatée avec le symbole %
    """
    return f"{value * 100:.{decimals}f}%"

