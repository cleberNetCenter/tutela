# Plano de Migração SPA → MPA
## Tutela Digital® - Arquitetura Multi-Page Application

---

## 📋 Status Atual

- ✅ PR #18 aberto: Implementação Multilíngua Completa (PT/EN/ES)
- ✅ Sistema i18n funcional (81 chaves × 3 idiomas)
- ✅ Hreflang implementado
- ⏸️  Migração MPA em preparação

---

## 🎯 Objetivo da Migração MPA

Migrar o site institucional de SPA (Single Page Application) para MPA (Multi Page Application), preservando integralmente:
- Layout
- CSS  
- Identidade visual
- Hierarquia institucional
- Estrutura de conteúdo

**Benefícios:**
- ✅ Indexação individual por página
- ✅ Autoridade documental
- ✅ Previsibilidade jurídica
- ✅ SEO probatório

---

## 📁 Páginas a Migrar (7 principais)

1. **index.html** (Home) - `page-home`
2. **institucional.html** - `page-institucional`
3. **preservacao-probatoria-digital.html** - `page-preservacao-probatoria`
4. **fundamento-juridico.html** - `page-fundamento-juridico`
5. **termos-de-custodia.html** - `page-termos-de-custodia`
6. **seguranca.html** - `page-seguranca`
7. **como-funciona.html** - `page-como-funciona`

---

## 🔧 Implementação Técnica

### PARTE 1: Criar Arquitetura MPA

**Ação:** Extrair cada seção `<div class="page" id="...">` do SPA e criar páginas HTML independentes.

**Template base:**
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <!-- Meta tags específicas -->
  <title>Página Específica - Tutela Digital®</title>
  <meta name="description" content="Descrição específica"/>
  <meta name="last-modified" content="2025-02-18"/>
  <link rel="canonical" href="URL"/>
  
  <!-- Open Graph -->
  <meta property="og:type" content="article"/>
  <meta property="og:title" content="..."/>
  
  <!-- Hreflang -->
  <link rel="alternate" hreflang="pt-br" href="..."/>
  
  <!-- CSS (mesmo do SPA) -->
  <link rel="stylesheet" href="assets/css/styles-clean.css?v=4">
  <link rel="stylesheet" href="assets/css/styles-header-final.css?v=4">
  <link rel="stylesheet" href="assets/css/styles-clean.exec-compact.css?v=4">
</head>
<body class="exec-compact">
  <div class="app">
    <!-- HEADER com links reais -->
    <header class="header" id="header">
      <nav class="nav">
        <a href="/">Início</a>
        <a href="/institucional.html">Institucional</a>
        <!-- ... -->
      </nav>
    </header>
    
    <!-- CONTEÚDO da página -->
    <main class="main">
      <!-- Conteúdo extraído do SPA -->
    </main>
    
    <!-- FOOTER com links reais -->
    <footer class="footer">
      <!-- ... -->
    </footer>
  </div>
  
  <script src="assets/js/i18n.js"></script>
  <script>
    function toggleMobileMenu() { /* ... */ }
  </script>
</body>
</html>
```

### PARTE 2: Head Individual por Página

Cada página deve ter:
- `<title>` específico
- `<meta name="description">` específica
- `<meta name="last-modified">` individual
- `<link rel="canonical">` próprio
- Open Graph tags completas
- Hreflang matrix completa

### PARTE 3: Schema JSON-LD por Página

| Página | Schema Type |
|--------|-------------|
| Home | Organization + WebSite + LegalService |
| Preservação | Article + LegalService |
| Fundamento | Article |
| Termos | LegalService + TermsOfService |
| Segurança | TechArticle |
| Como Funciona | HowTo |
| Institucional | Article + Organization |

### PARTE 4: Atualizar Navegação

**Remover:**
- `onclick="navigateTo('page')"`
- `data-page="..."`
- Dependência de `navigation.js`

**Substituir por:**
- `href="/institucional.html"`
- `href="/preservacao-probatoria-digital.html"`
- Links reais HTML padrão

### PARTE 5: Remover Dependência de JS para Renderização

**Manter JS apenas para:**
- Modal
- Dropdown idioma
- Interações (toggle mobile menu)

**Remover JS de:**
- Carregamento de conteúdo principal
- Navegação entre páginas
- Exibição de seções

### PARTE 6: Sitemap.xml

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.tuteladigital.com.br/</loc>
    <lastmod>2025-02-18</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://www.tuteladigital.com.br/institucional</loc>
    <lastmod>2025-02-18</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
  <!-- ... -->
</urlset>
```

