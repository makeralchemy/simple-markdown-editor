@echo off

:: Navigate to the directory where the script is located
cd /d "%~dp0"

:: Activate the virtual environment if it exists
IF EXIST venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

:: Install dependencies
echo Installing/Verifying dependencies...
pip install -r requirements.txt

:: Run the application
echo Starting Markdown Editor...
python main.py

echo Application closed.
