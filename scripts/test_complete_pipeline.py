"""
Test complet du pipeline BOB-Enquête.

Vérifie que tous les scripts fonctionnent correctement.
"""

import subprocess
import sys
from pathlib import Path
from datetime import datetime


def run_script(script_name, description):
    """Exécute un script et retourne le résultat."""
    print(f"\n{'='*70}")
    print(f"TEST : {description}")
    print(f"Script : {script_name}")
    print(f"{'='*70}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print("[OK] Script execute avec succes")
            return True
        else:
            print(f"[ERREUR] Script echoue (code {result.returncode})")
            print(f"Erreur : {result.stderr[:500]}")
            return False
            
    except subprocess.TimeoutExpired:
        print("[ERREUR] Timeout (>120s)")
        return False
    except Exception as e:
        print(f"[ERREUR] {e}")
        return False


def check_output_files():
    """Vérifie que les fichiers de sortie existent."""
    print(f"\n{'='*70}")
    print("VERIFICATION DES FICHIERS DE SORTIE")
    print(f"{'='*70}")
    
    base_dir = Path(__file__).parent.parent
    
    # Fichiers à vérifier
    files_to_check = {
        'Données préparées': base_dir / 'data' / 'raw' / 'enquete_all_prepared.xlsx',
        'Marges INSEE': base_dir / 'data' / 'margins' / 'margins_center.csv',
    }
    
    # Répertoires à vérifier
    dirs_to_check = {
        'Figures': base_dir / 'outputs' / 'figures',
        'Rapports': base_dir / 'outputs' / 'reports',
    }
    
    all_ok = True
    
    # Vérifier les fichiers
    for name, path in files_to_check.items():
        if path.exists():
            size = path.stat().st_size / 1024  # KB
            print(f"[OK] {name:30s} : {path.name} ({size:.1f} KB)")
        else:
            print(f"[MANQUANT] {name:30s} : {path}")
            all_ok = False
    
    # Vérifier les répertoires
    for name, path in dirs_to_check.items():
        if path.exists():
            n_files = len(list(path.glob('*')))
            print(f"[OK] {name:30s} : {n_files} fichiers")
        else:
            print(f"[MANQUANT] {name:30s} : {path}")
            all_ok = False
    
    return all_ok


def main():
    """Fonction principale."""
    print("="*70)
    print("TEST COMPLET DU PIPELINE BOB-ENQUETE")
    print("="*70)
    print(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    scripts_dir = Path(__file__).parent
    
    # Liste des scripts à tester
    tests = [
        {
            'script': scripts_dir / 'prepare_bob_with_all_respondents.py',
            'description': 'Preparation des donnees (90 repondants)'
        },
        {
            'script': scripts_dir / 'compare_besancon_vs_hors.py',
            'description': 'Comparaison Besancon vs Hors-Besancon'
        },
        {
            'script': scripts_dir / 'analyze_interest_by_profile.py',
            'description': 'Analyse de l\'interet par profil'
        },
        {
            'script': scripts_dir / 'generate_executive_summary.py',
            'description': 'Rapport de synthese executif (PDF)'
        },
        {
            'script': scripts_dir / 'generate_enriched_report.py',
            'description': 'Rapport enrichi avec analyse par profil (PDF)'
        },
        {
            'script': scripts_dir / 'create_dashboard.py',
            'description': 'Tableau de bord interactif (visualisations)'
        }
    ]
    
    # Exécuter les tests
    results = []
    for test in tests:
        success = run_script(test['script'], test['description'])
        results.append({
            'script': test['script'].name,
            'description': test['description'],
            'success': success
        })
    
    # Vérifier les fichiers de sortie
    files_ok = check_output_files()
    
    # Résumé
    print(f"\n{'='*70}")
    print("RESUME DES TESTS")
    print(f"{'='*70}")
    
    n_success = sum(1 for r in results if r['success'])
    n_total = len(results)
    
    print(f"\nScripts testes : {n_total}")
    print(f"Succes : {n_success}")
    print(f"Echecs : {n_total - n_success}")
    
    if files_ok:
        print(f"\nFichiers de sortie : [OK]")
    else:
        print(f"\nFichiers de sortie : [MANQUANTS]")
    
    print(f"\n{'='*70}")
    
    # Détails
    print("\nDETAILS :")
    for r in results:
        status = "[OK]" if r['success'] else "[ECHEC]"
        print(f"  {status} {r['description']}")
    
    # Conclusion
    print(f"\n{'='*70}")
    if n_success == n_total and files_ok:
        print("TOUS LES TESTS SONT PASSES !")
        print("Le pipeline est operationnel.")
        return_code = 0
    else:
        print("CERTAINS TESTS ONT ECHOUE")
        print("Verifier les erreurs ci-dessus.")
        return_code = 1
    
    print(f"{'='*70}")
    
    return return_code


if __name__ == '__main__':
    sys.exit(main())

