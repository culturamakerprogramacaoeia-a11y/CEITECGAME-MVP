@echo off
title CEITECGAME - Servidor
color 0B

echo ==========================================
echo        INICIANDO SERVIDOR CEITECGAME
echo ==========================================
echo.
echo O sistema esta sendo iniciado...
echo.

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    color 0C
    echo [ERRO] Python nao encontrado!
    echo Instale o Python antes de iniciar.
    pause
    exit /b
)

echo Servidor rodando! 
echo.
echo ------------------------------------------
echo ACESSE NO SEU NAVEGADOR:
echo http://localhost:5000
echo ------------------------------------------
echo.
echo (Para desligar, feche esta janela)
echo.

python run.py

if %ERRORLEVEL% NEQ 0 (
    color 0C
    echo.
    echo [ERRO] O servidor parou inesperadamente.
    pause
)
