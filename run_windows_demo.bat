@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Python virtual environment not found.
  echo Create it with: py -3.12 -m venv .venv
  exit /b 1
)

set "PY=.venv\Scripts\python.exe"

echo [1/4] Running automated tests...
%PY% -m pytest
if errorlevel 1 exit /b 1

echo [2/4] Running illustrative flat-panel spatial simulation...
%PY% -m pbrbiosphere.cli --config examples\configs\flat_panel_demo.json --duration-s 86400 --output-points 49 --output results\windows-demo
if errorlevel 1 exit /b 1

echo [3/4] Checking run integrity and numerical structure...
%PY% scripts\validate_spatial_run.py results\windows-demo --output results\windows-demo\validation-report.json
if errorlevel 1 exit /b 1

echo [4/4] Generating plots...
%PY% scripts\plot_spatial_run.py results\windows-demo
if errorlevel 1 exit /b 1

echo.
echo COMPLETE. Results are in results\windows-demo
start "" "results\windows-demo\spatial_profiles.png"
endlocal
