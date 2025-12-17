@echo off
setlocal enabledelayedexpansion

REM Check virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Error: Virtual environment not found
    echo Please run setup.bat to complete setup
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Use Python from virtual environment
set PYTHON_EXE=venv\Scripts\python.exe
if not exist "%PYTHON_EXE%" (
    echo Error: Python not found in virtual environment
    echo Please re-run setup.bat
    pause
    exit /b 1
)

REM Check AWS credentials
aws sts get-caller-identity >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ========================================
    echo AWS credentials not configured
    echo ========================================
    echo.
    echo Please configure AWS CLI with:
    echo   aws configure
    echo.
    echo Or set environment variables:
    echo   set AWS_ACCESS_KEY_ID=your_access_key
    echo   set AWS_SECRET_ACCESS_KEY=your_secret_key
    echo   set AWS_DEFAULT_REGION=ap-northeast-1
    echo.
    pause
    exit /b 1
)

REM Execute Python script
echo ========================================
echo Running AWS EC2 Usage Analyzer...
echo ========================================
echo.

"%PYTHON_EXE%" ec2_usage_analyzer.py %*

REM Check execution result
if %errorlevel% neq 0 (
    echo.
    echo An error occurred. Please check the messages above.
) else (
    echo.
    echo Analysis completed successfully.
)

echo.
pause