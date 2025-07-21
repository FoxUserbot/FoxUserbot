@echo off
chcp 65001 > nul
cls
title FoxUserBot

where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Python found on system 
    python main.py
    pause
    exit /b
)

echo Python not found...

winget --version >nul 2>&1
if errorlevel 1 (
    echo Install Winget...
    powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/getwinget' -OutFile 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'; Start-Process -FilePath 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle' -ArgumentList '/quiet' -Wait"
    echo Winget installed succesfully
)

echo Install Python 3.12...
winget install --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements

echo Please restart windows.bat
pause
