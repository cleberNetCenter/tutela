# Configuração de Clean URLs e Redirects

## ⚠️ Problema
URLs sem `.html` retornam 404:
- ❌ `https://www.tuteladigital.com.br/fundamento-juridico` → 404
- ✅ `https://www.tuteladigital.com.br/fundamento-juridico.html` → 200

---

## 🛠️ Soluções por plataforma

### **1️⃣ Vercel**
📄 Arquivo: `public/vercel.json`

**Como usar:**
- O arquivo `vercel.json` já está no repositório
- Vercel detecta automaticamente no deploy
- Nenhuma configuração adicional necessária

**Funcionalidades:**
✅ Clean URLs (sem .html)
✅ Redirects automáticos
✅ Security headers

---

### **2️⃣ Netlify**
📄 Arquivo: `public/netlify.toml` **ou** `public/_redirects`

**Como usar:**
- **Opção A**: Use `netlify.toml` (mais recursos)
- **Opção B**: Use `_redirects` (mais simples)
- Netlify detecta automaticamente no deploy

**Funcionalidades:**
✅ Clean URLs (status 200 rewrites)
✅ Redirects 301 de rotas antigas SPA
✅ Security headers (somente em netlify.toml)

---

### **3️⃣ Cloudflare Pages**
📄 Arquivo: `public/_redirects`

**Como usar:**
- O arquivo `_redirects` já está no repositório
- Cloudflare Pages detecta automaticamente
- Funciona igual ao Netlify

**Funcionalidades:**
✅ Clean URLs
✅ Redirects 301 de rotas SPA antigas
✅ Multilingual redirects (/en, /es)

---

### **4️⃣ Apache (cPanel, VPS tradicional)**
📄 Arquivo: `public/.htaccess`

**Como usar:**
1. Upload do arquivo `.htaccess` para a pasta `public_html`
2. Certifique-se que `mod_rewrite` está habilitado
3. Reinicie o Apache (se necessário)

**Funcionalidades:**
✅ Clean URLs automáticos
✅ Force HTTPS
✅ Redirects 301 de rotas SPA antigas
✅ Security headers
✅ Browser caching otimizado

---

### **5️⃣ Nginx**
📄 Criar arquivo de configuração manualmente

**Exemplo de configuração:**
```nginx
server {
    listen 80;
    server_name tuteladigital.com.br www.tuteladigital.com.br;
    root /var/www/html/public;
    index index.html;

    # Clean URLs
    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    # Redirects 301 de rotas SPA antigas
    location ~ ^/#(.*)$ {
        return 301 /$1.html;
    }

    # Security headers
    add_header X-Frame-Options "DENY";
    add_header X-Content-Type-Options "nosniff";
    add_header X-XSS-Protection "1; mode=block";

    # Browser caching
    location ~* \.(css|js|jpg|jpeg|png|gif|svg|ico)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

---

## 📋 Arquivos criados

| Arquivo | Plataforma | Status |
|---------|-----------|--------|
| `public/vercel.json` | Vercel | ✅ Criado |
| `public/netlify.toml` | Netlify | ✅ Criado |
| `public/_redirects` | Netlify/Cloudflare | ✅ Criado |
| `public/.htaccess` | Apache | ✅ Criado |

---

## 🧪 Como testar localmente

### Teste com Python HTTP Server (simples)
```bash
cd public
python3 -m http.server 8000
```
⚠️ **Limitação**: Não suporta rewrites/redirects (404 para clean URLs)

### Teste com servidor que suporta rewrites

#### **Opção 1: http-server (Node.js)**
```bash
npm install -g http-server
cd public
http-server -p 8000 --ext html
```

#### **Opção 2: serve (Node.js)**
```bash
npm install -g serve
cd public
serve -p 8000 --single
```

---

## ✅ URLs que devem funcionar após deploy

### Clean URLs (sem .html)
- `https://www.tuteladigital.com.br/`
- `https://www.tuteladigital.com.br/como-funciona`
- `https://www.tuteladigital.com.br/seguranca`
- `https://www.tuteladigital.com.br/preservacao-probatoria-digital`
- `https://www.tuteladigital.com.br/institucional`
- `https://www.tuteladigital.com.br/fundamento-juridico` ✅
- `https://www.tuteladigital.com.br/termos-de-custodia`
- `https://www.tuteladigital.com.br/politica-de-privacidade`

### URLs com .html (também funcionam)
- `https://www.tuteladigital.com.br/fundamento-juridico.html`

### Multilingual
- `https://www.tuteladigital.com.br/en`
- `https://www.tuteladigital.com.br/es`

---

## 🚀 Próximos passos

1. **Commit** dos arquivos de configuração
2. **Push** para o branch `feature/mpa-migration`
3. **Merge** do PR #19
4. **Deploy** para produção
5. **Testar** todas as URLs clean

---

## 📝 Observações importantes

- **Vercel/Netlify/Cloudflare**: Detectam automaticamente os arquivos de configuração
- **Apache**: Certifique-se que `mod_rewrite` está habilitado
- **Nginx**: Requer configuração manual no arquivo de virtual host
- **Produção atual**: Verifique qual servidor web está sendo usado em produção

---

## 🔗 Referências

- Vercel Rewrites: https://vercel.com/docs/project-configuration#rewrites
- Netlify Redirects: https://docs.netlify.com/routing/redirects/
- Cloudflare Pages: https://developers.cloudflare.com/pages/platform/redirects/
- Apache mod_rewrite: https://httpd.apache.org/docs/current/mod/mod_rewrite.html
