# Guide de Compilation - Application BOB

Ce guide explique comment compiler l'application Streamlit BOB en exécutable Windows autonome pour le partage avec des collègues qui n'ont pas Python installé.

## 📋 Prérequis

Pour compiler l'application, vous devez avoir :

- **Python 3.8 ou supérieur** installé
- **pip** (gestionnaire de paquets Python)
- **Accès Internet** pour télécharger les dépendances

## 🚀 Méthode 1 : Compilation Automatique (Recommandée)

La méthode la plus simple est d'utiliser le script batch fourni :

1. **Ouvrez un terminal** (Invite de commandes ou PowerShell)

2. **Naviguez vers le dossier du projet** :
   ```bash
   cd D:\python_work\bob-enquete
   ```

3. **Exécutez le script de compilation** :
   ```bash
   build_exe.bat
   ```

Le script va automatiquement :
- ✅ Vérifier que Python est installé
- ✅ Installer PyInstaller si nécessaire
- ✅ Installer toutes les dépendances
- ✅ Compiler l'application
- ✅ Créer l'exécutable dans le dossier `dist`

## 🔧 Méthode 2 : Compilation Manuelle

Si vous préférez compiler manuellement :

### Étape 1 : Installer les dépendances

```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Étape 2 : Compiler avec PyInstaller

```bash
pyinstaller build_app.spec
```

### Étape 3 : Vérifier le résultat

L'exécutable sera créé dans le dossier `dist\Simulateur_BOB.exe`

## 📦 Structure du Dossier de Distribution

Après compilation, vous trouverez dans le dossier `dist` :

```
dist/
├── Simulateur_BOB.exe          # Exécutable principal
├── _internal/                   # Fichiers internes (ne pas modifier)
│   ├── ...
│   └── (bibliothèques et dépendances)
└── data/                        # Données de l'application
    ├── raw/
    └── margins/
```

## 🎯 Partage avec les Collègues

Pour partager l'application avec vos collègues :

### Option 1 : Partage du Dossier Complet (Recommandé)

1. **Compressez tout le dossier `dist`** en ZIP :
   ```
   dist.zip contenant :
   - Simulateur_BOB.exe
   - _internal/ (dossier complet)
   - data/ (dossier complet)
   ```

2. **Partagez le fichier ZIP** avec vos collègues

3. **Vos collègues doivent** :
   - Extraire le ZIP
   - Double-cliquer sur `Simulateur_BOB.exe`
   - L'application s'ouvrira dans leur navigateur

### Option 2 : Créer un Installateur (Avancé)

Pour une expérience plus professionnelle, vous pouvez utiliser :
- **Inno Setup** (gratuit) pour créer un installateur Windows
- **NSIS** (gratuit) pour créer un installateur avec scripts personnalisés

## ⚠️ Notes Importantes

### Taille de l'Exécutable

L'exécutable final sera volumineux (environ 200-500 Mo) car il inclut :
- Python
- Toutes les bibliothèques (pandas, numpy, streamlit, plotly, etc.)
- Les données de l'application

### Antivirus et Sécurité

Certains antivirus peuvent signaler l'exécutable comme suspect car :
- Il contient un interpréteur Python compilé
- Il est créé par PyInstaller (outil connu)

**Solution** : Ajoutez une exception dans votre antivirus ou signez numériquement l'exécutable.

### Windows Defender SmartScreen

Lors du premier lancement, Windows peut afficher un avertissement :
> "Windows a protégé votre PC"

**Solution** :
1. Cliquez sur "Plus d'infos"
2. Cliquez sur "Exécuter quand même"

### Port et Firewall

L'application Streamlit utilise le port **8501** par défaut. Si ce port est bloqué :
- Le lancement peut être plus lent
- Vous pouvez modifier le port dans le code si nécessaire

## 🐛 Dépannage

### Problème : "Module not found"

**Solution** : Ajoutez le module manquant dans `hiddenimports` du fichier `build_app.spec`

### Problème : L'application ne se lance pas

1. Vérifiez les logs dans la console
2. Vérifiez que tous les fichiers de données sont présents dans `dist/data/`
3. Vérifiez que le fichier `config.yaml` est présent

### Problème : Erreur lors de la compilation

1. Vérifiez que toutes les dépendances sont installées :
   ```bash
   pip install -r requirements.txt
   ```

2. Vérifiez que PyInstaller est à jour :
   ```bash
   pip install --upgrade pyinstaller
   ```

3. Essayez de nettoyer les fichiers temporaires :
   ```bash
   rmdir /s /q build
   rmdir /s /q dist
   ```

## 📝 Modification de la Configuration

Si vous modifiez le code ou ajoutez des fichiers :

1. **Ajoutez les nouveaux fichiers** dans la section `datas` de `build_app.spec`
2. **Ajoutez les nouveaux modules** dans `hiddenimports`
3. **Recompilez** avec `build_exe.bat`

## 🔍 Vérification de la Compilation

Pour tester que l'exécutable fonctionne :

1. **Lancez l'exécutable** : `dist\Simulateur_BOB.exe`
2. **Vérifiez** que :
   - La console s'ouvre
   - Le navigateur s'ouvre automatiquement
   - L'application se charge correctement
   - Les données s'affichent correctement

## 📞 Support

En cas de problème :
1. Consultez les logs dans la console de l'exécutable
2. Vérifiez que tous les fichiers de données sont présents
3. Testez sur une machine propre sans Python installé

## ✨ Améliorations Futures Possibles

- **Créer un installateur** avec Inno Setup
- **Signer numériquement** l'exécutable pour éviter les alertes Windows
- **Optimiser la taille** en excluant les modules non utilisés
- **Créer un mode portable** avec configuration personnalisable


