# 06 — Design System

## Índice
- [Existe um Design System?](#existe-um-design-system)
- [Paleta de cores](#paleta-de-cores)
- [Tipografia](#tipografia)
- [Espaçamento](#espaçamento)
- [Breakpoints e grid](#breakpoints-e-grid)
- [Sombras e raios](#sombras-e-raios)
- [Animações](#animações)
- [Fragmentação: três sistemas de tokens](#fragmentação-três-sistemas-de-tokens)

## Existe um Design System?

**Parcialmente.** Existe um arquivo central de design tokens bem estruturado e documentado — `public/assets/css/foundation/tokens.css` — que segue um padrão reconhecível de token system em camadas (paleta primitiva → tokens semânticos → aliases de compatibilidade → extensão de produto). O próprio arquivo se autodocumenta:

```css
/* ============================================================
   foundation/tokens.css
   Tutela Digital® — Design Tokens Globais
   ============================================================
   Organização:
     1. Paleta primitiva (cor pura, sem semântica)
     2. Tokens semânticos globais
     3. Escala tipográfica
     4. Espaçamento
     5. Extensão: Ativos Digitais (--ad-*)
   ============================================================ */
```

No entanto, esse sistema **não é o único** em uso — ver [Fragmentação](#fragmentação-três-sistemas-de-tokens) abaixo. Não há um arquivo de documentação de design system (Storybook, style guide HTML, Figma tokens exportados) — não identificado no projeto.

## Paleta de cores

### Paleta primitiva (`tokens.css:19-50`)

| Token | Valor | Uso |
| --- | --- | --- |
| `--primitive-green-990` | `#0a0f0d` | Fundo editorial quase-preto |
| `--primitive-green-980` | `#081a13` | — |
| `--primitive-green-970` | `#0c2418` | Header/footer marca escura |
| `--primitive-green-950` | `#0b241b` | Texto forte |
| `--primitive-green-900` | `#0f3a2a` | Superfície base / texto base |
| `--primitive-green-850` | `#134634` | — |
| `--primitive-green-800` | `#16503b` | — |
| `--primitive-green-700` | `#1b6b4d` | — |
| `--primitive-green-500` | `#1db954` | Acento global |
| `--primitive-green-400` | `#2db560` | Acento sutil |
| `--primitive-green-300` | `#4ade80` | Hover states brilhantes |
| `--primitive-green-200` | `#a8d9b8` | Acento claro |
| `--primitive-green-100` | `#deeade` | — |
| `--primitive-green-050` | `#edf4ed` | Superfície clara |
| `--primitive-neutral-000` a `-600` | `#ffffff` → `#4f7c6b` | Escala neutra esverdeada |
| `--primitive-gold-500` | `#b08a57` | Acento dourado (páginas de ativos) |
| `--primitive-red-700` | `#9f3627` | Danger/alerta |

### Tokens semânticos globais (`tokens.css:56-85`)

Organizados por papel: `--color-surface-*` (dark/base/muted/light/brand/darkest), `--color-text-*` (strong/base/muted/inverse/muted-dark), `--color-border-*` (soft/strong), `--color-accent*` (base/subtle/bright/light). Todos referenciam a paleta primitiva — não há valores hexadecimais soltos nessa camada.

A identidade visual é dominantemente **verde institucional escuro** (marca) com um acento dourado reservado para destaques editoriais nas páginas de Ativos Digitais, e vermelho reservado exclusivamente para estados de risco/perigo (ex.: resultado "alto risco" do diagnóstico).

## Tipografia

| Papel | Família | Fallback | Token |
| --- | --- | --- | --- |
| Display (títulos, site global) | Cormorant Garamond | Georgia, serif | `--font-display` |
| Corpo (site global) | Inter | -apple-system, BlinkMacSystemFont, sans-serif | `--font-body` |
| Display editorial (Ativos Digitais) | Playfair Display | Georgia, serif | `--font-editorial-display` |
| Corpo editorial (Ativos Digitais) | Source Serif 4 | Georgia, serif | `--font-editorial-body` |
| Monoespaçada editorial | DM Mono | monospace | `--font-editorial-mono` |

As fontes editoriais **exigem** um `<link>` adicional no `<head>` das páginas que usam a classe `.assets-pillar-page` — não são carregadas globalmente (comentário em `tokens.css:96-102`), o que é uma decisão consciente de performance (evita baixar 3 famílias extras em páginas que não precisam delas).

Escala de tamanhos (`tokens.css:108-121`): `--font-size-xs` (14px) até `--font-size-2xl` (40px), mais uma escala semântica fluida com `clamp()` para hero (`clamp(2rem, 4vw, 3rem)`) e título de seção (`clamp(1.75rem, 3vw, 2.5rem)`) — essas duas são as únicas que escalam responsivamente por viewport sem media query.

Pesos: regular (400), medium (500), semibold (600), bold (700). Alturas de linha: tight (1.3), base (1.6), relaxed (1.75).

## Espaçamento

Escala em `rem`, de `--space-xs` (0.5rem/8px) a `--space-3xl` (10rem/160px) (`tokens.css:140-153`), mais tokens semânticos derivados para seções (`--space-section`, `--space-section-hero`, `--space-section-tight`) e um valor único sem equivalente na escala global (`--space-feature: 7rem`, comentado explicitamente como exceção).

Largura máxima de conteúdo: `--max-width: 1200px` (padrão) e `--max-width-narrow: 800px`.

## Breakpoints e grid

**Não há uma escala de breakpoints tokenizada.** Uma varredura de todos os arquivos CSS por `@media(max-width:...)` encontrou **13 valores distintos** usados diretamente como número mágico, sem token correspondente:

`480px, 540px, 560px, 600px, 640px, 720px, 760px, 768px, 860px, 900px, 1024px, 1200px`

(768px é o mais comum, usado 15 vezes; a maioria dos demais aparece 1-4 vezes, sugerindo ajuste pontual por componente em vez de uma escala de grid deliberada). Há também inconsistência de formatação — `max-width:768px` (sem espaço) convive com `max-width: 768px` (com espaço) no mesmo arquivo (`layout/layout.css:24,30`). Ver [12-technical-debt.md](12-technical-debt.md).

Grid: o único sistema de grid CSS documentado como tal é `.features-grid` (`layout/layout.css:14-36`), que vai de 4 colunas → 2 colunas (≤1200px, variante `--security`) → 1 coluna (≤768px). Outros grids (`.verticals-grid--new`, `.pillars-grid--new`) são definidos ad hoc dentro dos arquivos de página (`homepage.css`), não em `layout.css`.

## Sombras e raios

Definidos apenas na extensão `--ad-*` (Ativos Digitais), não na camada global de tokens:

| Token | Valor |
| --- | --- |
| `--ad-shadow-xs` | `0 10px 24px rgba(16, 24, 40, 0.04)` |
| `--ad-shadow-sm` | `0 2px 20px rgba(10, 34, 24, 0.07), 0 1px 4px rgba(10, 34, 24, 0.04)` |
| `--ad-shadow-md` | `0 8px 32px rgba(10, 34, 24, 0.12)` |
| `--ad-radius` | `4px` |
| `--ad-radius-md` | `8px` |
| `--ad-radius-lg` | `14px` |
| `--ad-radius-xl` | `20px` |

Fora da extensão `--ad-*`, raios e sombras aparecem como valores literais espalhados nos arquivos de página (ex.: `.feature-item { border-radius: 14px; }` em `components/cards.css:13`) — não há tokens globais `--radius-*` ou `--shadow-*` na camada `foundation/`.

## Animações

`utilities/animations.css` concentra keyframes e classes utilitárias reutilizáveis. Padrão de "scroll reveal" (opacidade + translateY) é reimplementado de duas formas diferentes no projeto:
1. Classe `.reveal` + `IntersectionObserver` inline duplicado por página (ex. `public/index.html:422-441`).
2. Classe `.legal-animate` + `IntersectionObserver` centralizado em `public/assets/js/legal-animations.js`, exclusivo para `body.legal-page`.

Não há biblioteca de animação (GSAP, Framer Motion, AOS) — tudo é CSS transitions/keyframes + `IntersectionObserver` nativo.

## Fragmentação: três sistemas de tokens

Foram identificados **três namespaces de custom properties** coexistindo, com sobreposição conceitual mas valores não idênticos:

| Namespace | Onde é definido | Escopo | Exemplo de valor |
| --- | --- | --- | --- |
| `--color-*`, `--font-*`, `--space-*` | `foundation/tokens.css` (global) | Site inteiro | `--color-accent: #1db954` |
| `--ad-*` | `foundation/tokens.css` (seção 6, mesma fonte) | Páginas `/ativos-digitais/*` via `assets-digital.css` | `--ad-brand-dark: #0d2b1a` |
| `--ux-*` | `<style>` inline em `partials/ativos-digitais-pillar-styles.html` (não em `tokens.css`) | `.assets-page` (mesmo cluster de páginas) | `--ux-brand: #0f4a36` |

Os valores de marca de `--ad-*` e `--ux-*` são **próximos, mas não idênticos** (`#0d2b1a` vs. `#0f4a36` para tons de verde de marca equivalentes), o que sugere que o segundo sistema (`--ux-*`) foi introduzido posteriormente, em paralelo, sem consolidar com o primeiro (`--ad-*`) — reforçado pelo fato de `pages/ativos-digitais-pillar-styles.css` ter sido esvaziado com o comentário *"Deprecated: the active assets-page styles live in partials/ativos-digitais-pillar-styles.html"*. Isto é tratado como dívida técnica em [12-technical-debt.md](12-technical-debt.md), por representar duas fontes de verdade visual para o mesmo cluster de páginas.

## Documentos relacionados
- [05-components.md](05-components.md) — componentes que consomem esses tokens.
- [12-technical-debt.md](12-technical-debt.md) — impacto da fragmentação de tokens e breakpoints.
