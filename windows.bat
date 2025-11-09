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
    C:\Python312\python.exe
    C:\Python311\python.exe
    C:\Python310\python.exe
    C:\Python39\python.exe
    C:\Python38\python.exe
    C:\Python37\python.exe
    "C:\Program Files\Python312\python.exe"
    "C:\Program Files\Python311\python.exe"
    "C:\Program Files\Python310\python.exe"
    "C:\Program Files\Python39\python.exe"
    "C:\Program Files\Python38\python.exe"
    "C:\Program Files\Python37\python.exe"
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
    echo Python not found. Installing...
    
    winget --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Installing Winget...
        powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/getwinget' -OutFile 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'; Start-Process -FilePath 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle' -ArgumentList '/quiet' -Wait"
    )
    
    winget install --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements
    echo Please restart windows.bat
    pause
)
