# 🚀 GUIA DE DEPLOY MANUAL - SERVIDOR PROPRIETÁRIO

**Ambiente**: Servidor Proprietário  
**Método**: Git Pull Manual  
**Commit Pronto**: `2055da4`  
**Data**: 2026-02-20  
**Status**: ✅ **PRONTO PARA DEPLOY**

---

## 📊 STATUS ATUAL DO REPOSITÓRIO

### Branches Prontas
```
✅ main: 2055da4 (em origin/main)
✅ genspark_ai_developer: 2055da4 (em origin/genspark_ai_developer)
```

### Último Commit
```bash
Commit: 2055da4
Autor: GenSpark AI Developer
Mensagem: docs: Add production deployment guide
Data: 2026-02-20 20:15 UTC
```

---

## 🎯 PASSO A PASSO PARA DEPLOY

### 1️⃣ Conectar ao Servidor de Produção

```bash
# SSH para o servidor
ssh usuario@servidor-producao.com

# Ou conectar via painel de controle/terminal web
```

### 2️⃣ Navegar até o Diretório do Projeto

```bash
# Exemplo comum:
cd /var/www/tuteladigital.com.br

# Ou:
cd /home/usuario/public_html

# Ou outro path específico do seu servidor
```

### 3️⃣ Verificar Branch Atual

```bash
# Ver em qual branch está
git branch

# Deve mostrar algo como:
# * main
```

### 4️⃣ Fazer Backup (Recomendado)

```bash
# Criar backup antes do pull
cp -r . ../backup-$(date +%Y%m%d-%H%M%S)

# Ou apenas verificar status
git status
```

### 5️⃣ Fazer Git Pull

```bash
# Pull da branch main
git pull origin main

# Saída esperada:
# Updating dca6e57..2055da4
# Fast-forward
#  DEPLOY_GUIDE.md | 335 ++++++++++++++++++++++++++++
#  1 file changed, 335 insertions(+)
```

### 6️⃣ Verificar Atualização

```bash
# Confirmar commit atual
git log -1 --oneline

# Deve mostrar:
# 2055da4 docs: Add production deployment guide
```

### 7️⃣ Reiniciar Serviços (se necessário)

```bash
# Se usar Apache
sudo systemctl restart apache2

# Se usar Nginx
sudo systemctl restart nginx

# Se usar Node.js/PM2
pm2 restart all

# Ou apenas recarregar configuração
sudo systemctl reload nginx
```

---

## 📋 COMANDOS COMPLETOS (COPIAR E COLAR)

### Opção A: Deploy Simples

```bash
# Navegar para o diretório
cd /var/www/tuteladigital.com.br  # ajustar path

# Verificar status antes
git status
git log -1 --oneline

# Fazer pull
git pull origin main

# Verificar após
git log -1 --oneline

# Pronto! ✅
```

### Opção B: Deploy com Backup

```bash
# Navegar para o diretório
cd /var/www/tuteladigital.com.br  # ajustar path

# Backup
cp -r . ../backup-$(date +%Y%m%d-%H%M%S)

# Pull
git pull origin main

# Verificar
git log -1 --oneline

# Se algo der errado, restaurar:
# rm -rf ./*
# cp -r ../backup-TIMESTAMP/* .
```

### Opção C: Deploy com Verificação Completa

```bash
# Navegar
cd /var/www/tuteladigital.com.br

# Status antes
echo "=== ANTES DO DEPLOY ==="
git branch
git log -1 --oneline
git status

# Pull
echo "=== FAZENDO PULL ==="
git pull origin main

# Status depois
echo "=== APÓS DEPLOY ==="
git log -1 --oneline
git status

# Reiniciar serviço (ajustar conforme servidor)
sudo systemctl restart nginx  # ou apache2
```

---

## 🔍 VERIFICAÇÕES PÓS-DEPLOY

### 1. Verificar Arquivos

```bash
# Listar arquivos recentes
ls -lht | head -10

# Verificar documentação nova
ls -l DEPLOY_GUIDE.md REVERSION_REPORT.md
```

### 2. Verificar Logs

```bash
# Se usar Apache
tail -f /var/log/apache2/error.log

# Se usar Nginx
tail -f /var/log/nginx/error.log

# Verificar se há erros
```

### 3. Testar Site

```bash
# Fazer request local
curl -I http://localhost

# Ou se tiver curl instalado
curl http://localhost | head -20
```

---

## 🌐 VERIFICAR NO NAVEGADOR

Após fazer o pull no servidor:

1. **Abrir**: https://www.tuteladigital.com.br
2. **Hard Refresh**: `Ctrl + Shift + R`
3. **Testar Menu Mobile**: Clicar no hamburger
4. **Console**: Abrir DevTools (F12) → Console
5. **Confirmar**: Zero erros JavaScript

