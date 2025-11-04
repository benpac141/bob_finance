@echo off
echo ========================================
echo Compilation de l'application BOB
echo en exécutable Windows autonome
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou pas dans le PATH
    pause
    exit /b 1
)

echo [1/4] Vérification de PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller n'est pas installé. Installation...
    pip install pyinstaller
    if errorlevel 1 (
        echo ERREUR: Impossible d'installer PyInstaller
        pause
        exit /b 1
    )
)

echo [2/4] Vérification des dépendances...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERREUR: Impossible d'installer les dépendances
    pause
    exit /b 1
)

echo [3/4] Nettoyage des anciens builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist Simulateur_BOB.spec del /q Simulateur_BOB.spec

echo [4/4] Compilation avec PyInstaller...
pyinstaller build_app.spec

if errorlevel 1 (
    echo.
    echo ERREUR lors de la compilation
    pause
    exit /b 1
)

echo.
echo ========================================
echo Compilation terminée avec succes !
echo ========================================
echo.
echo L'executable se trouve dans : dist\Simulateur_BOB.exe
echo.
echo Vous pouvez maintenant :
echo 1. Tester l'executable : dist\Simulateur_BOB.exe
echo 2. Partager le dossier "dist" avec vos collegues
echo.
pause


