# Sugestões de refatoração: consolidação, modularização e isolamento por página

## 1) Consolidação de funções duplicadas

### Oportunidades observadas
- **Detecção de viewport mobile** aparece em mais de um script (`isMobileViewport` em `mobile-menu.js` e `isMobile` em `dropdown-menu.js`) com a mesma regra (`<= 1200`).
- **Fechamento de menus/dropdowns ao clicar fora** está distribuído entre múltiplos listeners globais (`document.addEventListener('click', ...)`) em `mobile-menu.js` e `dropdown-menu.js`.
- **Fluxos de inicialização em `DOMContentLoaded`** estão repetidos em blocos separados nos scripts de navegação e menu.

### Mapa objetivo de duplicações (ponto de partida)

| Comportamento | Onde aparece hoje | Sugestão de unificação |
|---|---|---|
| Regra de mobile (`<=1200`) | `mobile-menu.js` (`isMobileViewport`) e `dropdown-menu.js` (`isMobile`) | `core/breakpoints.js` com `isMobileViewport()` |
| Clique fora para fechar | listeners globais em `mobile-menu.js` (menu + idiomas) e `dropdown-menu.js` | helper `onClickOutside()` em `core/events.js` |
| Lock de rolagem do body | `mobile-menu.js` altera `document.body.style.overflow` | `setBodyScrollLocked(true/false)` em `core/dom-utils.js` |
| Fechar grupos de elementos ativos | `closeMobileMenu()` e `closeAllDropdowns()` | `closeAllBySelector(selector, className='active')` |

### Sugestão prática
Consolidar utilidades em um módulo único (ex.: `ui-helpers.js`) com funções puras e reutilizáveis:
- `isMobileViewport(maxWidth = 1200)`
- `onClickOutside(container, trigger, handler)`
- `toggleBodyScroll(lock)`
- `closeAll(elements, className = 'active')`

**Benefício:** reduz duplicação de lógica e elimina divergência de comportamento entre menu mobile, dropdown de navegação e dropdown de idioma.

---

## 2) Extração de módulos (separação por responsabilidade)

### Situação atual
Os arquivos atuais já possuem separação inicial (`mobile-menu.js`, `dropdown-menu.js`, `i18n.js`), mas ainda carregam muita lógica de orquestração via listeners globais e acoplamento ao DOM completo.

### Proposta de módulos
Estrutura sugerida:

```text
public/assets/js/
  core/
    dom-utils.js
    events.js
    breakpoints.js
  features/
    mobile-menu.js
    nav-dropdown.js
    language-switcher.js
    legal-notice.js
    i18n-engine.js
  pages/
    home.js
    empresas.js
    governo.js
    pessoas.js
    legal.js
  main.js
```

### Critérios de extração
- **`core/*`**: funções sem conhecimento de página (helpers e infraestrutura).
- **`features/*`**: componentes reutilizáveis entre páginas.
- **`pages/*`**: regra específica de conteúdo e comportamento local.
- **`main.js`**: bootstrap e composição, sem regra de negócio.

**Benefício:** facilita manutenção incremental e testes unitários por módulo.

---

## 3) Isolamento de escopo por página

### Problema típico atual
Scripts globais tentam inicializar comportamentos em páginas onde os elementos não existem, exigindo muitos `if (!el) return` e gerando acoplamento implícito.

### Estratégia recomendada
1. Definir identificador de página no HTML (ex.: `<body data-page="governo">`).
2. Em `main.js`, carregar/inicializar apenas o módulo correspondente:

```js
const page = document.body.dataset.page;

const registry = {
  home: initHome,
  empresas: initEmpresas,
  governo: initGoverno,
  pessoas: initPessoas,
  legal: initLegal,
};

registry[page]?.();
```

3. Deixar `features` independentes e chamadas só quando necessárias por cada `pages/*`.

**Benefício:** reduz efeitos colaterais, melhora performance e torna cada página previsível.

### Matriz de isolamento recomendada

| Página | `data-page` | O que inicializar | O que NÃO inicializar |
|---|---|---|---|
| Home | `home` | hero, destaques, CTA específicos | regras de páginas legais |
| Empresas | `empresas` | blocos de soluções B2B + CTA dedicado | componentes de governo/pessoas |
| Governo | `governo` | seções institucionais + fluxos de contratação | componentes comerciais de empresas |
| Pessoas | `pessoas` | conteúdo cidadão e variações de jornada individual | fluxos específicos de governo |
| Legal | `legal` | breadcrumbs, notices jurídicos, i18n legal | scripts de landing/hero comercial |

> Observação: `features` globais (menu mobile, dropdown de navegação e troca de idioma) continuam reutilizáveis, porém carregados via `main.js` somente quando o DOM da página realmente contém os elementos-alvo.

---

## 4) Plano incremental de implementação (baixo risco)

1. **Fase 1 — utilidades compartilhadas**
   - Criar `core/breakpoints.js` e `core/dom-utils.js`.
   - Migrar `isMobileViewport`/`isMobile` para uma única função.
2. **Fase 2 — componentes de navegação**
   - Extrair dropdown de idioma para `features/language-switcher.js`.
   - Padronizar fechamento por clique externo com helper comum.
3. **Fase 3 — bootstrap por página**
   - Adicionar `data-page` nos HTMLs principais.
   - Criar `main.js` com registry de inicialização.
4. **Fase 4 — i18n desacoplado**
   - Separar motor (`i18n-engine`) de comportamentos legais (`legal-notice`).

---

## 5) Quick wins imediatos

- Substituir constantes mágicas de breakpoint por constante central.
- Unificar listeners de clique externo para evitar múltiplos handlers concorrentes.
- Consolidar regras de lock de scroll (`document.body.style.overflow`) em helper único.
- Introduzir convenção `initX()` + `destroyX()` para cada feature (preparando eventual navegação parcial futuramente).

---

## 6) Métricas de sucesso da refatoração

- Redução do número total de listeners globais no `document`.
- Redução de blocos defensivos (`if (!el) return`) em scripts globais.
- Menor tempo de onboarding para alterar uma página sem impacto em outras.
- Menor difusão de regras de breakpoint (uma única fonte da verdade).
