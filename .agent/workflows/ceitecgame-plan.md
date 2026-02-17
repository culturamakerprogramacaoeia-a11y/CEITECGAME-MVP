---
description: Plano de Guerra - CEITECGAME MVP 1.0
---

# 🎮 PLANO DE GUERRA - CEITECGAME MVP 1.0

## 📋 VISÃO GERAL DO PROJETO

**Sistema:** CEITECGAME - Sistema de Gamificação Educacional  
**Objetivo:** Plataforma web para gamificação de atividades educacionais em Programação, Arduino, Cultura Maker e Pensamento Computacional  
**Stack:** Python 3.10+ | Flask | SQLAlchemy | SQLite | Bootstrap 5  
**Deploy:** PythonAnywhere

---

## 🎯 ESPECIALISTAS COORDENADOS

### 1. **Arquiteto de Software**
- Estrutura de pastas e organização modular
- Padrão Blueprint para escalabilidade
- Separação de responsabilidades (MVC)

### 2. **Engenheiro Backend**
- Modelos de dados (SQLAlchemy)
- Lógica de negócio (XP, níveis, recompensas)
- Rotas e controllers (Flask Blueprints)
- Sistema de autenticação (Flask-Login)

### 3. **Engenheiro Frontend**
- Interface responsiva (Bootstrap 5)
- Tema customizado (roxo escuro + verde tech)
- Dashboards para Professor e Aluno
- Sistema de ranking e loja

### 4. **Especialista em Segurança**
- Hash de senhas (werkzeug.security)
- Controle de acesso por tipo de usuário
- Proteção de rotas sensíveis
- Validação de dados

### 5. **DevOps Engineer**
- Configuração para PythonAnywhere
- Scripts de inicialização
- Gerenciamento de dependências
- Documentação de deploy

---

## 🏗️ ARQUITETURA DO SISTEMA

### Estrutura de Diretórios
```
ceitecgame/
├── app/
│   ├── __init__.py           # Factory pattern + Flask-Login
│   ├── models.py             # Modelos SQLAlchemy
│   ├── utils.py              # Funções auxiliares (cálculo de nível)
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Login/Logout
│   │   ├── professor.py      # Dashboard Professor
│   │   └── aluno.py          # Dashboard Aluno
│   ├── templates/
│   │   ├── base.html         # Template base
│   │   ├── login.html
│   │   ├── professor/
│   │   │   ├── dashboard.html
│   │   │   ├── criar_missao.html
│   │   │   ├── lancar_pontuacao.html
│   │   │   └── aprovar_resgates.html
│   │   └── aluno/
│   │       ├── dashboard.html
│   │       ├── historico.html
│   │       ├── ranking.html
│   │       └── loja.html
│   └── static/
│       ├── css/
│       │   └── style.css     # Tema customizado
│       └── img/
│           └── logo.png
├── config.py                 # Configurações
├── run.py                    # Entry point
├── requirements.txt          # Dependências
├── init_db.py               # Script de inicialização
└── README.md                # Documentação
```

---

## 📊 MODELO DE DADOS

### Entidades e Relacionamentos

**Usuario** (1:N com Pontuacao, Resgate)
- id, nome, email, senha_hash, tipo, turma_id
- Tipos: 'admin', 'professor', 'aluno'

**Turma** (1:N com Usuario)
- id, nome, ano, descricao

**Missao** (1:N com Pontuacao)
- id, titulo, categoria, xp, teccoins, descricao
- Categorias: 'Programação', 'Arduino', 'Maker', 'Pensamento Computacional'

**Pontuacao** (N:1 com Usuario, Missao)
- id, aluno_id, missao_id, xp_recebido, teccoins_recebido, data

**Recompensa** (1:N com Resgate)
- id, nome, custo_teccoins, descricao, nivel_minimo

**Resgate** (N:1 com Usuario, Recompensa)
- id, aluno_id, recompensa_id, data, status
- Status: 'pendente', 'aprovado', 'rejeitado'

---

## ⚙️ LÓGICA DE NEGÓCIO

### Sistema de Níveis
```python
def calcular_nivel(xp_total):
    if xp_total < 100:
        return "Explorador", 1
    elif xp_total < 300:
        return "Programador", 2
    elif xp_total < 600:
        return "Maker", 3
    elif xp_total < 1000:
        return "Engenheiro", 4
    else:
        return "Mentor", 5
```