### PARTE 7: robots.txt

```
User-agent: *
Allow: /

Sitemap: https://www.tuteladigital.com.br/sitemap.xml
```

---

## 🛠️ Ferramentas Criadas

### Script Gerador: `_mpa_generator.py`

Funções disponíveis:
- `extract_page_content(spa_html, page_id)` - Extrai conteúdo de página do SPA
- `create_head(title, desc, url, ...)` - Gera `<head>` customizado
- `create_header()` - Gera header MPA com links reais
- `create_footer()` - Gera footer MPA com links reais

**Uso:**
```python
# Ler SPA
with open('public/index.html', 'r') as f:
    spa = f.read()

# Extrair página
content = extract_page_content(spa, 'page-institucional')

# Montar MPA
mpa_html = f'''<!DOCTYPE html>
<html lang="pt-BR">
{create_head(...)}
<body class="exec-compact">
<div class="app">
{create_header()}
<main class="main">
{content}
</main>
{create_footer()}
</div>
</body>
</html>'''

# Salvar
with open('institucional.html', 'w') as f:
    f.write(mpa_html)
```

---

## ✅ Checklist de Validação

### Por Página:
- [ ] Acessível via URL direta
- [ ] Indexável isoladamente  
- [ ] Title único
- [ ] Description única
- [ ] Canonical correto
- [ ] Open Graph completo
- [ ] Hreflang implementado
- [ ] Schema JSON-LD específico
- [ ] CSS carregando corretamente
- [ ] i18n funcionando
- [ ] Links do header funcionam
- [ ] Links do footer funcionam

### Global:
- [ ] sitemap.xml gerado
- [ ] robots.txt atualizado
- [ ] Navegação funciona sem JS
- [ ] Conteúdo visível sem JS
- [ ] Build executado
- [ ] Cache limpo
- [ ] Testes em produção

---

## 📅 Cronograma Recomendado

1. **Fase 1:** Finalizar e mergear PR #18 (Multilíngua)
2. **Fase 2:** Criar branch `feature/mpa-migration`
3. **Fase 3:** Gerar 7 páginas MPA usando script
4. **Fase 4:** Validar cada página individualmente
5. **Fase 5:** Atualizar sitemap.xml e robots.txt
6. **Fase 6:** Criar PR dedicado para migração MPA
7. **Fase 7:** Review, testes e merge
8. **Fase 8:** Deploy e validação em produção

**Estimativa:** 2-3 dias de trabalho focado

---

## 🚨 Pontos de Atenção

### CSS
- ✅ Manter CSS idêntico
- ✅ Verificar caminhos relativos (`href="assets/..."`)
- ✅ Preservar classes `.page`, `.exec-compact`, etc.

### JavaScript
- ✅ Remover `navigation.js` (não necessário no MPA)
- ✅ Manter `i18n.js` (necessário para multilíngua)
- ✅ Manter funções `toggleMobileMenu()`

### SEO
- ✅ Cada página = URL única
- ✅ Canonical em todas as páginas
- ✅ Meta tags únicas
- ✅ Hreflang completo
- ✅ Schema específico

### Performance
- ✅ Cache-busting nos CSS (`?v=4`)
- ✅ Lazy loading de imagens mantido
- ✅ Google Analytics em todas as páginas

---

## 📊 Métricas de Sucesso

| Métrica | Antes (SPA) | Depois (MPA) |
|---------|-------------|--------------|
| Páginas indexáveis | 1 (index.html) | 7 páginas |
| Canonical único | Não | Sim |
| Title único por página | Não | Sim |
| Description única | Não | Sim |
| Schema por página | 3 globais | 7 específicos |
| Dependência de JS | Alta | Baixa |
| URLs diretas | Não | Sim |

---

## 🔗 Referências

- [PR #18 - Multilíngua](https://github.com/cleberNetCenter/tutela/pull/18)
- [Repositório](https://github.com/cleberNetCenter/tutela)
- [Site Produção](https://www.tuteladigital.com.br/)

---

**Próximo passo recomendado:**  
Mergear PR #18 e criar novo PR dedicado à migração MPA.

