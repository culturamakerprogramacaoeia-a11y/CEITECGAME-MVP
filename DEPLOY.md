# 🌐 GUIA DE DEPLOY - PYTHONANYWHERE

## 📋 Pré-requisitos

- Conta no PythonAnywhere (gratuita ou paga)
- Código do projeto (via Git ou upload manual)

---

## 🚀 Passo a Passo Completo

### 1️⃣ Criar Conta

1. Acesse: https://www.pythonanywhere.com
2. Clique em "Start running Python online in less than a minute!"
3. Escolha "Create a Beginner account" (gratuito)
4. Preencha os dados e confirme o email

---

### 2️⃣ Upload do Código

#### Opção A: Via Git (Recomendado)

1. Vá para a aba **Consoles**
2. Clique em **Bash**
3. Execute:

```bash
git clone https://github.com/SEU_USUARIO/ceitecgame.git
cd ceitecgame
```

#### Opção B: Upload Manual

1. Vá para a aba **Files**
2. Crie a pasta `ceitecgame`
3. Faça upload de todos os arquivos mantendo a estrutura

---

### 3️⃣ Configurar Ambiente Virtual

No console Bash:

```bash
cd ~/ceitecgame
python3.10 -m venv venv
source venv/bin/activate
```

---

### 4️⃣ Instalar Dependências

```bash
pip install -r requirements.txt
```

**Aguarde a instalação completa!** Pode levar alguns minutos.

---

### 5️⃣ Inicializar Banco de Dados

```bash
python init_db.py
```

Você verá a mensagem de sucesso com as credenciais.

---

### 6️⃣ Configurar Web App

1. Vá para a aba **Web**
2. Clique em **Add a new web app**
3. Clique em **Next** (aceite o domínio gratuito)
4. Escolha **Manual configuration**
5. Selecione **Python 3.10**
6. Clique em **Next**

---

### 7️⃣ Configurar WSGI

1. Na seção **Code**, clique no link do arquivo WSGI
2. **Delete todo o conteúdo** do arquivo
3. Cole o seguinte código (substitua `SEU_USUARIO`):

```python
import sys
import os

# Adicionar o diretório do projeto ao path
project_home = '/home/SEU_USUARIO/ceitecgame'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Importar a aplicação
from run import app as application
```

4. Clique em **Save**

---

### 8️⃣ Configurar Virtualenv

1. Na seção **Virtualenv**
2. No campo "Enter path to a virtualenv", digite:

```
/home/SEU_USUARIO/ceitecgame/venv
```

3. Clique no ✓ (check)

---

### 9️⃣ Configurar Arquivos Estáticos

Na seção **Static files**, clique em **Enter URL** e adicione:

| URL | Directory |
|-----|-----------|
| `/static/` | `/home/SEU_USUARIO/ceitecgame/app/static/` |

---

### 🔟 Reload e Teste

1. Clique no botão verde **Reload SEU_USUARIO.pythonanywhere.com**
2. Aguarde alguns segundos
3. Clique no link do seu site

**Seu site estará no ar!** 🎉

```
https://SEU_USUARIO.pythonanywhere.com
```

---

## 🔍 Verificação de Erros

### Ver Logs de Erro

1. Aba **Web**
2. Seção **Log files**
3. Clique em **Error log**

### Erros Comuns

#### Erro 500 - Internal Server Error

**Causa:** Caminho do WSGI incorreto

**Solução:**
- Verifique se substituiu `SEU_USUARIO` pelo seu username
- Confirme que o caminho existe: `/home/SEU_USUARIO/ceitecgame`

#### Erro: No module named 'flask'

**Causa:** Virtualenv não configurado corretamente

**Solução:**
```bash
cd ~/ceitecgame
source venv/bin/activate
pip install -r requirements.txt
```

#### CSS não carrega

**Causa:** Arquivos estáticos não configurados

**Solução:**
- Verifique a configuração em **Static files**
- Caminho deve ser absoluto: `/home/SEU_USUARIO/ceitecgame/app/static/`

---

## 🔄 Atualizar o Site

Quando fizer alterações no código:

```bash
cd ~/ceitecgame
git pull  # Se usar Git
source venv/bin/activate
pip install -r requirements.txt  # Se houver novas dependências
```

Depois, na aba **Web**, clique em **Reload**.

---

## 📊 Monitoramento

### Ver Acessos

Aba **Web** → **Access log**

### Ver Erros

Aba **Web** → **Error log**

### Ver Console

Aba **Web** → **Server log**

---

## 🔒 Segurança em Produção

### 1. Alterar SECRET_KEY

Edite `config.py`:

```python
SECRET_KEY = 'sua-chave-super-secreta-aqui-123456789'
```

### 2. Alterar Credenciais Padrão

Após o primeiro acesso:
1. Faça login como admin
2. Altere as senhas de todos os usuários
3. Delete usuários de exemplo se não forem necessários

### 3. Desabilitar Debug

Edite `run.py`:

```python
if __name__ == '__main__':
    app.run(debug=False)  # Altere para False
```

---

## 💾 Backup do Banco de Dados

### Fazer Backup

```bash
cd ~/ceitecgame
cp ceitecgame.db ceitecgame_backup_$(date +%Y%m%d).db
```

### Restaurar Backup

```bash
cd ~/ceitecgame
cp ceitecgame_backup_20240101.db ceitecgame.db
```

---

## 📈 Upgrade para Conta Paga

Benefícios:
- Domínio personalizado
- Mais CPU e memória
- Mais espaço em disco
- Suporte prioritário

Planos: https://www.pythonanywhere.com/pricing/

---

## 🆘 Suporte

### Documentação Oficial
https://help.pythonanywhere.com/

### Fórum
https://www.pythonanywhere.com/forums/

### Suporte Direto
support@pythonanywhere.com (apenas contas pagas)

---

## ✅ Checklist de Deploy

- [ ] Conta criada no PythonAnywhere
- [ ] Código enviado (Git ou upload)
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Banco de dados inicializado
- [ ] WSGI configurado
- [ ] Virtualenv configurado
- [ ] Arquivos estáticos configurados
- [ ] Site recarregado
- [ ] Site acessível e funcionando
- [ ] Credenciais padrão alteradas
- [ ] SECRET_KEY alterada
- [ ] Debug desabilitado

---

**🎉 Parabéns! Seu CEITECGAME está no ar!**

Compartilhe o link: `https://SEU_USUARIO.pythonanywhere.com`
