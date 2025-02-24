@echo off
:: Activate virtual environment and run GUI
call venv\Scripts\activate.bat
python src/gui_main.py
pause
