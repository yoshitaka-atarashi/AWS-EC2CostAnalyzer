@echo off
echo ========================================
echo AWS EC2 Usage Analyzer Setup
echo ========================================

REM Python detection
call :find_python
if "%PYTHON_EXE%"=="" (
    echo Error: Python not found
    echo.
    echo Please install Python using one of these methods:
    echo 1. Microsoft Store - Search for "Python" and install
    echo 2. Download from https://www.python.org/downloads/
    echo 3. Install Anaconda/Miniconda
    echo.
    pause
    exit /b 1
)

echo Using Python: %PYTHON_EXE%

REM Create virtual environment
echo Creating virtual environment...
"%PYTHON_EXE%" -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    echo Python version might be too old (Python 3.7+ required)
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Usage:
echo   run.bat                    - Basic execution
echo   run.bat --help             - Show help
echo   run.bat --region us-west-2 - Specify region
echo.
pause

:find_python
REM Python detection function
set PYTHON_EXE=

REM 1. Try standard python command
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python
    goto :eof
)

REM 2. Try python3 command
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=python3
    goto :eof
)

REM 3. Try py launcher
py --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_EXE=py
    goto :eof
)

REM 4. Search common installation paths
for %%p in (
    "C:\Python*\python.exe"
    "C:\Program Files\Python*\python.exe"
    "C:\Program Files (x86)\Python*\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python*\python.exe"
    "%APPDATA%\Local\Programs\Python\Python*\python.exe"
) do (
    for /f "delims=" %%i in ('dir /b /od "%%~p" 2^>nul') do (
        if exist "%%i" (
            "%%i" --version >nul 2>&1
            if !errorlevel! equ 0 (
                set PYTHON_EXE=%%i
                goto :eof
            )
        )
    )
)

REM 5. Search Anaconda/Miniconda
for %%p in (
    "%USERPROFILE%\anaconda3\python.exe"
    "%USERPROFILE%\miniconda3\python.exe"
    "C:\Anaconda3\python.exe"
    "C:\Miniconda3\python.exe"
    "%LOCALAPPDATA%\Continuum\anaconda3\python.exe"
    "%LOCALAPPDATA%\Continuum\miniconda3\python.exe"
) do (
    if exist "%%p" (
        "%%p" --version >nul 2>&1
        if !errorlevel! equ 0 (
            set PYTHON_EXE=%%p
            goto :eof
        )
    )
)

goto :eof