### Regras de Resgate
1. Aluno solicita resgate
2. Validação: `teccoins >= custo AND nivel >= nivel_minimo`
3. Status inicial: 'pendente'
4. Professor aprova/rejeita
5. Se aprovado: deduz TecCoins do aluno

---

## 🎨 DESIGN SYSTEM

### Paleta de Cores
- **Primária:** `#1e1b4b` (Roxo escuro)
- **Secundária:** `#00ff88` (Verde tech)
- **Fundo:** `#0f0e1f`
- **Cards:** `#252340`
- **Texto:** `#ffffff` / `#a0a0b0`

### Componentes
- Navbar fixa com logo e menu
- Cards com bordas arredondadas e sombras
- Tabelas estilizadas para rankings
- Badges para níveis e status
- Botões com hover effects

---

## 🔐 SEGURANÇA

### Autenticação
- Flask-Login para gerenciamento de sessão
- Senhas com hash SHA256 (werkzeug.security)
- Decorators para proteção de rotas: `@login_required`

### Autorização
- Verificação de tipo de usuário em cada rota
- Professores: acesso a criação de missões e lançamento de pontos
- Alunos: acesso apenas a visualização e solicitação de resgates
- Admin: acesso total (futuro)

---

## 🚀 FASES DE IMPLEMENTAÇÃO

### **FASE 1: Fundação** ✅
1. Criar estrutura de diretórios
2. Configurar `config.py` e `run.py`
3. Implementar `app/__init__.py` com Flask-Login
4. Criar `requirements.txt`

### **FASE 2: Modelos e Banco** ✅
1. Implementar todos os modelos em `models.py`
2. Criar `utils.py` com função de cálculo de nível
3. Desenvolver `init_db.py` para popular banco inicial
4. Testar criação e relacionamentos

### **FASE 3: Autenticação** ✅
1. Implementar `routes/auth.py`
2. Criar templates de login
3. Configurar Flask-Login
4. Testar login/logout

### **FASE 4: Dashboard Professor** ✅
1. Implementar `routes/professor.py`
2. Criar templates do professor
3. Funcionalidades:
   - Criar missão
   - Listar alunos
   - Lançar pontuação
   - Aprovar resgates
   - Visualizar ranking

### **FASE 5: Dashboard Aluno** ✅
1. Implementar `routes/aluno.py`
2. Criar templates do aluno
3. Funcionalidades:
   - Ver XP e TecCoins
   - Ver nível atual
   - Histórico de pontuação
   - Ranking da turma
   - Loja de recompensas
   - Solicitar resgate

### **FASE 6: Frontend e Estilização** ✅
1. Criar `static/css/style.css` com tema completo
2. Implementar `templates/base.html`
3. Estilizar todos os templates
4. Garantir responsividade

### **FASE 7: Testes e Refinamento** ✅
1. Testar todos os fluxos
2. Validar cálculos de XP e níveis
3. Verificar segurança
4. Otimizar queries

### **FASE 8: Documentação e Deploy** ✅
1. Criar README.md completo
2. Documentar instalação local
3. Documentar deploy PythonAnywhere
4. Criar guia de uso

---

## 📦 DEPENDÊNCIAS (requirements.txt)

```
Flask==3.0.0
Flask-Login==0.6.3
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
```

---

## 🎯 CRITÉRIOS DE SUCESSO

- ✅ Sistema roda localmente sem erros
- ✅ Autenticação funcional com 3 tipos de usuário
- ✅ Professor consegue criar missões e lançar pontos
- ✅ Aluno vê progressão de XP e níveis corretamente
- ✅ Sistema de recompensas funcional
- ✅ Interface responsiva e visualmente atraente
- ✅ Código comentado e organizado
- ✅ Pronto para deploy no PythonAnywhere

---

## 📝 PRÓXIMOS PASSOS (Pós-MVP)

1. Sistema de badges e conquistas
2. Gráficos de evolução
3. Missões em equipe
4. Notificações em tempo real
5. API REST para integração mobile
6. Dashboard administrativo completo
7. Relatórios e analytics

---

**Status:** 🚀 PRONTO PARA EXECUÇÃO  
**Tempo Estimado:** 2-3 horas de implementação  
**Complexidade:** Média-Alta  
**Risco:** Baixo (stack consolidada)
