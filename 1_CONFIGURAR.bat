@echo off
title CEITECGAME - Configuracao Inicial
color 0A

echo ==========================================
echo      CONFIGURACAO INICIAL - CEITECGAME
echo ==========================================
echo.

echo [1/3] Verificando instalação do Python...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO CRITICO] Python nao encontrado!
    echo.
    echo O computador nao reconheceu o comando 'python'.
    echo.
    echo SOLUCAO:
    echo 1. Baixe o Python em python.org
    echo 2. Instale marcando a opcao "Add Python to PATH"
    echo 3. Reinicie este arquivo depois
    echo.
    pause
    exit /b
)
echo Python detectado com sucesso!
echo.

echo [2/3] Instalando bibliotecas necessarias...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao instalar dependencias do requirements.txt
    pause
    exit /b
)
echo Bibliotecas instaladas!
echo.

echo [3/3] Criando Banco de Dados (init_db.py)...
python init_db.py
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Falha ao rodar o script de banco de dados.
    pause
    exit /b
)

echo.
echo ==========================================
echo      TUDO PRONTO! SISTEMA CONFIGURADO
echo ==========================================
echo.
echo Siga os passos:
echo 1. Feche esta janela
echo 2. Execute o arquivo "2_INICIAR_SISTEMA.bat" para abrir o site
echo.
pause
