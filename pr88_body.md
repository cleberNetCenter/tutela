## ⚖️ FIX: Páginas Legais - Sempre PT + Aviso em EN/ES

### 📜 Requisito Jurídico

As páginas do menu **"Base Jurídica"** (`/legal/*.html`) devem:
1. **Sempre** exibir conteúdo em **português** (requisito legal/regulatório)
2. **Traduzir** interface (header, footer, menu) conforme idioma do usuário
3. **Exibir aviso** quando usuário navega em inglês ou espanhol
4. **Oferecer botão** para trocar para PT diretamente do aviso

---

### 🐛 Problema Identificado

**Páginas afetadas:**
- `/legal/fundamento-juridico.html`
- `/legal/institucional.html`
- `/legal/politica-de-privacidade.html`
- `/legal/preservacao-probatoria-digital.html`
- `/legal/termos-de-custodia.html`

**Sintomas:**
- ❌ Aviso **não aparecia** quando usuário navegava em EN/ES
- ❌ Scripts `i18n.js` **não estavam carregados** nessas páginas
- ❌ Menu de idiomas não funcionava corretamente
- ✅ Conteúdo já estava em português (correto)

**Causa raiz:**
1. Função `isLegalPage()` apenas detectava páginas **SPA** (via ID `#page-institucional`, etc.)
2. Não detectava páginas **HTML separadas** com classe `.legal-page`
3. Páginas `/legal/*.html` não carregavam os scripts necessários

---

### ✅ Solução Implementada

#### 1. **i18n.js - Detecção aprimorada**

**Função `isLegalPage()` modificada:**

```javascript
// ANTES (apenas SPA)
isLegalPage() {
  return this.legalPages.some(pageId => {
    const page = document.getElementById(pageId);
    return page && page.classList.contains('active');
  });
}

// DEPOIS (SPA + páginas standalone)
isLegalPage() {
  // Método 1: Verifica body com classe 'legal-page' (HTML separado)
  if (document.body && document.body.classList.contains('legal-page')) {
    return true;
  }
  
  // Método 2: Verifica páginas SPA (compatibilidade)
  return this.legalPages.some(pageId => {
    const page = document.getElementById(pageId);
    return page && page.classList.contains('active');
  });
}
```

**Resultado:** Detecta páginas legais tanto no SPA quanto em arquivos HTML separados.

#### 2. **Scripts i18n adicionados nas páginas /legal/*.html**

Adicionado em **todas as 5 páginas** legais (antes do `</body>`):

```html
<!-- Scripts de internacionalização e navegação -->
<script src="/assets/js/navigation.js?v=202602190108"></script>
<script src="/assets/js/i18n.js?v=9"></script>
<script src="/assets/js/dropdown-menu.js?v=202602190108"></script>

<!-- Inicializar i18n para páginas legais -->
<script>
document.addEventListener('DOMContentLoaded', async () => {
  // Inicializa sistema i18n
  await I18N.init();
  
  // Força exibição do aviso se não estiver em PT
  if (I18N.currentLang !== 'pt') {
    console.log('[Legal Page] Idioma atual:', I18N.currentLang, '- Exibindo aviso');
    I18N.showLegalPageNoticeIfNeeded();
  }
});
</script>
```

**Resultado:** 
- Menu de idiomas funciona corretamente
- Aviso aparece automático em EN/ES
- Interface traduz, conteúdo permanece em PT

---

### 🎯 Comportamento Esperado

#### **Cenário 1: Usuário navega em PT** ✅
```
1. Usuário acessa /legal/institucional.html
2. Interface: PT
3. Conteúdo: PT
4. Aviso: NÃO exibido
✅ Experiência normal
```

#### **Cenário 2: Usuário navega em EN** ✅
```
1. Usuário acessa /legal/termos-de-custodia.html
2. Interface (header/footer/menu): traduz para EN
3. Conteúdo legal: permanece em PT
4. Aviso amarelo no topo:
   ⚠️ Legal Information: This document is available in Portuguese only.
   For complete understanding, please switch to Portuguese (PT).
   [Botão: Switch to Portuguese (PT)]
✅ Usuário informado + opção de trocar
```

#### **Cenário 3: Usuário navega em ES** ✅
```
1. Usuário acessa /legal/politica-de-privacidade.html
2. Interface (header/footer/menu): traduz para ES
3. Conteúdo legal: permanece em PT
4. Aviso amarelo no topo:
   ⚠️ Información Legal: Este documento está disponible solo en portugués.
   Para una comprensión completa, cambie a portugués (PT).
   [Botão: Cambiar a Portugués (PT)]
✅ Usuário informado + opção de trocar
```

---

### 📁 Arquivos Modificados

| Arquivo | Alterações |
|---------|------------|
| `public/assets/js/i18n.js` | • `isLegalPage()`: detecta `body.legal-page` OU SPA IDs<br>• `showLegalPageNoticeIfNeeded()`: usa `isLegalPage()` unificada |
| `public/legal/fundamento-juridico.html` | • Scripts i18n.js, navigation.js, dropdown-menu.js<br>• Inicializador automático |
| `public/legal/institucional.html` | • Scripts i18n.js, navigation.js, dropdown-menu.js<br>• Inicializador automático |
| `public/legal/politica-de-privacidade.html` | • Scripts i18n.js, navigation.js, dropdown-menu.js<br>• Inicializador automático |
| `public/legal/preservacao-probatoria-digital.html` | • Scripts i18n.js, navigation.js, dropdown-menu.js<br>• Inicializador automático |
| `public/legal/termos-de-custodia.html` | • Scripts i18n.js, navigation.js, dropdown-menu.js<br>• Inicializador automático |
| **Script auxiliar** | `add_i18n_to_legal_pages.py` (automatiza adição) |

