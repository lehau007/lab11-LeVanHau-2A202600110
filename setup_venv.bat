@echo off
REM Setup script for Lab 11 - Windows

echo 🚀 Setting up Lab 11 environment...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

@REM REM Upgrade pip
@REM echo ⬆️  Upgrading pip...
@REM python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt

REM Copy .env.example to .env if .env doesn't exist
if not exist .env (
    echo 📝 Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your GOOGLE_API_KEY
    echo    Get your key at: https://aistudio.google.com/apikey
) else (
    echo ✅ .env file already exists
)

echo.
echo ✅ Setup complete!
echo.
echo Next steps:
echo 1. Edit .env and add your GOOGLE_API_KEY
echo 2. Activate the virtual environment:
echo    venv\Scripts\activate
echo 3. Run the lab:
echo    python src\main.py
echo.
pause
