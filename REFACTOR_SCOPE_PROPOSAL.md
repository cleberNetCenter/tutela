# Proposta de Refatoração Incremental

## 1) Consolidação de funções duplicadas

### Duplicações mapeadas
- `MOBILE_MAX_WIDTH = 1200` aparece em **`mobile-menu.js`** e **`dropdown-menu.js`**.
- A lógica de detectar viewport mobile (`window.innerWidth <= 1200`) também se repete.
- Existe lógica duplicada de fechar elementos ao clicar fora (`document.addEventListener('click', ...)`) em múltiplos pontos.
- O dropdown de idioma é inicializado no `mobile-menu.js`, enquanto o `i18n.js` também atualiza/coordena UI de idioma.

### Sugestão prática
Criar utilitários compartilhados em `public/assets/js/core/`:

- `breakpoints.js`
  - `export const MOBILE_MAX_WIDTH = 1200`
  - `export function isMobileViewport()`
- `dom-utils.js`
  - `export function getHeaderElements()`
  - `export function closeOnOutsideClick({ root, ignore = [], onClose })`
  - `export function safeToggle(el, className, force)`
- `events.js`
  - helper para registrar/remover listeners de forma centralizada.

Com isso, `mobile-menu.js` e `dropdown-menu.js` passam a depender da mesma base utilitária, reduzindo divergência comportamental entre páginas.

---

## 2) Extração de módulos por responsabilidade

### Problema atual
- `i18n.js` acumula responsabilidades de serviço, regras de conteúdo jurídico, renderização de aviso e controle de UI.
- `mobile-menu.js` mistura menu mobile e dropdown de idioma.
- `dropdown-menu.js` mistura inicialização, validação de estrutura e regras de interação.

### Estrutura sugerida
Organizar `public/assets/js/` por domínio:

- `core/`
  - `config.js` (constantes globais)
  - `breakpoints.js`
  - `dom-utils.js`
- `navigation/`
  - `mobile-menu.js`
  - `nav-dropdowns.js`
  - `outside-click.js`
- `i18n/`
  - `i18n-service.js` (load/switch/t)
  - `i18n-legal-rules.js` (detecção + aviso para páginas legais)
  - `language-switcher-ui.js` (somente interação do seletor)
- `bootstrap/`
  - `main.js` (roteia inicialização por página)

Isso permite testar e evoluir cada parte sem risco de quebrar o fluxo completo.

---

## 3) Isolamento de escopo por página

### Objetivo
Evitar listeners e inicializações globais em páginas onde os elementos não existem.

### Implementação recomendada
Adicionar `data-page` no `<body>` de cada HTML e usar um bootstrap único:

```html
<body data-page="home">
```

```js
// bootstrap/main.js
const page = document.body.dataset.page;
initSharedHeader();

if (page === 'home') initHome();
if (page === 'governo') initGoverno();
if (page === 'empresas') initEmpresas();
if (page === 'pessoas') initPessoas();
if (page === 'legal') initLegal();
```

### Benefícios imediatos
- Menos listeners em páginas legais.
- Menos side effects entre i18n e navegação.
- Menor custo de execução por página e debug mais previsível.

---

## 4) Plano incremental (baixo risco)

1. **Fase 1 – Core compartilhado**
   - Extrair `MOBILE_MAX_WIDTH`, `isMobileViewport` e helper de outside-click.
2. **Fase 2 – Navegação enxuta**
   - Separar menu mobile e dropdowns de navegação em módulos distintos.
3. **Fase 3 – i18n desacoplado**
   - Isolar `i18n-service` e mover regras jurídicas para módulo dedicado.
4. **Fase 4 – Bootstrap por página**
   - Introduzir `data-page` e inicializadores específicos.
5. **Fase 5 – Hardening**
   - Remover logs de debug e padronizar telemetria de erro/aviso.

---

## 5) Checklist rápido de revisão por PR

- [ ] Nenhuma constante de breakpoint duplicada.
- [ ] Nenhum listener global sem necessidade de página.
- [ ] Dropdown de idioma inicializado em **um único módulo**.
- [ ] `i18n` sem dependência direta de regras de navegação.
- [ ] Módulos com responsabilidade única e nomes previsíveis.

---

## 6) Resultado esperado

- Redução de duplicação em navegação/header.
- Menor acoplamento entre i18n, menu e regras jurídicas.
- Melhor manutenção com evolução isolada por página.
- Base pronta para bundling futuro (Vite/Webpack) sem reescrita completa.
