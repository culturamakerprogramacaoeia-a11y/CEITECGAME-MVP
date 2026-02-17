# 🎮 CEITECGAME – MVP 1.0
**Sistema de Gamificação Educacional para Centro Tecnológico**

Programação • Arduino • Maker • Pensamento Computacional

---

## 📁 ESTRUTURA DO PROJETO

```
ceitecgame/
├── app/
│   ├── __init__.py          ← Application Factory + Flask-Login
│   ├── models.py            ← Modelos SQLAlchemy + calcular_nivel()
│   ├── routes/
│   │   ├── auth.py          ← Login / Logout
│   │   ├── professor.py     ← Dashboard professor, missões, pontuações
│   │   └── aluno.py         ← Dashboard aluno, loja, resgates
│   └── templates/
│       ├── base.html        ← Layout base (navbar, estilos)
│       ├── login.html
│       ├── professor/       ← Templates do professor
│       └── aluno/           ← Templates do aluno
├── config.py                ← Configurações (SECRET_KEY, banco)
├── run.py                   ← Entry point + comandos CLI
└── requirements.txt
```

---

## 🚀 COMO RODAR LOCALMENTE (Passo a Passo)

### 1. Pré-requisitos
- Python 3.10 ou superior instalado
- pip instalado

### 2. Criar e ativar ambiente virtual

```bash
# Crie a pasta do projeto (se não existir)
cd ceitecgame

# Crie o ambiente virtual
python -m venv venv

# Ative o ambiente virtual:
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Inicializar e popular o banco de dados

```bash
# Opção A – Cria as tabelas E popula com dados de teste:
flask --app run seed-db

# Opção B – Apenas cria as tabelas (sem dados):
flask --app run init-db
```

### 5. Rodar o servidor

```bash
python run.py
```

Acesse: **http://127.0.0.1:5000**

### 6. Credenciais de acesso (dados de teste)

| Perfil    | Email               | Senha    |
|-----------|---------------------|----------|
| Admin     | admin@ceitec.com    | admin123 |
| Professor | genezi@ceitec.com   | prof123  |
| Aluno 1   | alice@aluno.com     | aluno123 |
| Aluno 2   | bruno@aluno.com     | aluno123 |
| Aluno 3   | carla@aluno.com     | aluno123 |

---

## ✅ ROTEIRO DE TESTE

1. **Login como professor** → genezi@ceitec.com / prof123
2. **Lançar pontuação** → Menu "Lançar Pontos" → selecione Alice + Missão + confirme
3. **Login como aluno** → alice@aluno.com / aluno123
4. **Verificar XP/nível** no Dashboard do aluno
5. **Ir à Loja** → tentar resgatar uma recompensa
6. **Voltar como professor** → aprovar o resgate em "Resgates"

---

## ☁️ DEPLOY NO PYTHONANYWHERE (Passo a Passo)

### 1. Criar conta
Acesse https://www.pythonanywhere.com e crie uma conta gratuita.

### 2. Abrir console Bash
No painel: **Consoles → Bash**

### 3. Fazer upload do projeto

**Opção A – Upload via painel:**
- Menu: **Files → Upload a file**
- Faça upload do ZIP do projeto e extraia:
```bash
unzip ceitecgame.zip
```

**Opção B – Git clone:**
```bash
git clone https://github.com/seu-usuario/ceitecgame.git
```

### 4. Criar ambiente virtual e instalar dependências

```bash
cd ceitecgame
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Popular o banco de dados

```bash
flask --app run seed-db
```

### 6. Configurar Web App

No painel do PythonAnywhere:
- **Web → Add a new web app**
- Selecione: **Manual configuration** → Python 3.10

**Preencha os campos:**

| Campo | Valor |
|-------|-------|
| Source code | `/home/SEU_USUARIO/ceitecgame` |
| Working directory | `/home/SEU_USUARIO/ceitecgame` |
| Virtualenv | `/home/SEU_USUARIO/ceitecgame/venv` |
| WSGI file | (editar – ver passo 7) |

### 7. Editar o arquivo WSGI

Clique em **WSGI configuration file** e substitua TODO o conteúdo por:

```python
import sys
import os

# Adiciona o diretório do projeto ao PATH
path = '/home/SEU_USUARIO/ceitecgame'
if path not in sys.path:
    sys.path.insert(0, path)

os.chdir(path)

from run import app as application
```

> ⚠️ Substitua `SEU_USUARIO` pelo seu nome de usuário no PythonAnywhere.

### 8. Configurar variável de ambiente (segurança)

Na aba **Web → Environment variables**, adicione:
```
SECRET_KEY = uma-chave-muito-secreta-e-longa-2024
```

Ou edite diretamente o `config.py` com uma chave fixa.

### 9. Recarregar o app

Clique em **Reload** na aba Web. Acesse:
```
https://SEU_USUARIO.pythonanywhere.com
```

---

## 🎯 LÓGICA DE NÍVEL

| Nível          | XP necessário |
|----------------|--------------|
| 🔵 Explorador    | 0 – 100      |
| 🟢 Programador   | 101 – 300    |
| 🟡 Maker         | 301 – 600    |
| 🟣 Engenheiro    | 601 – 1000   |
| 🔴 Mentor        | 1000+        |

> O nível é **calculado dinamicamente** via `calcular_nivel(xp_total)` – não é armazenado no banco.

---

## 🔧 VARIÁVEIS DE CONFIGURAÇÃO (config.py)

```python
SECRET_KEY          # Chave para sessões Flask
SQLALCHEMY_DATABASE_URI  # Caminho do banco SQLite
```

---

## 📦 DEPENDÊNCIAS (requirements.txt)

```
Flask==3.0.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
SQLAlchemy==2.0.23
Werkzeug==3.0.1
```

---

*CEITECGAME MVP 1.0 – Desenvolvido para o Centro Tecnológico*
