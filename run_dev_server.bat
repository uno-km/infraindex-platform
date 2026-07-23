@echo off
title InfraIndex Smart API Dev Server Launcher
echo ===================================================
echo  Starting InfraIndex Platform Dev Environment...  
echo ===================================================
cd /d "C:\Users\GAME\Desktop\uno-km\dev\AMEVA-Memory-Price-Check"
call .venv\Scripts\activate.bat

powershell -ExecutionPolicy Bypass -File .\run_dev_server.ps1
