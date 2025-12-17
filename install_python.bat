@echo off
echo ========================================
echo Python Auto-Installer
echo ========================================
echo.

REM Check administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires administrator privileges.
    echo Please right-click and select "Run as administrator".
    pause
    exit /b 1
)

echo Select Python installation method:
echo.
echo 1. Microsoft Store Python (Recommended)
echo 2. Official Python.org download
echo 3. Automatic installation using winget
echo 4. Cancel
echo.
set /p choice="Select option (1-4): "

if "%choice%"=="1" goto install_store
if "%choice%"=="2" goto install_official
if "%choice%"=="3" goto install_winget
if "%choice%"=="4" goto cancel
goto invalid_choice

:install_store
echo.
echo Installing Microsoft Store Python...
echo Microsoft Store will open in your browser.
start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
echo.
echo After installation completes in Microsoft Store, run setup.bat
goto end

:install_official
echo.
echo Opening official Python.org download page...
start https://www.python.org/downloads/windows/
echo.
echo After download and installation, run setup.bat
echo Make sure to check "Add Python to PATH" during installation.
goto end

:install_winget
echo.
echo Installing Python using winget...
winget --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: winget not found
    echo Windows 10 version 1809+ or Windows 11 required
    echo Please use option 1 or 2 instead
    pause
    exit /b 1
)

echo Installing Python...
winget install Python.Python.3.11
if %errorlevel% equ 0 (
    echo Python installation completed.
    echo Open a new command prompt and run setup.bat
) else (
    echo Installation failed.
    echo Please use option 1 or 2 instead.
)
goto end

:invalid_choice
echo Invalid selection.
pause
exit /b 1

:cancel
echo Cancelled.
goto end

:end
echo.
pause