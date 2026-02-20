# Proposta de Refatoração Incremental

## 1) Consolidação de funções duplicadas

### Problemas observados
- `MOBILE_MAX_WIDTH` é definido em mais de um arquivo (`mobile-menu.js` e `dropdown-menu.js`).
- Existe duplicação da lógica de abrir/fechar dropdown de idioma em `mobile-menu.js` e em listeners globais de `i18n.js`.
- Há padrões repetidos de seleção e manipulação de DOM (`querySelector`, `classList.toggle/remove`) espalhados por arquivos de navegação.

### Sugestão prática
Criar utilitários compartilhados em `public/assets/js/core/dom-utils.js` e `public/assets/js/core/breakpoints.js`:

- `isMobileViewport(width = 1200)`
- `toggleClass(el, className, force?)`
- `closeOnOutsideClick({root, toggle, onClose})`
- `getHeaderElements()` (retorna `nav`, `mobile button`, `lang dropdown`)

Com isso:
- `mobile-menu.js` e `dropdown-menu.js` passam a importar os mesmos helpers.
- A gestão de idioma fica centralizada apenas no `i18n.js` (ou em um módulo próprio de language UI), evitando corrida de eventos e comportamento divergente.

---

## 2) Extração de módulos por responsabilidade

### Problema atual
Os arquivos atuais misturam responsabilidades:
- `i18n.js` faz carregamento de tradução, regras de páginas legais, atualização de schema e também controla UI de dropdown de idioma.
- `navigation.js` contém lógica de SPA fallback, roteamento e animação de transição.

### Sugestão de estrutura
Organizar `public/assets/js/` em módulos:

- `core/`
  - `config.js` (constantes globais: breakpoints, duração de transição)
  - `dom-utils.js`
- `navigation/`
  - `router.js` (mapa de rotas + `navigateTo`)
  - `transitions.js` (fade in/out)
  - `dropdowns.js` (apenas nav dropdowns)
  - `mobile-menu.js`
- `i18n/`
  - `i18n-service.js` (carregar JSON + `t()`)
  - `i18n-page-rules.js` (regras de páginas legais)
  - `i18n-language-switcher.js` (UI seletor de idioma)

Essa divisão reduz acoplamento e facilita testes unitários por módulo.

---

## 3) Isolamento de escopo por página

### Problema atual
Há listeners e observers globais que rodam em todas as páginas (inclusive quando não necessário), por exemplo:
- Observador de páginas SPA no `i18n.js`.
- Inicialização de dropdown/menu mesmo em páginas que podem não possuir esses elementos.

### Sugestão prática
Adicionar bootstrap por página usando `data-page` no `<body>` (ou por pathname):

- `bootstrap/home.js`
- `bootstrap/governo.js`
- `bootstrap/empresas.js`
- `bootstrap/pessoas.js`
- `bootstrap/legal.js`

Fluxo:
1. `main.js` detecta `document.body.dataset.page`.
2. Carrega somente os módulos daquela página.
3. Mantém `header` e `i18n service` como compartilhados, mas ativa recursos opcionais apenas quando o DOM exigir.

Resultado esperado:
- Menos listeners globais.
- Menor custo de execução por página.
- Menor risco de regressão cruzada entre páginas legais e páginas comerciais.

---

## 4) Plano incremental (baixo risco)

1. **Fase 1 – Shared constants/utilities**
   - Extrair `MOBILE_MAX_WIDTH` e helpers de DOM.
   - Ajustar `mobile-menu.js` e `dropdown-menu.js` para consumir utilitários.

2. **Fase 2 – Centralização do language dropdown**
   - Remover listeners duplicados de idioma em um dos pontos.
   - Manter fonte única da verdade para abrir/fechar e troca de idioma.

3. **Fase 3 – i18n desacoplado**
   - Separar carregamento de traduções (`i18n-service`) das regras de UI.

4. **Fase 4 – bootstrap por página**
   - Introduzir inicialização por `data-page` e reduzir listeners globais.

5. **Fase 5 – limpeza técnica**
   - Remover logs de debug (`console.log`) e manter apenas logs de erro/warn controlados.

---

## 5) Ganhos esperados
- Redução de código duplicado e de inconsistências entre comportamentos mobile/desktop.
- Melhor legibilidade e manutenção (arquivos menores e mais focados).
- Facilidade para evoluir páginas específicas sem afetar toda a navegação.
- Preparação para migração futura para bundling modular (Vite/Webpack) sem reescrever tudo.
