@echo off
REM ============================================================
REM  run.bat – Lance l'extraction sur tous les PDF de data/input
REM  Double-cliquez sur ce fichier pour exécuter le programme.
REM ============================================================

cd /d "%~dp0"
echo.
echo === NAF_ISB – Extraction de documents ===
echo.

python -m src.main -f data/input

echo.
pause
