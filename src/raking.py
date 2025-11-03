"""
Implémentation de l'algorithme de raking (calage sur marges).
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class RakingWeighter:
    """
    Classe pour effectuer le redressement par raking.
    """
    
    def __init__(
        self,
        max_iterations: int = 100,
        tolerance: float = 0.001,
        min_weight: float = 0.1,
        max_weight: float = 10.0
    ):
        """
        Initialise le redresseur.
        
        Args:
            max_iterations: Nombre maximum d'itérations
            tolerance: Critère de convergence (écart relatif max)
            min_weight: Poids minimum autorisé
            max_weight: Poids maximum autorisé
        """
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.min_weight = min_weight
        self.max_weight = max_weight
        self.convergence_history = []
        self.has_converged = False
        self.n_iterations = 0
    
    def rake(
        self,
        df: pd.DataFrame,
        margins: Dict[str, pd.Series],
        weight_col: str = "weight"
    ) -> pd.DataFrame:
        """
        Effectue le raking sur les données.
        
        Args:
            df: DataFrame contenant les données
            margins: Dictionnaire {variable: marges de référence}
            weight_col: Nom de la colonne de poids
        
        Returns:
            DataFrame avec poids ajustés
        
        Raises:
            ValueError: Si les variables ne correspondent pas
        """
        df = df.copy()
        
        # Vérifier que toutes les variables sont présentes
        for var in margins.keys():
            if var not in df.columns:
                raise ValueError(f"Variable '{var}' non trouvée dans les données")
        
        logger.info("Début du raking")
        logger.info(f"  - Variables : {list(margins.keys())}")
        logger.info(f"  - Échantillon : {len(df)} observations")
        logger.info(f"  - Critères : max_iter={self.max_iterations}, tol={self.tolerance}")
        
        # Initialiser l'historique
        self.convergence_history = []
        self.has_converged = False
        
        # Itérations de raking
        for iteration in range(self.max_iterations):
            max_diff = 0.0
            
            # Pour chaque variable de redressement
            for var, target_margin in margins.items():
                # Calculer la marge actuelle
                current_margin = df.groupby(var)[weight_col].sum()
                
                # Aligner les indices
                common_index = current_margin.index.intersection(target_margin.index)
                
                if len(common_index) == 0:
                    logger.warning(
                        f"Aucune modalité commune pour '{var}' entre "
                        f"échantillon et marges"
                    )
                    continue
                
                # Calculer les facteurs d'ajustement
                adjustment_factors = target_margin[common_index] / current_margin[common_index]
                
                # Remplacer les NaN et Inf par 1
                adjustment_factors = adjustment_factors.replace([np.inf, -np.inf], 1.0)
                adjustment_factors = adjustment_factors.fillna(1.0)
                
                # Appliquer les ajustements
                df[weight_col] = df[var].map(adjustment_factors) * df[weight_col]
                
                # Calculer l'écart maximum
                relative_diff = np.abs(adjustment_factors - 1.0).max()
                max_diff = max(max_diff, relative_diff)
            
            # Appliquer les limites de poids
            df[weight_col] = df[weight_col].clip(self.min_weight, self.max_weight)
            
            # Enregistrer la convergence
            self.convergence_history.append(max_diff)
            
            # Vérifier la convergence
            if max_diff < self.tolerance:
                self.has_converged = True
                self.n_iterations = iteration + 1
                logger.info(f"Convergence atteinte après {self.n_iterations} itérations")
                logger.info(f"  - Écart final : {max_diff:.6f}")
                break
        
        if not self.has_converged:
            self.n_iterations = self.max_iterations
            logger.warning(
                f"Convergence non atteinte après {self.max_iterations} itérations"
            )
            logger.warning(f"  - Écart final : {max_diff:.6f}")
        
        # Afficher les statistiques des poids
        self._log_weight_statistics(df[weight_col])
        
        return df
    
    def _log_weight_statistics(self, weights: pd.Series) -> None:
        """
        Affiche les statistiques des poids.
        
        Args:
            weights: Series des poids
        """
        logger.info("Statistiques des poids :")
        logger.info(f"  - Minimum : {weights.min():.3f}")
        logger.info(f"  - Q1 : {weights.quantile(0.25):.3f}")
        logger.info(f"  - Médiane : {weights.median():.3f}")
        logger.info(f"  - Moyenne : {weights.mean():.3f}")
        logger.info(f"  - Q3 : {weights.quantile(0.75):.3f}")
        logger.info(f"  - Maximum : {weights.max():.3f}")
        logger.info(f"  - Écart-type : {weights.std():.3f}")
    
    def check_margins_quality(
        self,
        df: pd.DataFrame,
        margins: Dict[str, pd.Series],
        weight_col: str = "weight"
    ) -> pd.DataFrame:
        """
        Vérifie la qualité du calage sur marges.
        
        Args:
            df: DataFrame avec poids ajustés
            margins: Marges de référence
            weight_col: Nom de la colonne de poids
        
        Returns:
            DataFrame avec les écarts par variable et modalité
        """
        results = []
        
        for var, target_margin in margins.items():
            # Calculer la marge obtenue
            obtained_margin = df.groupby(var)[weight_col].sum()
            
            # Aligner les indices
            common_index = obtained_margin.index.intersection(target_margin.index)
            
            for modality in common_index:
                target = target_margin[modality]
                obtained = obtained_margin[modality]
                abs_diff = obtained - target
                rel_diff = abs_diff / target if target > 0 else 0
                
                results.append({
                    'variable': var,
                    'modalite': modality,
                    'cible': target,
                    'obtenu': obtained,
                    'ecart_absolu': abs_diff,
                    'ecart_relatif': rel_diff
                })
        
        results_df = pd.DataFrame(results)
        
        # Afficher un résumé
        logger.info("Qualité du calage :")
        for var in margins.keys():
            var_results = results_df[results_df['variable'] == var]
            max_rel_diff = var_results['ecart_relatif'].abs().max()
            logger.info(f"  - {var} : écart relatif max = {max_rel_diff:.4f}")
        
        return results_df


def compare_distributions(
    df: pd.DataFrame,
    variable: str,
    weight_col: str = "weight",
    initial_weight_col: str = None
) -> pd.DataFrame:
    """
    Compare les distributions avant et après redressement.
    
    Args:
        df: DataFrame
        variable: Variable à comparer
        weight_col: Colonne des poids finaux
        initial_weight_col: Colonne des poids initiaux (si None, utilise 1)
    
    Returns:
        DataFrame avec les distributions
    """
    # Distribution initiale (effectifs bruts)
    initial_dist = df.groupby(variable).size()
    
    # Distribution avec poids initiaux
    if initial_weight_col is None:
        # Si pas de poids initiaux, utiliser les effectifs bruts
        initial_weighted = initial_dist.copy()
    else:
        initial_weighted = df.groupby(variable)[initial_weight_col].sum()
    
    # Distribution finale (avec poids finaux)
    final_weighted = df.groupby(variable)[weight_col].sum()
    
    # Créer le DataFrame de comparaison
    comparison = pd.DataFrame({
        'effectif_brut': initial_dist,
        'pct_brut': initial_dist / initial_dist.sum() * 100,
        'effectif_initial': initial_weighted,
        'pct_initial': initial_weighted / initial_weighted.sum() * 100,
        'effectif_final': final_weighted,
        'pct_final': final_weighted / final_weighted.sum() * 100
    })
    
    comparison['diff_pct'] = comparison['pct_final'] - comparison['pct_initial']
    
    return comparison

