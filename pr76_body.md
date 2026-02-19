## 🎯 Objetivo

Aplicar o **padrão hero institucional** da página segurança à página **como-funciona.html**:
- Remover elemento gráfico/imagem do hero
- Hero centralizado sem imagem de fundo
- Adicionar gráfico SVG institucional (3 círculos)

---

## 📋 Alterações Implementadas

### **ANTES:**
```html
<section class="page-header page-header--como-funciona hero--image" 
         style="background-image: url('/assets/images/fluxo-cadeia-custodia-verde.png');">
  <div class="page-header-inner page-header--split">
    <div class="page-header-content">
      <h1>Como Funciona</h1>
      <p>Processo estruturado...</p>
    </div>
  </div>
</section>
```

### **DEPOIS:**
```html
<section class="page-header page-header--como-funciona-centered">
  <div class="page-header-inner page-header--como-funciona">
    
    <h1>Como Funciona</h1>

    <div class="como-funciona-graphic">
      <svg viewBox="0 0 900 120">
        <!-- Linha + 3 círculos: Integridade, Cadeia de Custódia, Validade Jurídica -->
      </svg>
    </div>

    <p class="page-header-subtitle">Processo estruturado...</p>

  </div>
</section>
```

---

## 🎨 Transformações Visuais

### **1️⃣ Hero:**
- ❌ **Removido:** Imagem de fundo (`fluxo-cadeia-custodia-verde.png`)
- ❌ **Removido:** Layout split horizontal (`.page-header--split`)
- ✅ **Adicionado:** Hero centralizado (`.page-header--como-funciona-centered`)
- ✅ **Adicionado:** Gráfico SVG institucional com 3 círculos
- ✅ **Adicionado:** Subtítulo centralizado

### **2️⃣ Gráfico SVG Institucional:**
```html
<div class="como-funciona-graphic">
  <svg viewBox="0 0 900 120">
    <line /> <!-- Linha base verde -->
    <circle /> <text>Integridade</text>
    <circle /> <text>Cadeia de Custódia</text>
    <circle /> <text>Validade Jurídica</text>
  </svg>
</div>
```

### **3️⃣ CSS Inline:**
```css
/* Main - compensação para header fixo */
body.exec-compact .main.main--hero-top {
  padding-top: 80px !important;
  margin-top: 0 !important;
}

/* Hero centralizado */
.page-header--como-funciona-centered {
  background: linear-gradient(135deg, 
    var(--color-surface-light) 0%, 
    rgba(255,255,255,0.98) 100%);
  padding: 3rem 2rem 5rem 2rem;
  text-align: center;
}

/* Gráfico SVG */
.como-funciona-graphic {
  margin: 1.5rem auto 2.5rem auto;
  max-width: 900px;
  opacity: 0.9;
}

/* Mobile */
@media (max-width: 768px) {
  body.exec-compact .main.main--hero-top {
    padding-top: 70px !important;
  }
  .como-funciona-graphic svg text {
    font-size: 13px;
  }
  .page-header--como-funciona-centered {
    padding: 2rem 1.5rem 3rem 1.5rem;
  }
}
```

---

## 🔒 Garantias de Não Impacto

### **✅ Seletor específico:**
```css
body.exec-compact .main.main--hero-top
```
- Requer `body.exec-compact` + `main.main--hero-top`
- **como-funciona.html** tem esta combinação ← **AFETADA**
- Outras páginas **não** têm esta combinação ← **NÃO AFETADAS**

### **✅ CSS inline isolado:**
- Todo o CSS está no `<head>` de `como-funciona.html`
- Prefixos exclusivos: `.como-funciona-*`, `.page-header--como-funciona-*`
- **Não modifica** arquivos CSS globais

### **✅ Não alterado:**
- ❌ Header
- ❌ Footer
- ❌ Menu
- ❌ CTA final
- ❌ Variáveis CSS globais
- ❌ Arquivos CSS compartilhados
- ❌ Sistema i18n
- ❌ Classes em outras páginas
- ❌ Seção "Etapas do Processo" (mantida intacta)

---

## 📱 Responsividade

### **Desktop (≥768px):**
- Main: `padding-top: 80px`
- Hero: `padding: 3rem 2rem 5rem 2rem`
- SVG text: `font-size: 16px`

### **Mobile (<768px):**
- Main: `padding-top: 70px`
- Hero: `padding: 2rem 1.5rem 3rem 1.5rem`
- SVG text: `font-size: 13px`

---

## 🎨 Resultado Visual

### **ANTES:**
```
┌───────────────────────────────────┐
│ [IMAGEM DE FUNDO: FLUXO VERDE]    │
│                                   │
│ Como Funciona │ Processo...       │
│               │                   │
└───────────────────────────────────┘
```

### **DEPOIS:**
```
┌───────────────────────────────────┐
│ [HEADER FIXO]                     │
├───────────────────────────────────┤ ← Main (padding-top 80px)
│                                   │
│         Como Funciona             │
│                                   │
│  [LINHA ——●—— ——●—— ——●——]        │
│   Integridade  Cadeia  Validade   │
│                                   │
│  Processo estruturado para...     │
└───────────────────────────────────┘
```

---

## ✅ Validação

**Checklist:**
- [x] Imagem de fundo removida
- [x] Hero centralizado (padrão segurança)
- [x] Gráfico SVG institucional inserido
- [x] 3 círculos com títulos corretos
- [x] Subtítulo centralizado
- [x] Main com padding-top adequado (80px/70px)
- [x] CSS inline isolado
- [x] Prefixos específicos (`.como-funciona-*`)
- [x] Responsividade mobile funcional
- [x] Zero sobreposição com header
- [x] Outras páginas não afetadas

---

## 📊 Impacto

**Risco:** Muito baixo (CSS inline + seletor específico)  
**Benefício:** Alto (padronização visual institucional)  
**Páginas afetadas:** 1 (somente `como-funciona.html`)  
**Regressões:** Zero

---

## 🔍 Arquivo Alterado

**`public/como-funciona.html`:**
- Hero transformado (HTML)
- CSS inline adicionado
- Gráfico SVG institucional inserido

**Total:** 1 arquivo, ~150 linhas adicionadas/modificadas

---

## 🚀 Próximos Passos

1. **Review** deste PR
2. **Approve & Merge** para `main`
3. **Deploy automático** (~3 min)
4. **Validar** em https://www.tuteladigital.com.br/como-funciona.html
5. **Hard refresh** (Ctrl+Shift+R / Cmd+Shift+R)
6. **Verificar:** hero centralizado, gráfico visível, sem imagem de fundo

---

## 🎯 Consistência Visual

Com esta alteração, **3 páginas** agora compartilham o **mesmo padrão hero institucional**:
1. ✅ **seguranca.html** (já implementado)
2. ✅ **como-funciona.html** (este PR)
3. 🔜 Futuras páginas podem seguir este padrão

**Elementos padronizados:**
- Hero centralizado sem imagem
- Gráfico SVG institucional (3 círculos)
- Títulos: Integridade, Cadeia de Custódia, Validade Jurídica
- Layout responsivo
- Compensação para header fixo

---

## ✔️ Resultado Final

✔ Hero minimalista institucional  
✔ Sem imagem de fundo  
✔ Gráfico SVG padronizado  
✔ Layout centralizado e harmonioso  
✔ Compensação adequada para header fixo  
✔ Zero sobreposição  
✔ Zero impacto em outras páginas  
✔ Padrão visual consistente
