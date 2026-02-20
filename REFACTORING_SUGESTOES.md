# Sugestões de refatoração: consolidação, extração de módulos e isolamento por página

## 1) Consolidação de funções duplicadas

### Duplicações concretas detectadas

| Comportamento | Implementação atual | Sugestão de consolidação |
|---|---|---|
| Regra de breakpoint mobile (`<= 1200`) | `isMobileViewport()` em `mobile-menu.js` e `isMobile()` em `dropdown-menu.js` | Criar `core/breakpoints.js` com `isMobileViewport(maxWidth = 1200)` |
| Fechamento por clique fora | `document.addEventListener('click', ...)` separado em `mobile-menu.js` (menu + idioma) e `dropdown-menu.js` (dropdowns) | Criar helper `onClickOutside(container, handler, exceptions = [])` em `core/events.js` |
| Fechamento em lote de elementos ativos | `closeMobileMenu()` e `closeAllDropdowns()` com lógica semelhante | Criar `closeActiveBySelector(selector, activeClass = 'active')` em `core/dom.js` |
| Lock de scroll de `<body>` | `document.body.style.overflow` manipulado diretamente no menu mobile | Criar `setBodyScrollLocked(true/false)` em `core/dom.js` |

### Quick win sugerido (baixo risco)
1. Criar `MOBILE_BREAKPOINT = 1200` em um único módulo.
2. Substituir chamadas locais de viewport para usar o helper único.
3. Trocar listeners globais repetidos por uma função utilitária compartilhada.

---

## 2) Extração de módulos por responsabilidade

### Estrutura alvo sugerida

```text
public/assets/js/
  core/
    breakpoints.js
    dom.js
    events.js
  features/
    mobile-menu.js
    nav-dropdown.js
    language-switcher.js
  pages/
    home.js
    empresas.js
    governo.js
    pessoas.js
    legal.js
  main.js
```

### Regras de fronteira
- **`core/*`**: utilitários puros (sem dependência de elementos de página).
- **`features/*`**: componentes compartilháveis (header/menu/dropdown/idioma).
- **`pages/*`**: apenas comportamento específico da página.
- **`main.js`**: bootstrap e composição por `data-page`.

### Sugestão de extração imediata
- Mover a lógica de dropdown de idioma para `features/language-switcher.js`.
- Renomear `dropdown-menu.js` para `features/nav-dropdown.js` (papel mais claro).
- Manter `navigation.js` apenas para navegação interna (ou descontinuar se o projeto já é MPA puro).

---

## 3) Isolamento de escopo por página

### Problema atual
Scripts globais inicializam em todas as páginas, mesmo quando os alvos não existem, aumentando `if (!el) return` e acoplamento implícito.

### Padrão recomendado
1. Definir `data-page` no `<body>` de cada HTML.
2. Centralizar inicialização em `main.js`.
3. Executar apenas o módulo da página atual.

```js
import { initHeaderFeatures } from './features/header.js';
import { initHome } from './pages/home.js';
import { initEmpresas } from './pages/empresas.js';
import { initGoverno } from './pages/governo.js';
import { initPessoas } from './pages/pessoas.js';
import { initLegal } from './pages/legal.js';

const page = document.body.dataset.page;

const pageRegistry = {
  home: initHome,
  empresas: initEmpresas,
  governo: initGoverno,
  pessoas: initPessoas,
  legal: initLegal,
};

initHeaderFeatures();
pageRegistry[page]?.();
```

### Mapa sugerido de escopo

| Página | `data-page` | Inicializar | Não inicializar |
|---|---|---|---|
| `index.html` | `home` | hero, CTA, destaques | regras legais |
| `empresas.html` | `empresas` | jornadas B2B | fluxo cidadão e governo |
| `governo.html` | `governo` | seções institucionais | blocos comerciais B2B |
| `pessoas.html` | `pessoas` | jornadas individuais | fluxos de contratação pública |
| `legal/*.html` | `legal` | breadcrumbs + ajustes jurídicos | scripts de hero comercial |

---

## 4) Plano incremental (4 fases)

1. **Fase 1 – Core compartilhado**
   - Criar `core/breakpoints.js`, `core/dom.js`, `core/events.js`.
   - Substituir funções duplicadas nos arquivos atuais.
2. **Fase 2 – Features desacopladas**
   - Extrair idioma e dropdown para módulos próprios.
   - Reduzir listeners globais concorrentes.
3. **Fase 3 – Bootstrap por página**
   - Adicionar `data-page` nos HTMLs.
   - Introduzir `main.js` com registry.
4. **Fase 4 – Limpeza e observabilidade**
   - Remover logs de debug permanentes (`console.log`/`console.warn` não essenciais).
   - Padronizar contrato `init()/destroy()` por feature.

---

## 5) Métricas de sucesso

- Menos listeners no `document` e `window`.
- Uma única fonte da verdade para breakpoint mobile.
- Menos condicionais defensivas em scripts globais.
- Menor impacto cruzado ao alterar páginas específicas.