---

## ⚠️ TROUBLESHOOTING

### Problema: "Already up to date"

**Causa**: Servidor já tem o commit mais recente.

**Solução**: Verificar se o commit é realmente o esperado:
```bash
git log -1 --oneline
# Deve mostrar: 2055da4
```

### Problema: "Merge conflict"

**Causa**: Modificações locais no servidor.

**Solução A (Preservar mudanças locais)**:
```bash
git stash
git pull origin main
git stash pop
```

**Solução B (Descartar mudanças locais)**:
```bash
git reset --hard HEAD
git pull origin main
```

### Problema: "Permission denied"

**Causa**: Usuário não tem permissão.

**Solução**:
```bash
# Verificar proprietário
ls -la

# Ajustar permissões (cuidado!)
sudo chown -R usuario:grupo .

# Ou executar com sudo
sudo git pull origin main
```

### Problema: "Could not resolve host"

**Causa**: Servidor sem acesso ao GitHub.

**Solução**: Verificar conexão:
```bash
ping github.com
ssh -T git@github.com
```

---

## 📊 ESTRUTURA ESPERADA APÓS DEPLOY

```
/var/www/tuteladigital.com.br/
├── public/
│   ├── assets/
│   │   ├── css/
│   │   │   ├── styles-clean.css
│   │   │   ├── styles-header-final.css
│   │   │   └── dropdown-menu.css
│   │   └── js/
│   │       ├── navigation-controller.js
│   │       └── i18n.js
│   ├── legal/
│   │   ├── fundamento-juridico.html
│   │   ├── institucional.html
│   │   ├── politica-de-privacidade.html
│   │   ├── preservacao-probatoria-digital.html
│   │   └── termos-de-custodia.html
│   ├── en/
│   ├── es/
│   └── index.html
├── DEPLOY_GUIDE.md          ← NOVO
├── REVERSION_REPORT.md      ← NOVO
└── README.md
```

---

## 🎯 AMBIENTE APÓS DEPLOY

### O que estará em produção:

✅ **Estado Base**: Commit `2055da4`  
✅ **PR #99**: Fix dropdown mobile (mantido)  
✅ **Sistema MPA**: Funcionando  
✅ **i18n**: Ativo  
✅ **Footer**: Institucional completo  
✅ **Páginas Legais**: Todas presentes

### O que NÃO estará:

❌ **PRs #100-#104**: Removidos (causavam problemas)  
❌ **Mobile Menu Unification**: Revertido  
❌ **Page Structure Standardization**: Revertido  
❌ **iOS Safari Fixes**: Revertidos (podem ser reaplicados depois)

---

## 📝 CHECKLIST DE DEPLOY

### Antes do Pull
- [ ] Conectado ao servidor de produção
- [ ] No diretório correto do projeto
- [ ] Verificado branch atual (deve ser `main`)
- [ ] Backup criado (opcional mas recomendado)

### Durante o Pull
- [ ] Executar: `git pull origin main`
- [ ] Confirmar que atualizou para `2055da4`
- [ ] Verificar que não houve erros

### Após o Pull
- [ ] Verificar commit: `git log -1 --oneline`
- [ ] Reiniciar serviço (se necessário)
- [ ] Testar site no navegador
- [ ] Verificar console do navegador (F12)
- [ ] Confirmar menu mobile funciona

---

## 🎉 COMANDO ÚNICO (MAIS SIMPLES)

Se você tem acesso SSH e o diretório está correto:

```bash
ssh usuario@servidor && cd /var/www/tuteladigital.com.br && git pull origin main && exit
```

Depois apenas:
1. Abrir https://www.tuteladigital.com.br
2. Fazer hard refresh (Ctrl+Shift+R)
3. Testar

---

## 📞 INFORMAÇÕES DE SUPORTE

### Repositório
- **URL**: https://github.com/cleberNetCenter/tutela.git
- **Branch**: `main`
- **Commit**: `2055da4`

### Documentação
- **Relatório de Reversão**: `REVERSION_REPORT.md`
- **Guia de Deploy**: `DEPLOY_GUIDE.md` (este arquivo)

### Site
- **Produção**: https://www.tuteladigital.com.br

---

## ✅ RESUMO EXECUTIVO

**Para fazer o deploy, você precisa**:

1. Conectar ao servidor de produção (SSH ou painel)
2. Navegar até o diretório do projeto
3. Executar: `git pull origin main`
4. Reiniciar o serviço web (se necessário)
5. Testar no navegador

**Tempo estimado**: 2-5 minutos

**Resultado**: Site atualizado com ambiente revertido (pré-PR-100)

---

**Deploy manual pronto para execução** 🚀  
**Aguardando seu pull no servidor** ⏳  
**Commit pronto**: `2055da4`
