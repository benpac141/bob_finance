@echo off
echo ========================================
echo Lancement de l'Application Interactive
echo Simulateur BOB - Budget
echo ========================================
echo.
echo L'application va s'ouvrir dans votre navigateur...
echo URL : http://localhost:8501
echo.
cd /d "%~dp0"
python -m streamlit run scripts/app_simulation_interactive.py
pause

