@echo off
echo ========================================
echo Lancement Dashboard BOB avec ngrok
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe
    pause
    exit /b 1
)

REM Lancer Streamlit en arrière-plan
echo [1/2] Lancement de Streamlit...
start "Streamlit BOB" cmd /k "cd /d %~dp0 && python -m streamlit run scripts/app_simulation_interactive.py"

REM Attendre que Streamlit démarre
timeout /t 5 /nobreak >nul

REM Vérifier si ngrok existe
if not exist "C:\ngrok\ngrok.exe" (
    echo.
    echo ATTENTION: ngrok n'est pas trouve dans C:\ngrok\
    echo.
    echo Pour utiliser ngrok:
    echo 1. Telechargez ngrok depuis https://ngrok.com/download
    echo 2. Extrayez-le dans C:\ngrok\
    echo 3. Configurez votre token: ngrok.exe authtoken VOTRE_TOKEN
    echo.
    echo L'application Streamlit est lancee sur http://localhost:8501
    echo Vous pouvez y acceder localement.
    pause
    exit /b 0
)

REM Lancer ngrok
echo [2/2] Lancement de ngrok...
start "ngrok Tunnel" cmd /k "cd /d C:\ngrok && ngrok.exe http 8501"

echo.
echo ========================================
echo Application lancee avec succes !
echo ========================================
echo.
echo Streamlit: http://localhost:8501
echo.
echo L'URL publique ngrok sera affichee dans la fenetre ngrok
echo Copiez cette URL pour la partager avec vos collegues
echo.
echo Pour arreter: Fermez les fenetres Streamlit et ngrok
echo.
pause


