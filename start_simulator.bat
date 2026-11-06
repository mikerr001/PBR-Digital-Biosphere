@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo ERROR: Python virtual environment not found.
  echo Run: py -3.12 -m venv .venv
  echo Then activate it and run: pip install -e ".[dev]"
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -m pbrbiosphere.desktop_app
if errorlevel 1 pause
endlocal
