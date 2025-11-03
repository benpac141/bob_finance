"""
Script de test rapide du pipeline bob-enquete.

Ce script vérifie que tous les modules peuvent être importés
et que la structure est correcte.
"""

import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

def test_imports():
    """Test des imports de tous les modules."""
    print("[TEST] Imports...")
    
    try:
        import utils
        print("  [OK] utils")
    except ImportError as e:
        print(f"  [ERREUR] utils : {e}")
        return False
    
    try:
        import load_clean
        print("  [OK] load_clean")
    except ImportError as e:
        print(f"  [ERREUR] load_clean : {e}")
        return False
    
    try:
        import raking
        print("  [OK] raking")
    except ImportError as e:
        print(f"  [ERREUR] raking : {e}")
        return False
    
    try:
        import analysis
        print("  [OK] analysis")
    except ImportError as e:
        print(f"  [ERREUR] analysis : {e}")
        return False
    
    try:
        import report_pdf
        print("  [OK] report_pdf")
    except ImportError as e:
        print(f"  [ERREUR] report_pdf : {e}")
        return False
    
    try:
        import pdf_report
        print("  [OK] pdf_report")
    except ImportError as e:
        print(f"  [ERREUR] pdf_report : {e}")
        return False
    
    try:
        import cli
        print("  [OK] cli")
    except ImportError as e:
        print(f"  [ERREUR] cli : {e}")
        return False
    
    return True


def test_structure():
    """Test de la structure des répertoires."""
    print("\n[TEST] Structure...")
    
    base_dir = Path(__file__).parent.parent
    
    required_dirs = [
        'data/raw',
        'data/margins',
        'outputs/figures',
        'outputs/reports',
        'src',
        'scripts'
    ]
    
    all_ok = True
    for dir_path in required_dirs:
        full_path = base_dir / dir_path
        if full_path.exists():
            print(f"  [OK] {dir_path}")
        else:
            print(f"  [ERREUR] {dir_path} (manquant)")
            all_ok = False
    
    return all_ok


def test_config():
    """Test du fichier de configuration."""
    print("\n[TEST] Configuration...")
    
    base_dir = Path(__file__).parent.parent
    config_file = base_dir / 'config.yaml'
    
    if not config_file.exists():
        print("  [ERREUR] config.yaml manquant")
        return False
    
    print("  [OK] config.yaml existe")
    
    # Tenter de charger la config
    sys.path.insert(0, str(base_dir / 'src'))
    try:
        from utils import load_config, validate_config
        config = load_config(str(config_file))
        validate_config(config)
        print("  [OK] Configuration valide")
        return True
    except Exception as e:
        print(f"  [ERREUR] Erreur de configuration : {e}")
        return False


def test_data_files():
    """Test de la présence des fichiers de données."""
    print("\n[TEST] Fichiers de donnees...")
    
    base_dir = Path(__file__).parent.parent
    
    margins_file = base_dir / 'data' / 'margins' / 'margins_center.csv'
    if margins_file.exists():
        print("  [OK] margins_center.csv existe")
    else:
        print("  [WARN] margins_center.csv manquant (normal si pas encore cree)")
    
    # Chercher un fichier d'enquête
    raw_dir = base_dir / 'data' / 'raw'
    excel_files = list(raw_dir.glob('*.xlsx'))
    
    if excel_files:
        print(f"  [OK] Fichier(s) d'enquete trouve(s) : {[f.name for f in excel_files]}")
        return True
    else:
        print("  [WARN] Aucun fichier .xlsx dans data/raw/ (executez generate_sample_data.py)")
        return False


def main():
    """Fonction principale."""
    print("=" * 60)
    print("TEST DU PIPELINE BOB-ENQUETE")
    print("=" * 60)
    
    results = []
    
    # Tests
    results.append(("Imports", test_imports()))
    results.append(("Structure", test_structure()))
    results.append(("Configuration", test_config()))
    results.append(("Données", test_data_files()))
    
    # Résumé
    print("\n" + "=" * 60)
    print("RÉSUMÉ")
    print("=" * 60)
    
    for test_name, result in results:
        status = "[OK]" if result else "[ECHEC]"
        print(f"{test_name:20s} : {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("[OK] TOUS LES TESTS SONT PASSES !")
        print("\nVous pouvez maintenant :")
        print("1. Generer des donnees : python scripts/generate_sample_data.py")
        print("2. Lancer l'analyse : python src/cli.py run --config config.yaml")
    else:
        print("[ERREUR] CERTAINS TESTS ONT ECHOUE")
        print("\nVerifiez les erreurs ci-dessus et :")
        print("1. Installez les dependances : pip install -r requirements.txt")
        print("2. Verifiez la structure du projet")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())

