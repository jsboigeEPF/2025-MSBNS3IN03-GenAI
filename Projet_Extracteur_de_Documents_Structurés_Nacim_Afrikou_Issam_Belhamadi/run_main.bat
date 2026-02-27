@echo off
REM ============================================================
REM  run_main.bat – Exécute main.py DIRECTEMENT
REM  Démontre que main.py peut maintenant être lancé directement
REM ============================================================

cd /d "%~dp0"
echo.
echo === NAF_ISB – Extraction directe via main.py ===
echo.

python code_source\main.py

echo.
pause
