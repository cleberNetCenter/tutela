# Sugestões de refatoração: consolidação, extração de módulos e isolamento por página

## Objetivo
Reduzir acoplamento entre scripts globais, eliminar duplicação no header e criar execução por escopo de página para evitar efeitos colaterais entre `index`, `empresas`, `governo`, `pessoas` e páginas legais.

---

## 1) Consolidação de funções duplicadas

### Duplicações práticas no código atual

| Tema | Onde aparece hoje | Problema | Consolidação sugerida |
|---|---|---|---|
| Detecção de viewport mobile | `mobile-menu.js` e `dropdown-menu.js` | Duas regras para o mesmo comportamento | `core/breakpoints.js` com `isMobileViewport(maxWidth = 1200)` |
| Fechamento ao clicar fora | listeners globais diferentes em menu mobile, dropdown e idioma | Concorrência de listeners + comportamento inconsistente | `core/events.js` com `onClickOutside(container, handler, exceptions)` |
| Fechamento de itens ativos | lógica semelhante para menu, idioma e dropdown | Repetição de seleção/manipulação de classes | `core/dom.js` com `closeActiveBySelector(selector, activeClass='active')` |
| Lock de scroll do body | manipulação direta de `document.body.style.overflow` | risco de esquecer unlock e criar estado inválido | `core/dom.js` com `setBodyScrollLocked(isLocked)` |

### Mapeamento direto (estado atual → alvo)

| Arquivo atual | Função/bloco atual | Novo módulo sugerido |
|---|---|---|
| `public/assets/js/dropdown-menu.js` | `isMobile()` | `core/breakpoints.isMobileViewport()` |
| `public/assets/js/mobile-menu.js` | `isMobileViewport()` | `core/breakpoints.isMobileViewport()` |
| `public/assets/js/dropdown-menu.js` | `closeAllDropdowns(exceptDropdown)` | `features/header/nav-dropdown.closeAll()` |
| `public/assets/js/mobile-menu.js` | `closeMobileMenu()` | `features/header/mobile-menu.close()` |
| `public/assets/js/mobile-menu.js` | listener de click fora (`onDocumentClick`) | `core/events.onClickOutside()` |
| `public/assets/js/mobile-menu.js` | listener de idioma (`onDocumentLangClick`) | `core/events.onClickOutside()` |

> Resultado esperado: reduzir duplicações de utilitários de viewport, click fora e fechamento de estados ativos em 1 ponto de verdade.

### Contrato recomendado de utilitários

```js
// core/breakpoints.js
export const MOBILE_BREAKPOINT = 1200;
export const isMobileViewport = (maxWidth = MOBILE_BREAKPOINT) => window.innerWidth <= maxWidth;

// core/events.js
export function onClickOutside(container, handler, exceptions = []) {
  document.addEventListener('click', (event) => {
    const clickInsideContainer = container?.contains(event.target);
    const clickInsideException = exceptions.some((el) => el?.contains?.(event.target));
    if (!clickInsideContainer && !clickInsideException) handler(event);
  });
}

// core/dom.js
export const setBodyScrollLocked = (isLocked) => {
  document.body.style.overflow = isLocked ? 'hidden' : '';
};
```

---

## 2) Extração de módulos por responsabilidade

### Estrutura alvo proposta

```text
public/assets/js/
  core/
    breakpoints.js
    dom.js
    events.js
  features/
    header/
      mobile-menu.js
      nav-dropdown.js
      language-switcher.js
      index.js
  pages/
    home.js
    empresas.js
    governo.js
    pessoas.js
    legal.js
  main.js
```

### Regras de fronteira
- `core/*`: funções puras e utilitárias sem acoplamento com markup específico.
- `features/header/*`: somente comportamento compartilhado do cabeçalho.
- `pages/*`: regras específicas da página (hero, seções e CTAs locais).
- `main.js`: ponto único de bootstrap e roteamento por `data-page`.

### Extrações imediatas (baixo risco)
1. Mover bloco de idioma para `features/header/language-switcher.js`.
2. Renomear `dropdown-menu.js` para `features/header/nav-dropdown.js`.
3. Criar `features/header/index.js` com `initHeaderFeatures()` para inicializar apenas menu + dropdown + idioma.
4. Padronizar API mínima de cada feature com `init()` e `close()`.

### Interface padrão sugerida para componentes de header

```js
// features/header/mobile-menu.js
export function createMobileMenu(deps) {
  const { nav, button, setBodyScrollLocked, isMobileViewport, onClickOutside } = deps;

  function open() { /* ... */ }
  function close() { /* ... */ }
  function toggle() { /* ... */ }
  function init() { /* ... */ }

  return { init, open, close, toggle };
}
```

---

## 3) Isolamento de escopo por página

### Problema atual
Parte dos scripts globais executa em páginas onde os elementos-alvo não existem, exigindo vários guard clauses e aumentando a chance de regressão cruzada.

Além disso, há páginas com inclusão duplicada de scripts do header (por exemplo, `navigation.js` e `dropdown-menu.js` aparecem duas vezes em algumas páginas legais), o que aumenta risco de listeners duplicados e comportamento não determinístico.

