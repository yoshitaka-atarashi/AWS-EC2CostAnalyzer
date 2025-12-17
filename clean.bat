@echo off
echo ========================================
echo Virtual Environment Cleanup
echo ========================================

REM Confirm virtual environment deletion
set /p confirm="Delete virtual environment? (y/N): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)

REM Delete virtual environment folder
if exist "venv" (
    echo Deleting virtual environment...
    rmdir /s /q venv
    echo Virtual environment deleted.
) else (
    echo Virtual environment not found.
)

echo.
echo Cleanup completed.
echo Run setup.bat to use again.
echo.
pause