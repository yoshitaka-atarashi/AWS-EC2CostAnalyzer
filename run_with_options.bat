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

echo ========================================
echo AWS EC2 Usage Analyzer - Options Setup
echo ========================================
echo.

REM Region selection
echo 1. ap-northeast-1 (Tokyo)
echo 2. us-east-1 (N. Virginia)
echo 3. us-west-2 (Oregon)
echo 4. eu-west-1 (Ireland)
echo 5. Custom input
echo.
set /p region_choice="Select region (1-5): "

set region=ap-northeast-1
if "%region_choice%"=="1" set region=ap-northeast-1
if "%region_choice%"=="2" set region=us-east-1
if "%region_choice%"=="3" set region=us-west-2
if "%region_choice%"=="4" set region=eu-west-1
if "%region_choice%"=="5" (
    set /p region="Enter region name: "
)

echo.
REM Analysis period setting
set /p days="Analysis period (days, default: 30): "
if "%days%"=="" set days=30

echo.
REM CPU threshold setting
set /p cpu_threshold="CPU utilization threshold (%%, default: 5.0): "
if "%cpu_threshold%"=="" set cpu_threshold=5.0

echo.
REM Expensive threshold setting
set /p expensive_threshold="Expensive instance threshold ($/month, default: 100.0): "
if "%expensive_threshold%"=="" set expensive_threshold=100.0

echo.
REM Output file setting
set /p output_file="Output file name (optional, e.g. cost_analysis.json): "

echo.
echo ========================================
echo Configuration:
echo   Region: %region%
echo   Analysis period: %days% days
echo   CPU threshold: %cpu_threshold%%%
echo   Expensive threshold: $%expensive_threshold%/month
if not "%output_file%"=="" echo   Output file: %output_file%
echo ========================================
echo.

REM Execution confirmation
set /p confirm="Execute with these settings? (Y/n): "
if /i "%confirm%"=="n" (
    echo Cancelled.
    pause
    exit /b 0
)

REM Build command line arguments
set args=--region %region% --days %days% --cpu-threshold %cpu_threshold% --expensive-threshold %expensive_threshold%
if not "%output_file%"=="" set args=%args% --output %output_file%

echo.
echo Executing...
"%PYTHON_EXE%" ec2_usage_analyzer.py %args%

echo.
pause