### Padrão recomendado

```js
// main.js
import { initHeaderFeatures } from './features/header/index.js';
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

### Convenção de escopo por página

| Página | `data-page` | Inicializa | Não inicializa |
|---|---|---|---|
| `index.html` | `home` | hero e CTAs da home | blocos legais |
| `empresas.html` | `empresas` | conteúdo B2B | regras de governo/pessoas |
| `governo.html` | `governo` | conteúdo institucional | blocos comerciais |
| `pessoas.html` | `pessoas` | jornada individual | seções de contratação pública |
| `legal/*.html` | `legal` | breadcrumbs/ajustes jurídicos | hero e scripts comerciais |

### Ajuste mínimo em HTML

```html
<body data-page="home">
  <!-- conteúdo -->
  <script type="module" src="/assets/js/main.js"></script>
</body>
```

### Passo de transição (sem migrar tudo para ES modules de uma vez)

Se quiser reduzir risco de rollout, primeiro mantenha scripts clássicos e use um bootstrap condicional:

```html
<body data-page="governo">
  <script src="/assets/js/header.bundle.js"></script>
  <script src="/assets/js/page-bootstrap.js"></script>
</body>
```

```js
// page-bootstrap.js
(function initPageScope() {
  const page = document.body.dataset.page;
  const registry = {
    home: window.TutelaPages?.home,
    empresas: window.TutelaPages?.empresas,
    governo: window.TutelaPages?.governo,
    pessoas: window.TutelaPages?.pessoas,
    legal: window.TutelaPages?.legal,
  };

  registry[page]?.init?.();
})();
```

---

## 4) Plano incremental de implementação

1. **Fase 1 — Core compartilhado**
   - Criar `core/breakpoints.js`, `core/events.js`, `core/dom.js`.
   - Substituir duplicações sem alterar comportamento visual.
2. **Fase 2 — Header modular**
   - Extrair `language-switcher`, `nav-dropdown`, `mobile-menu` para `features/header`.
   - Expor `initHeaderFeatures()` em um único ponto.
3. **Fase 3 — Boot por página**
   - Adicionar `data-page` em todas as páginas MPA.
   - Migrar para `main.js` + `pageRegistry`.
4. **Fase 4 — Limpeza**
   - Remover globais legadas (`window.toggleMobileMenu` etc.).
   - Padronizar contrato `init()/destroy()` para componentes.

---

## 5) Critérios de sucesso

- Uma única fonte de verdade para breakpoint mobile.
- Redução de listeners globais concorrentes em `document/window`.
- Diminuição de condicionais defensivas em scripts globais.
- Alterações em páginas específicas sem impacto nas demais.

---

## 6) Backlog priorizado

| Prioridade | Item | Impacto | Esforço |
|---|---|---|---|
| P0 | Unificar `isMobile` + body scroll lock | Alto | Baixo |
| P0 | Criar `initHeaderFeatures()` | Alto | Baixo |
| P0 | Remover inclusões duplicadas de `navigation.js`/`dropdown-menu.js` nas páginas legais | Alto | Baixo |
| P1 | Extrair `onClickOutside` | Médio/Alto | Médio |
| P1 | Introduzir `data-page` + `main.js` | Alto | Médio |
| P2 | Remover logs de debug permanentes | Médio | Baixo |

### Ordem sugerida
1. Consolidar utilitários (`core/*`).
2. Organizar header (`features/header/*`).
3. Ativar bootstrap por página (`main.js`).
4. Limpar legado e estabilizar (`destroy`, logs, globais).


---

## 7) Sugestão direta (curto prazo) para o cenário atual

### Consolidar funções duplicadas (primeiro)
- Criar `public/assets/js/core/breakpoints.js` e centralizar o breakpoint `1200`.
  - `mobile-menu.js`: substituir `isMobileViewport()`.
  - `dropdown-menu.js`: substituir `isMobile()`.
- Criar `public/assets/js/core/scroll-lock.js` com `setBodyScrollLocked(isLocked)`.
  - `mobile-menu.js`: trocar escrita direta em `document.body.style.overflow`.
- Criar `public/assets/js/core/click-outside.js` com um helper único.
  - Reusar no fechamento de menu mobile, dropdown de navegação e dropdown de idioma.

### Extrair módulos por domínio (segundo)
- Quebrar `mobile-menu.js` em 2 módulos:
  - `features/header/mobile-menu.js`
  - `features/header/language-switcher.js`
- Evoluir `dropdown-menu.js` para `features/header/nav-dropdown.js`.
- Manter um agregador único `features/header/index.js` com `initHeaderFeatures()`.

### Isolar escopo por página (terceiro)
- Adicionar `data-page` no `<body>` de cada página MPA.
- Criar um bootstrap `public/assets/js/main.js` com registro por página:
  - `home`, `empresas`, `governo`, `pessoas`, `legal`.
- Inicializar sempre o header compartilhado e apenas o módulo da página atual.

### Ganhos esperados
- Menos regressões cruzadas entre páginas.
- Menos listeners globais concorrentes no `document`.
- Base pronta para remover scripts legados sem quebrar a navegação.