**Total:** 6 arquivos modificados (1 JS + 5 HTML) + 1 script auxiliar

---

### 🧪 Validação

**1. Classe `.legal-page` verificada:**
```bash
grep "class=\".*legal-page" public/legal/*.html
✅ Todas as 5 páginas têm body class="legal-page"
```

**2. Scripts adicionados:**
```bash
grep "i18n.js" public/legal/*.html
✅ Todas as 5 páginas carregam i18n.js v=9
```

**3. Detecção de páginas legais:**
```javascript
// Testa detecção
console.log(I18N.isLegalPage()); 
✅ true (em páginas /legal/*.html)
✅ false (em outras páginas)
```

**4. Exibição de aviso:**
```javascript
// Usuário em EN, acessa /legal/institucional.html
I18N.currentLang // "en"
I18N.showLegalPageNoticeIfNeeded()
✅ Banner amarelo aparece no topo
```

---

### 📊 Impacto

| Métrica | Valor |
|---------|-------|
| Páginas modificadas | 5 (todas as /legal/*.html) |
| Scripts JS modificados | 1 (i18n.js) |
| Linhas adicionadas | ~150 (scripts + inicializador) |
| Risco de regressão | 🟢 **Muito baixo** |
| Benefício | 🔴 **Crítico** (requisito jurídico) |
| Impacto UX | ✅ **Positivo** (clareza para usuários internacionais) |

---

### 🚀 Deploy e Teste

**1. Aprovação e merge:**
```bash
gh pr review 88 --approve
gh pr merge 88 --squash --delete-branch
```

**2. Deploy automático:**
- Cloudflare Pages (~3-5 minutos)

**3. Validação em produção:**

**Teste 1: Página em PT (sem aviso)**
- [ ] Acessar: https://www.tuteladigital.com.br/legal/institucional.html
- [ ] Verificar idioma selecionado: PT
- [ ] Confirmar: **nenhum aviso** exibido
- [ ] Confirmar: conteúdo em português

**Teste 2: Página em EN (com aviso)**
- [ ] Acessar: https://www.tuteladigital.com.br/legal/termos-de-custodia.html
- [ ] Trocar idioma para: EN (English)
- [ ] Confirmar: **aviso amarelo** aparece no topo
- [ ] Texto do aviso: "⚠️ Legal Information: This document is available in Portuguese only..."
- [ ] Botão: "Switch to Portuguese (PT)"
- [ ] Clicar no botão → página volta para PT

**Teste 3: Página em ES (com aviso)**
- [ ] Acessar: https://www.tuteladigital.com.br/legal/politica-de-privacidade.html
- [ ] Trocar idioma para: ES (Español)
- [ ] Confirmar: **aviso amarelo** aparece no topo
- [ ] Texto do aviso: "⚠️ Información Legal: Este documento está disponible solo en portugués..."
- [ ] Botão: "Cambiar a Portugués (PT)"
- [ ] Clicar no botão → página volta para PT

**Teste 4: Menu de idiomas**
- [ ] Acessar qualquer página /legal/*.html
- [ ] Verificar menu dropdown de idiomas funciona
- [ ] Trocar PT → EN → ES → PT
- [ ] Confirmar interface (header/footer) traduz
- [ ] Confirmar conteúdo legal permanece em PT

---

### 🎨 Exemplo Visual do Aviso

```
╔═══════════════════════════════════════════════════════════════╗
║  ⚠️  Language Notice                                          ║
║                                                               ║
║  ⚠️ Legal Information: This document is available in          ║
║  Portuguese only. For complete understanding, please          ║
║  switch to Portuguese (PT).                                   ║
║                                                               ║
║  [ Switch to Portuguese (PT) / Cambiar a Portugués (PT) ]    ║
╚═══════════════════════════════════════════════════════════════╝
```

**Estilo:**
- Fundo amarelo (`#fff3cd`)
- Texto marrom escuro (`#856404`)
- Sticky no topo (`position: sticky; top: 0; z-index: 9999`)
- Botão azul para trocar para PT
- Sombra sutil para destaque

---

### ✨ Resultado Final

**Antes:**
- ❌ Aviso não aparecia em páginas /legal/*.html
- ❌ Menu de idiomas não funcionava corretamente
- ❌ Scripts i18n.js não carregados

**Depois:**
- ✅ Aviso aparece automático em EN/ES
- ✅ Menu de idiomas funciona perfeitamente
- ✅ Scripts i18n.js carregados e inicializados
- ✅ Interface traduz, conteúdo legal permanece em PT
- ✅ Botão para trocar para PT diretamente do aviso
- ✅ Requisito jurídico atendido
- ✅ UX clara para usuários internacionais

**Status:** ✅ Pronto para merge e deploy em produção

---

**Commit:** `fix(i18n): Garantir que páginas legais sempre exibam em PT + aviso em outros idiomas`  
**Branch:** `fix/legal-pages-pt-only`  
**Resolve:** Requisito jurídico de conteúdo legal apenas em português
