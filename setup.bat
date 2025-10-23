@echo off
REM Watch Party Nova - Easy Setup Script for Windows

echo ==================================
echo    Watch Party Nova Setup
echo ==================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python 3 is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo [OK] Python 3 found

REM Check if Ollama is installed
ollama --version >nul 2>&1
if errorlevel 1 (
    echo X Ollama is not installed.
    echo    Please install from: https://ollama.ai
    echo    Then run this script again.
    pause
    exit /b 1
)

echo [OK] Ollama found

REM Install Python dependencies
echo.
echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Warning: Some packages failed to install.
    echo If pyaudio failed, you may need to install it separately:
    echo    Download from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    echo.
)

REM Pull LLaVA model
echo.
echo Downloading LLaVA model (this may take a few minutes)...
ollama pull llava:7b

if errorlevel 1 (
    echo.
    echo X Failed to download LLaVA model.
    echo    Make sure Ollama is running.
    pause
    exit /b 1
)

echo.
echo ==================================
echo    Setup Complete!
echo ==================================
echo.
echo To run Watch Party Nova:
echo   python watchparty_voice_final.py
echo.
echo Enjoy watching with Nova! 
pause
