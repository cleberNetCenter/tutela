# 08 — Performance

## Índice
- [Resumo](#resumo)
- [Carregamento de CSS](#carregamento-de-css)
- [Carregamento de JavaScript](#carregamento-de-javascript)
- [Fontes](#fontes)
- [Imagens](#imagens)
- [Cache e cache-busting](#cache-e-cache-busting)
- [Scripts de terceiros](#scripts-de-terceiros)
- [Lazy loading e code splitting](#lazy-loading-e-code-splitting)
- [Rede e requisições client-side em runtime](#rede-e-requisições-client-side-em-runtime)

## Resumo

Como o site é HTML/CSS/JS estático sem build, não há nenhuma das otimizações automáticas que um bundler forneceria (minificação, tree-shaking, code-splitting por rota, compressão de imagem no build). O desempenho depende inteiramente de decisões manuais feitas artigo por artigo, e do que o Nginx de produção fizer em termos de compressão/cache HTTP (não versionado, necessita validação).

## Carregamento de CSS

`public/assets/css/main.css` é um agregador que usa `@import` **nativo do CSS** (não pré-processado) para compor 8 categorias de estilo, na ordem: foundation → layout → utilities → components → sections → pages → animations → legacy (`main.css:5-45`). Isso tem uma implicação de performance real: `@import` no CSS é resolvido **sequencialmente pelo navegador em cascata de requisições**, ao contrário de um bundler que concatenaria tudo em um único arquivo antes de servir. Cada página então soma a esse agregador 1-3 folhas de estilo adicionais específicas (ex.: `public/index.html:38-40` carrega `main.css`, `styles-header-final.css` e `homepage.css` como três `<link>` separados, além dos `@import` internos de `main.css`).

Além disso, seis páginas legais e a pillar page de Ativos Digitais ainda referenciam via `<link>` arquivos CSS que foram esvaziados e reduzidos a um comentário de "descontinuado" (ex.: `pages/fundamento-juridico.css`, `pages/politica-de-privacidade.css`, `pages/termos-de-custodia.css`, `pages/preservacao-probatoria-digital.css`, `dropdown-menu.css`) — cada `<link>` desses ainda gera uma requisição HTTP (pequena, mas não-zero) sem entregar nenhum estilo. Ver [12-technical-debt.md](12-technical-debt.md).

Não há minificação — todos os arquivos CSS são servidos com comentários, indentação e espaçamento completos.

## Carregamento de JavaScript

Os 4 scripts globais (`mobile-menu.js`, `dropdown-menu.js`, `i18n.js`, `search.js`) são declarados com `defer` em `public/partials/scripts.html`, o que é a prática correta para não bloquear o parsing do HTML. Todos são carregados em **todas** as páginas, mesmo quando boa parte do código não se aplica (ex.: `search.js` roda em toda página para dar suporte ao destaque `#buscar=`, mesmo que o usuário nunca abra a busca ali). Não há `type="module"` nem `import`/`export` — todos os scripts são clássicos, o que impede tree-shaking nativo do navegador.

`diagnostico.js` e `legal-animations.js` não são declarados centralmente em `scripts.html` — presumivelmente incluídos apenas nas páginas que os usam (`diagnostico.html`, páginas `legal-page`), o que é uma forma manual (mas efetiva) de code-splitting por rota.

## Fontes

- Fontes globais (Cormorant Garamond, Inter) são carregadas via Google Fonts com `rel="preconnect"` para `fonts.googleapis.com` e `fonts.gstatic.com` **duplicado em dois lugares**: uma vez estaticamente no `<head>` de `index.html` (`public/index.html:30-36`) e novamente via injeção dinâmica por JavaScript no `header.html` (`public/partials/header.html:4-26`, com guarda `global-fonts-loaded` para não duplicar a segunda injeção). Isso significa que a maioria das páginas carrega a fonte **duas vezes na declaração** (uma vez estática no head da própria página, se presente, e uma vez via o script do header) — mitigado pela guarda, mas ainda resulta em dois `preconnect` idênticos por página.
- `display=swap` é usado na URL do Google Fonts (`homepage.css` link, `header.html:20`), o que evita FOIT (Flash of Invisible Text) — boa prática presente.
- Fontes editoriais (Playfair Display, Source Serif 4, DM Mono) só são carregadas nas páginas com `.assets-pillar-page`, evitando o custo em páginas que não precisam (`tokens.css:96-102`).

## Imagens

O inventário de imagens é extremamente enxuto: `public/assets/images/` contém apenas 3 SVGs (bandeiras) e `public/assets/illustrations/` contém 2 SVGs + 1 PNG (favicon duplicado em SVG e PNG) + 1 SVG adicional. **Não há imagens fotográficas ou rasterizadas de conteúdo no repositório** (sem `.jpg`, `.webp`, `.avif` versionados). Isso tem duas leituras:
- Positiva: o site é leve em payload de imagem, e SVG escala sem perda em qualquer densidade de tela.
- Negativa: o `og-image.jpg` referenciado em todo `<meta property="og:image">` (ver [07-seo.md](07-seo.md)) não existe no repositório — se também não existir em produção, todo compartilhamento social perde a imagem de preview.

Não há uso de `loading="lazy"` em nenhuma página (busca por esse atributo em todo `public/**/*.html` retornou zero ocorrências) nem de `<picture>`/`srcset` para arte direcionada — não identificado no projeto. Dado o baixíssimo volume de imagens atual, o impacto prático é pequeno hoje, mas a ausência do padrão significa que qualquer imagem pesada adicionada futuramente não terá lazy loading por padrão.

## Cache e cache-busting

Não há headers de cache HTTP configuráveis no repositório (Nginx não versionado — necessita validação). O cache-busting de assets é feito manualmente via query string de versão, com convenções inconsistentes entre arquivos:
- `main.css?v=7`, `styles-header-final.css?v=7`, `homepage.css?v=6` (números de versão simples incrementais)
- `i18n.js?v=2026041001`, `search.js?v=2026072201`, `mobile-menu.js?v=2026022601` (datas no formato `AAAAMMDDNN`)
- `search-index.json?v=2`, `lang/{lang}.json?v=10` (contadores simples)

Três esquemas de versionamento diferentes convivem no mesmo projeto — não há um único ponto de verdade para "versão do build" (porque não há build). Cada alteração de arquivo exige lembrar manualmente de incrementar a query string correspondente em todo `<link>`/`<script>` que a referencia, sob risco de o navegador servir uma versão em cache do arquivo antigo.

## Scripts de terceiros

| Script | Carregamento | Impacto |
| --- | --- | --- |
| Google Tag Manager / gtag.js | `<script async>` no `<head>` | Não bloqueia o parsing (async), mas roda em toda página, incluindo páginas legais e o diagnóstico |
| Google reCAPTCHA v2 | Injetado dinamicamente por `diagnostico.js:196-210` apenas na página `/diagnostico/`, recarregado a cada troca de idioma (remove o `<script>` antigo e cria um novo com `hl` correspondente) | Isolado à página que precisa; troca de idioma reprocessa o widget completo |
| Google Fonts | `<link rel="stylesheet">` render-blocking (mitigado por `display=swap` e `preconnect`) | Ver seção Fontes acima |

## Lazy loading e code splitting

| Técnica | Presente? | Evidência |
| --- | --- | --- |
| `loading="lazy"` em imagens | Não | Busca no projeto: 0 ocorrências |
| `<picture>`/`srcset` | Não | Não identificado no projeto |
| Dynamic `import()` de JS | Não | Todos os scripts são `<script>` clássicos com `defer` |
| CSS/JS por rota (code splitting manual) | Parcial | `diagnostico.css`/`.js` e `legal-*.css`/`.js` só carregam nas páginas correspondentes; os 4 scripts "core" carregam sempre |
| Prefetch/preload de rota seguinte | Não | Não identificado no projeto (não há `<link rel="prefetch">` nem `rel="preload"` de documentos) |
| Preconnect para origens externas | Sim | `fonts.googleapis.com`, `fonts.gstatic.com` |

## Rede e requisições client-side em runtime

Fluxo de requisições JS disparadas após o carregamento inicial da página (visto em `i18n.js`, `search.js`):
1. `GET /assets/config/i18n-config.json` — sempre, no `DOMContentLoaded`.
2. `GET /assets/lang/{lang}.json?v=10` — sempre (mesmo para PT, que é o idioma default do HTML — não há otimização de "pular fetch se já é PT e o HTML já está em PT"; isso é uma oportunidade de performance não implementada, pois o texto PT do HTML é substituído pelo mesmo texto vindo do JSON).
3. `GET /assets/search-index.json?v=2` — sob demanda, apenas quando o usuário abre o painel de busca.

## Documentos relacionados
- [02-stack.md](02-stack.md) — ausência de bundler/build.
- [12-technical-debt.md](12-technical-debt.md) — priorização dos achados de performance.
