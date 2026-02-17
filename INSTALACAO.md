# 🚀 GUIA RÁPIDO DE INSTALAÇÃO - CEITECGAME

## ⚡ Instalação Expressa (Windows)

### 1. Verificar Python

Abra o PowerShell e execute:
```powershell
python --version
```

Se não estiver instalado, baixe em: https://www.python.org/downloads/

> ⚠️ **IMPORTANTE**: Durante a instalação, marque "Add Python to PATH"

### 2. Criar Ambiente Virtual

```powershell
cd C:\Users\genez\CEITECGAME
python -m venv venv
```

### 3. Ativar Ambiente Virtual

```powershell
.\venv\Scripts\Activate.ps1
```

**Se der erro de execução de scripts:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### 4. Instalar Dependências

```powershell
pip install -r requirements.txt
```

### 5. Inicializar Banco de Dados

```powershell
python init_db.py
```

### 6. Executar Aplicação

```powershell
python run.py
```

### 7. Acessar no Navegador

```
http://localhost:5000
```

---

## 🔧 Solução de Problemas Comuns

### Python não reconhecido

**Solução 1:** Use `py` ao invés de `python`
```powershell
py -m venv venv
py init_db.py
py run.py
```

**Solução 2:** Adicione Python ao PATH manualmente
1. Encontre onde o Python está instalado (geralmente `C:\Users\SEU_USUARIO\AppData\Local\Programs\Python\Python3XX`)
2. Adicione ao PATH do sistema

### Erro ao ativar ambiente virtual

```powershell
# Execute como Administrador
Set-ExecutionPolicy RemoteSigned

# Depois ative normalmente
.\venv\Scripts\Activate.ps1
```

### Porta 5000 já em uso

Edite `run.py` e altere a porta:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

---

## 📦 Instalação Sem Ambiente Virtual (Não Recomendado)

Se tiver problemas com o ambiente virtual:

```powershell
cd C:\Users\genez\CEITECGAME
pip install Flask==3.0.0 Flask-Login==0.6.3 Flask-SQLAlchemy==3.1.1 Werkzeug==3.0.1
python init_db.py
python run.py
```

---

## 🎯 Checklist de Instalação

- [ ] Python 3.10+ instalado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Banco de dados inicializado
- [ ] Aplicação rodando em localhost:5000
- [ ] Login funcionando com credenciais padrão

---

## 📞 Precisa de Ajuda?

Se nada funcionar, tente:

1. **Reinstalar Python** (versão 3.10 ou superior)
2. **Reiniciar o computador**
3. **Executar PowerShell como Administrador**
4. **Desabilitar antivírus temporariamente** (pode bloquear scripts)

---

## 🎮 Credenciais para Teste

Após inicializar o banco, use:

**Professor:**
- Email: professor@ceitec.com
- Senha: professor123

**Aluno:**
- Email: ana@aluno.com
- Senha: aluno123

---

**Desenvolvido para o Centro Tecnológico** 🚀
