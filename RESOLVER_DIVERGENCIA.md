# 🔧 RESOLVER DIVERGÊNCIA DE BRANCHES

## ⚠️ SITUAÇÃO ATUAL

O servidor de produção tem commits locais que divergem do repositório remoto (GitHub).

---

## 🎯 SOLUÇÃO RÁPIDA (RECOMENDADA)

### Opção 1: Fazer merge (preserva histórico local)

```bash
# No servidor, execute:
git config pull.rebase false
git pull origin main
```

### Opção 2: Reset para o remoto (DESCARTA mudanças locais)

```bash
# ⚠️ CUIDADO: Isso vai descartar todas as mudanças locais!
git fetch origin
git reset --hard origin/main
```

---

## 📋 COMANDOS PASSO A PASSO

### 1️⃣ Verificar o que há de diferente

```bash
# Ver status local
git status

# Ver últimos commits locais
git log --oneline -5

# Ver o que está no remoto
git log origin/main --oneline -5

# Ver diferenças
git diff origin/main
```

### 2️⃣ Decidir qual opção usar

**Se NÃO há mudanças importantes no servidor** (RECOMENDADO):
```bash
# Resetar para o estado do GitHub
git fetch origin
git reset --hard origin/main
```

**Se há mudanças importantes no servidor que devem ser mantidas**:
```bash
# Fazer merge
git config pull.rebase false
git pull origin main
# Resolver conflitos se aparecerem
```

### 3️⃣ Verificar resultado

```bash
# Ver commit atual
git log -1 --oneline

# Deve mostrar:
# fc60eb7 docs: Add manual deployment guide for proprietary server
```

---

## 🚀 RESOLUÇÃO RÁPIDA (COPIAR E COLAR)

### Opção A: Reset Hard (Mais Seguro)

```bash
# Fazer backup primeiro
cp -r /var/www/tutela /var/www/tutela-backup-$(date +%Y%m%d-%H%M%S)

# Resetar para o remoto
cd /var/www/tutela
git fetch origin
git reset --hard origin/main

# Verificar
git log -1 --oneline

# Deve mostrar: fc60eb7
```

### Opção B: Merge (Se tem mudanças locais importantes)

```bash
cd /var/www/tutela

# Configurar merge
git config pull.rebase false

# Fazer pull
git pull origin main

# Se houver conflitos, resolver e depois:
# git add .
# git commit -m "Merge remote changes"
```

---

## ⚡ COMANDO ÚNICO (RECOMENDADO)

Se você quer apenas atualizar para o estado do GitHub (descartando mudanças locais):

```bash
cd /var/www/tutela && git fetch origin && git reset --hard origin/main && git log -1 --oneline
```

---

## 🔍 VERIFICAR O QUE ESTÁ NO SERVIDOR AGORA

Execute estes comandos para ver o que há de diferente:

```bash
# Ver status
git status

# Ver últimos 5 commits locais
git log --oneline -5

# Ver branch atual
git branch

# Ver diferenças com o remoto
git diff origin/main --stat
```

---

## 💡 RECOMENDAÇÃO

**Para deploy em produção, recomendo a Opção A (Reset Hard)**:

1. Fazer backup
2. Resetar para o remoto
3. Verificar commit

Isso garante que o servidor fique **exatamente igual** ao repositório GitHub.

---

## 📞 PRÓXIMOS PASSOS

Depois de resolver a divergência:

1. ✅ Verificar commit: `git log -1 --oneline`
2. ✅ Reiniciar servidor: `sudo systemctl restart nginx`
3. ✅ Testar site: https://www.tuteladigital.com.br
4. ✅ Verificar console (F12)

---

## ⚠️ IMPORTANTE

O reset hard vai **descartar** quaisquer mudanças locais no servidor. Se houver arquivos modificados que devem ser mantidos, use a **Opção B (Merge)** ao invés disso.

---

**Executar agora no servidor** 👇

```bash
cd /var/www/tutela
git fetch origin
git reset --hard origin/main
git log -1 --oneline
```
