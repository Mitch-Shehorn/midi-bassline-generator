@echo off
echo Checking Python environment...

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Display Python version and environment info
python --version
echo.
echo Python executable location:
where python
echo.
echo Installed packages:
pip list
echo.

:: Run verification script
python verify_setup.py

echo.
echo Choose program to run:
echo 1. GUI Version
echo 2. Command-line Version
echo 3. Exit

set /p choice="Enter choice (1-3): "

if "%choice%"=="1" (
    echo Starting GUI version...
    python src/gui_main.py
) else if "%choice%"=="2" (
    echo Starting command-line version...
    python src/main_program.py
) else if "%choice%"=="3" (
    echo Exiting...
    exit /b
) else (
    echo Invalid choice
)

pause
