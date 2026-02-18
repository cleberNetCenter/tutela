# 🚀 Instruções de Deploy - Nginx (Produção)

## 🔍 Situação Atual
- **Servidor detectado**: **Nginx** (www.tuteladigital.com.br)
- **Problema**: URLs sem `.html` retornam 404
- **Exemplo**: `https://www.tuteladigital.com.br/fundamento-juridico` → 404

---

## ✅ Solução: Configurar Clean URLs no Nginx

### **Passo 1: Acessar o servidor**
```bash
ssh usuario@servidor-producao
```

---

### **Passo 2: Localizar arquivo de configuração Nginx**

**Opções comuns:**
```bash
# Opção 1: sites-available (Debian/Ubuntu)
ls -la /etc/nginx/sites-available/

# Opção 2: conf.d (CentOS/RedHat)
ls -la /etc/nginx/conf.d/

# Opção 3: nginx.conf direto
cat /etc/nginx/nginx.conf
```

**Provavelmente o arquivo se chama:**
- `/etc/nginx/sites-available/tuteladigital.com.br`
- `/etc/nginx/sites-available/default`
- `/etc/nginx/conf.d/tuteladigital.com.br.conf`

---

### **Passo 3: Backup da configuração atual**
```bash
sudo cp /etc/nginx/sites-available/tuteladigital.com.br /etc/nginx/sites-available/tuteladigital.com.br.backup-$(date +%Y%m%d)
```

---

### **Passo 4: Editar configuração**

**Adicione dentro do bloco `server { ... }`:**

```nginx
location / {
    try_files $uri $uri.html $uri/ =404;
}
```

**Exemplo completo:**
```nginx
server {
    listen 443 ssl http2;
    server_name tuteladigital.com.br www.tuteladigital.com.br;
    root /var/www/tuteladigital.com.br/public;  # Ajuste o caminho conforme necessário
    index index.html;

    # ⭐ ADICIONE ESTA SEÇÃO
    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    # Resto da configuração SSL, headers, etc...
}
```

---

### **Passo 5: Testar configuração**
```bash
sudo nginx -t
```

**Saída esperada:**
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

---

### **Passo 6: Aplicar mudanças**

**Se o teste passou:**
```bash
sudo systemctl reload nginx
```

**Alternativas:**
```bash
# Método 1: reload (preferível - sem downtime)
sudo service nginx reload

# Método 2: restart (com pequeno downtime)
sudo systemctl restart nginx
```

---

### **Passo 7: Verificar status**
```bash
sudo systemctl status nginx
```

---

## 🧪 Testar URLs Clean

Após aplicar a configuração, teste:

```bash
# Teste 1: Clean URL
curl -I https://www.tuteladigital.com.br/fundamento-juridico

# Teste 2: Com .html (deve funcionar também)
curl -I https://www.tuteladigital.com.br/fundamento-juridico.html

# Teste 3: Home
curl -I https://www.tuteladigital.com.br/
```

**Status esperado:** `200 OK`

---

## 🌐 URLs que devem funcionar após deploy

### ✅ Clean URLs (sem .html)
- `https://www.tuteladigital.com.br/`
- `https://www.tuteladigital.com.br/como-funciona`
- `https://www.tuteladigital.com.br/seguranca`
- `https://www.tuteladigital.com.br/preservacao-probatoria-digital`
- `https://www.tuteladigital.com.br/institucional`
- `https://www.tuteladigital.com.br/fundamento-juridico` ⭐
- `https://www.tuteladigital.com.br/termos-de-custodia`
- `https://www.tuteladigital.com.br/politica-de-privacidade`

### ✅ URLs com .html (também funcionam)
- `https://www.tuteladigital.com.br/fundamento-juridico.html`
- etc.

---

## 🔧 Configuração Completa (Opcional)

Se quiser aplicar a configuração completa com SSL, security headers, caching, etc.:

1. **Copie o arquivo `nginx-tuteladigital.conf`** do repositório
2. **Ajuste os caminhos:**
   - `root /var/www/...` (document root)
   - `ssl_certificate` e `ssl_certificate_key` (certificados SSL)
3. **Substitua a configuração atual**
4. **Teste e recarregue**

---

## 📄 Arquivo de configuração completo

Veja: `nginx-tuteladigital.conf` no repositório

**Inclui:**
- ✅ Clean URLs
- ✅ Force HTTPS
- ✅ SSL/TLS optimizado
- ✅ Security headers
- ✅ Browser caching
- ✅ GZIP compression
- ✅ Multilingual redirects

---

## ⚠️ Troubleshooting

### Problema: "Permission denied"
```bash
sudo chown -R www-data:www-data /var/www/tuteladigital.com.br/
sudo chmod -R 755 /var/www/tuteladigital.com.br/
```

### Problema: "403 Forbidden"
Verifique:
1. Permissões dos arquivos (755 para diretórios, 644 para arquivos)
2. SELinux (se aplicável): `sudo setenforce 0`
3. Dono dos arquivos: `www-data` ou `nginx`

### Problema: "502 Bad Gateway"
```bash
# Verificar logs
sudo tail -f /var/log/nginx/error.log

# Reiniciar Nginx
sudo systemctl restart nginx
```

### Problema: Ainda retorna 404
Verifique:
1. Caminho do `root` está correto?
2. Arquivos `.html` existem no servidor?
   ```bash
   ls -la /var/www/tuteladigital.com.br/public/*.html
   ```
3. Configuração foi aplicada?
   ```bash
   sudo nginx -T | grep "try_files"
   ```

---

## 📝 Checklist de Deploy

- [ ] Backup da configuração atual
- [ ] Arquivo de configuração editado
- [ ] `try_files $uri $uri.html $uri/ =404;` adicionado
- [ ] `sudo nginx -t` passou sem erros
- [ ] `sudo systemctl reload nginx` executado
- [ ] Teste de URL clean funcionou (`/fundamento-juridico`)
- [ ] Todas as 7 páginas testadas
- [ ] Multilingual testado (`/en`, `/es`)

---

## 🔗 Referências

- **PR #19**: https://github.com/cleberNetCenter/tutela/pull/19
- **Nginx docs**: http://nginx.org/en/docs/http/ngx_http_core_module.html#try_files
- **Repositório**: https://github.com/cleberNetCenter/tutela

---

## 📞 Suporte

Se precisar de ajuda:
1. Verifique os logs: `sudo tail -f /var/log/nginx/error.log`
2. Teste a configuração: `sudo nginx -t`
3. Verifique status: `sudo systemctl status nginx`
4. Abra uma issue no GitHub se necessário

---

**Última atualização:** 2025-02-18
