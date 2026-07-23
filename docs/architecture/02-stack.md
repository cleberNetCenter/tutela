# 02 — Stack Tecnológica

## Índice
- [Resumo](#resumo)
- [Frontend](#frontend)
- [Internacionalização](#internacionalização)
- [Build e ferramentas](#build-e-ferramentas)
- [Infraestrutura e deploy](#infraestrutura-e-deploy)
- [Serviços de terceiros](#serviços-de-terceiros)
- [O que está ausente da stack](#o-que-está-ausente-da-stack)

## Resumo

| Camada | Tecnologia | Evidência |
| --- | --- | --- |
| Marcação | HTML5 estático (43 arquivos `.html`) | `public/**/*.html` |
| Estilo | CSS puro, modular, com `@import` | `public/assets/css/main.css` |
| Comportamento | JavaScript vanilla (ES6+, IIFE), sem framework | `public/assets/js/*.js` |
| Composição de página | Server Side Includes (SSI) | `<!--#include virtual="..." -->` em todas as páginas |
| Internacionalização | Sistema próprio em JS + JSON | `public/assets/js/i18n.js`, `public/assets/lang/*.json` |
| Busca interna | Índice JSON estático gerado por script Python + JS client-side | `.github/ci/build_search_index.py`, `public/assets/js/search.js` |
| Servidor web | Nginx (TLS, SSI, proxy reverso) | `docs/ambientes-e-deploy.md` |
| Empacotamento runtime | Docker Compose (definição fora do repo, em `/opt/tutela-v2`) | `docs/ambientes-e-deploy.md:20,72-73` |
| CI/CD | GitHub Actions com self-hosted runners | `.github/workflows/*.yml` |
| Geração de sitemap | Bash + Python dentro de GitHub Actions | `.github/workflows/sitemap.yml` |

## Frontend

O frontend não usa nenhum framework ou biblioteca de UI. Não há React, Vue, Angular, Svelte, jQuery, Alpine.js, htmx ou similares — confirmado por não haver nenhuma dessas dependências em `<script src>` nas páginas nem em `node_modules` versionado. Toda a interatividade (menu mobile, dropdowns, busca, i18n, formulário de diagnóstico, animações de scroll) é implementada em JavaScript vanilla, organizado como módulos IIFE (`(function () { ... })()`) carregados via `<script defer>` a partir de `public/partials/scripts.html`.

CSS é escrito à mão, sem pré-processador (não há Sass/Less/Stylus — nenhum arquivo `.scss`/`.less` no repositório) e sem pós-processador (não há `postcss.config.js` nem Tailwind — não há `tailwind.config.js`). A composição é feita via `@import` nativo do CSS em `public/assets/css/main.css` (ver [06-design-system.md](06-design-system.md)).

## Internacionalização

Sistema de i18n **próprio e client-side**, sem biblioteca (não é i18next, FormatJS, etc.):
- `public/assets/js/i18n.js` — carrega `assets/config/i18n-config.json` e `assets/lang/{lang}.json`, aplica traduções via atributos `data-i18n`, `data-i18n-aria`, `data-i18n-placeholder`, `data-i18n-alt`, `data-i18n-title`.
- Idiomas suportados: `pt` (fallback), `en`, `es` — declarados em `public/assets/config/i18n-config.json`.
- Arquivos de tradução com ~784-829 linhas cada: `public/assets/lang/pt.json`, `en.json`, `es.json`.
- Modelo **híbrido** de i18n (ver [04-routing.md](04-routing.md)): a maioria das páginas é uma única URL PT-BR com troca de idioma client-side (a URL não muda), enquanto a pillar page de Ativos Digitais tem páginas físicas traduzidas em `/en/digital-assets/` e `/es/activos-digitales/`.

## Build e ferramentas

Não há processo de build. Não existe:
- `webpack.config.js`, `vite.config.js`, `rollup.config.js`, `esbuild` — não identificado no projeto.
- Minificação/bundling de CSS ou JS — os arquivos em `public/assets/` são servidos como estão (cache-busting manual via query string, ex. `main.css?v=7`, `i18n.js?v=2026041001`).
- `tsconfig.json` — não identificado no projeto; não há TypeScript.
- `.eslintrc*` ou `eslint.config.js` — não identificado no projeto.
- `.prettierrc*` — não identificado no projeto.
- `tailwind.config.js` / `postcss.config.js` — não identificado no projeto.

O único artefato de tooling encontrado é um `package.json` na raiz com uma única dependência de desenvolvimento:

```json
{
  "devDependencies": {
    "@playwright/test": "^1.61.1"
  }
}
```

Este arquivo, `package-lock.json` e a pasta `test-results/` estão **não rastreados pelo Git** (aparecem como `??` em `git status`) e não há `playwright.config.*` nem nenhum arquivo de teste (`*.spec.*`) em lugar nenhum do repositório. Isto é tratado como dívida técnica/observação em [12-technical-debt.md](12-technical-debt.md).

## Infraestrutura e deploy

Documentado em detalhe em [11-build-deploy.md](11-build-deploy.md). Resumo:
- **Nginx** faz TLS, redirecionamentos e proxy reverso; a configuração ativa não é versionada no repositório (gerenciada diretamente nos servidores) — necessita validação.
- **Docker Compose** empacota o servidor estático; o `docker-compose.yml` efetivo vive em `/opt/tutela-v2` no servidor, fora deste repositório.
- **GitHub Actions** com runners self-hosted (`[self-hosted, homolog]` e `[self-hosted, production]`) fazem o deploy via `git reset --hard` + `docker compose up -d --build`.
- Existe um `public/vercel.json` com regras de redirect, mas o pipeline de deploy documentado (`docs/ambientes-e-deploy.md`) não menciona Vercel em nenhum momento — a Vercel parece não estar em uso no pipeline atual (ver [12-technical-debt.md](12-technical-debt.md)).

## Serviços de terceiros

| Serviço | Uso | Evidência |
| --- | --- | --- |
| Google Fonts | Cormorant Garamond, Inter (globais); Playfair Display, Source Serif 4, DM Mono (editorial, sob demanda) | `public/partials/header.html:17-20`, `public/assets/css/foundation/tokens.css:96-105` |
| Google Analytics 4 | `gtag.js`, ID `G-KXVB267PYJ`, com `linker` entre `tuteladigital.com.br` e `app.tuteladigital.com.br` | `public/index.html:46-54` |
| Google reCAPTCHA v2 | Widget no formulário de diagnóstico | `public/diagnostico.html:289`, `public/assets/js/diagnostico.js:196-219` |
| WhatsApp Business (link direto) | Botão flutuante de contato | `public/partials/footer.html:91` |
| Instagram / YouTube | Links institucionais no rodapé | `public/partials/footer.html:22-37` |
| e-Notariado (institucional, sem integração técnica no repo) | Citado como parceiro de formalização notarial | `public/index.html:191-193` |

## O que está ausente da stack

- Nenhum framework de frontend ou backend.
- Nenhum ORM, banco de dados ou camada de persistência (site inteiramente estático).
- Nenhum sistema de gerenciamento de conteúdo (CMS) — as páginas de conteúdo são HTML escrito/editado diretamente.
- Nenhuma ferramenta de observabilidade além do Google Analytics (sem Sentry, LogRocket, etc.) — não identificado no projeto.

## Documentos relacionados
- [03-folder-structure.md](03-folder-structure.md) — onde cada peça da stack vive no disco.
- [10-dependencies.md](10-dependencies.md) — lista detalhada de dependências e versões.
- [11-build-deploy.md](11-build-deploy.md) — pipeline completo de CI/CD.
