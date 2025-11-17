@echo off
chcp 65001
cls
title FoxUserBot

echo Starting FoxUserBot...

py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Python via py launcher
    py main.py
    pause
    exit /b
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Using Python via python command
    python main.py
    pause
    exit /b
)

echo Searching for Python in common locations...

set FOUND=0
for %%p in (
    C:\Python313\python.exe
    C:\Python312\python.exe
    C:\Python311\python.exe
    C:\Python310\python.exe
    C:\Python39\python.exe
    C:\Python38\python.exe
    C:\Python37\python.exe
    "C:\Program Files\Python313\python.exe"
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Program Files\Python39\python.exe"
    "C:\Program Files\Python38\python.exe"
    "C:\Program Files\Python37\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python39\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python38\python.exe"
    "%LOCALAPPDATA%\Programs\Python\Python37\python.exe"
) do (
    if exist %%p (
        echo Found Python: %%p
        %%p main.py
        set FOUND=1
        pause
        exit /b
    )
)

if %FOUND% equ 0 (
    echo Python not found. Attempting winget installation...
    
    winget install --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    if %errorlevel% equ 0 (
        echo Python installed successfully!
    ) else (
        echo.
        echo Winget installation failed. Installing winget...
        powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/getwinget' -OutFile 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'; Add-AppxPackage -Path 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'"
        echo.
        echo Installing Python via winget...
        winget install --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    )
    echo.
    echo Please restart windows.bat
    pause
)
