@echo off
echo Starting DocMemory Web Interface...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if docmemory is installed
python -c "import docmemory" >nul 2>&1
if errorlevel 1 (
    echo DocMemory is not installed
    echo Installing DocMemory...
    pip install docmemory
    if errorlevel 1 (
        echo Failed to install DocMemory
        pause
        exit /b 1
    )
)

REM Check if flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Flask is not installed
    echo Installing Flask...
    pip install flask
    if errorlevel 1 (
        echo Failed to install Flask
        pause
        exit /b 1
    )
)

REM Start the server
echo Starting DocMemory Web Interface on http://localhost:8000
python server.py

pause