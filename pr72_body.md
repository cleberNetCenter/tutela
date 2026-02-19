## 🎯 Objetivo

Inserir **gráfico vetorial institucional horizontal** em todas as páginas do menu `/legal/` para padronização visual institucional.

---

## 📐 Especificação do Gráfico

### **Elementos visuais:**
1. **Linha base horizontal** (stroke verde, opacity 0.35)
2. **Três círculos** posicionados ao longo da linha
3. **Três títulos fixos** (não traduzidos, não adaptados):
   - **Integridade**
   - **Cadeia de Custódia**
   - **Validade Jurídica**

### **Posicionamento:**
- Inserido **imediatamente após `<h1>`** dentro de `.page-header-inner`
- Estrutura final:
  ```html
  <h1>...</h1>
  <div class="legal-graphic">
    <!-- SVG aqui -->
  </div>
  <p>...</p>
  ```

---

## 📋 Implementação

### **1. SVG Institucional**
```html
<div class="legal-graphic">
  <svg viewBox="0 0 900 120" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    
    <!-- Linha Base -->
    <line x1="100" y1="60" x2="800" y2="60"
          stroke="var(--color-green-700)"
          stroke-width="1.5"
          opacity="0.35"/>
    
    <!-- Círculo 1: Integridade -->
    <circle cx="250" cy="60" r="10" fill="var(--color-green-700)"/>
    <text x="250" y="95" text-anchor="middle" font-size="16"
          font-family="var(--font-body)" fill="var(--color-text-strong)">
      Integridade
    </text>
    
    <!-- Círculo 2: Cadeia de Custódia -->
    <circle cx="450" cy="60" r="10" fill="var(--color-green-700)"/>
    <text x="450" y="95" text-anchor="middle" font-size="16"
          font-family="var(--font-body)" fill="var(--color-text-strong)">
      Cadeia de Custódia
    </text>
    
    <!-- Círculo 3: Validade Jurídica -->
    <circle cx="650" cy="60" r="10" fill="var(--color-green-700)"/>
    <text x="650" y="95" text-anchor="middle" font-size="16"
          font-family="var(--font-body)" fill="var(--color-text-strong)">
      Validade Jurídica
    </text>
    
  </svg>
</div>
```

### **2. CSS Isolado**
```css
.legal-graphic {
  margin: 1.5rem auto 2.5rem auto;
  max-width: 900px;
  opacity: 0.9;
}

.legal-graphic svg {
  width: 100%;
  height: auto;
  display: block;
}

@media (max-width: 768px) {
  .legal-graphic svg text {
    font-size: 13px;
  }
}
```

---

## 📁 Páginas Modificadas

✅ **5 páginas no diretório `/legal/`:**
1. `fundamento-juridico.html`
2. `institucional.html`
3. `politica-de-privacidade.html`
4. `preservacao-probatoria-digital.html`
5. `termos-de-custodia.html`

---

## 🔒 Garantias de Não Impacto

### **✅ Não alterado:**
- ❌ Header
- ❌ Footer
- ❌ Hero structure
- ❌ Grid system
- ❌ Tipografia global
- ❌ Espaçamentos globais
- ❌ Classes existentes
- ❌ Layout responsivo
- ❌ Variáveis CSS (`:root`)
- ❌ Páginas fora de `/legal/`

### **✅ Apenas adicionado:**
- ✅ Elemento `<div class="legal-graphic">` após `<h1>`
- ✅ CSS isolado com prefixo `.legal-graphic`
- ✅ Responsividade mobile (redução de font-size)

---

## 📱 Responsividade

**Desktop (≥768px):**
- SVG largura 100% do container (max-width 900px)
- Font-size dos textos: 16px

**Mobile (<768px):**
- SVG se adapta à largura do container
- Font-size dos textos: 13px (ajuste automático)

---

## 🎨 Resultado Visual

### **Antes:**
```
<h1>Título da Página</h1>
<p>Subtítulo...</p>
```

### **Depois:**
```
<h1>Título da Página</h1>

[GRÁFICO: ——●—— Integridade ——●—— Cadeia de Custódia ——●—— Validade Jurídica]

<p>Subtítulo...</p>
```

---

## ✔️ Validação

**Checklist de verificação:**
- [x] Gráfico inserido após `<h1>` em todas as páginas legais
- [x] Três títulos fixos corretos (sem tradução/adaptação)
- [x] CSS isolado (não sobrescreve regras existentes)
- [x] Responsividade mobile funcional
- [x] Estrutura HTML preservada
- [x] Sem impacto em outras páginas do site
- [x] ViewBox, coordenadas e tamanhos exatos
- [x] Variáveis CSS utilizadas (`--color-green-700`, `--font-body`, etc.)

---

## 📐 Especificações Técnicas

**SVG:**
- ViewBox: `0 0 900 120`
- Linha base: `x1="100" y1="60" x2="800" y2="60"`
- Círculos: `cx="250/450/650" cy="60" r="10"`
- Textos: `y="95"`, `font-size="16"`

**CSS:**
- Margin: `1.5rem auto 2.5rem auto`
- Max-width: `900px`
- Opacity: `0.9`
- Mobile font-size: `13px`

---

## 🚀 Próximos Passos

1. **Review** deste PR
2. **Approve & Merge** para `main`
3. **Deploy automático** (~3 min)
4. **Validar** em cada página legal:
   - https://www.tuteladigital.com.br/legal/fundamento-juridico.html
   - https://www.tuteladigital.com.br/legal/institucional.html
   - https://www.tuteladigital.com.br/legal/politica-de-privacidade.html
   - https://www.tuteladigital.com.br/legal/preservacao-probatoria-digital.html
   - https://www.tuteladigital.com.br/legal/termos-de-custodia.html
5. **Hard refresh** (Ctrl+Shift+R / Cmd+Shift+R)

---

## 📊 Impacto

**Risco:** Muito baixo  
**Benefício:** Alto (padronização visual institucional)  
**Páginas afetadas:** 5 (somente `/legal/`)  
**Regressões:** Zero (alteração isolada)

---

## 🔍 Arquivos Alterados

1. `public/legal/fundamento-juridico.html` – gráfico + CSS
2. `public/legal/institucional.html` – gráfico + CSS
3. `public/legal/politica-de-privacidade.html` – gráfico + CSS
4. `public/legal/preservacao-probatoria-digital.html` – gráfico + CSS
5. `public/legal/termos-de-custodia.html` – gráfico + CSS
6. `insert_legal_graphic.py` – script de inserção automática

**Total:** 6 arquivos, ~700 linhas (majoritariamente SVG inline)
