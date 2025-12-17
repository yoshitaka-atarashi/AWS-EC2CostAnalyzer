@echo off
setlocal enabledelayedexpansion
echo ========================================
echo AWS EC2 Usage Analyzer
echo ========================================
echo.

REM Python detection
call :find_python
if "%PYTHON_EXE%"=="" (
    echo Python not found.
    echo.
    set /p install_choice="Install Python? (y/N): "
    if /i "!install_choice!"=="y" (
        call install_python.bat
        exit /b 0
    ) else (
        echo Please install Python and run again.
        pause
        exit /b 1
    )
)

echo Using Python: %PYTHON_EXE%
echo.

REM Check virtual environment
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Running setup...
    call setup.bat
    if %errorlevel% neq 0 (
        echo Setup failed.
        pause
        exit /b 1
    )
)

REM Execution method selection
echo Select execution method:
echo.
echo 1. Basic execution (default settings)
echo 2. Execution with options
echo 3. Interactive execution (menu-driven)
echo 4. Re-run setup
echo 5. Exit
echo.
set /p run_choice="Select option (1-5): "

if "%run_choice%"=="1" goto run_basic
if "%run_choice%"=="2" goto run_options
if "%run_choice%"=="3" goto run_interactive
if "%run_choice%"=="4" goto run_setup
if "%run_choice%"=="5" goto end
goto invalid_choice

:run_basic
echo.
echo Starting basic execution...
call run.bat
goto end

:run_options
echo.
echo Enter options (e.g. --region us-west-2 --days 7)
set /p options="Options: "
call run.bat %options%
goto end

:run_interactive
echo.
call run_with_options.bat
goto end

:run_setup
echo.
call setup.bat
goto end

:invalid_choice
echo Invalid selection.
pause
exit /b 1

:end
echo.
pause
exit /b 0

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