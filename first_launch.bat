@echo off
chcp 65001
cls
echo Install Python 3.12 and Node.js...
winget --version >nul 2>&1
if errorlevel 1 (
    echo Winget not found. Installing Winget...
    powershell -Command "Invoke-WebRequest -Uri 'https://aka.ms/getwinget' -OutFile 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle'; Start-Process -FilePath 'Microsoft.DesktopAppInstaller_8wekyb3d8bbwe.msixbundle' -ArgumentList '/quiet' -Wait"
    echo Winget installed.
)
winget install Python.Python.3.12
winget install OpenJS.NodeJS.LTS
python main.py