# 03 — Estrutura de Diretórios e Inventário

## Índice
- [Árvore de diretórios](#árvore-de-diretórios)
- [Raiz do repositório](#raiz-do-repositório)
- [public/ — conteúdo servido](#public--conteúdo-servido)
- [public/assets/ — detalhado](#publicassets--detalhado)
- [Inventário de páginas HTML](#inventário-de-páginas-html)
- [Configuração de projeto encontrada vs. ausente](#configuração-de-projeto-encontrada-vs-ausente)

## Árvore de diretórios

```text
tutela/
├── .github/
│   ├── ci/
│   │   └── build_search_index.py         # gera assets/search-index.json
│   └── workflows/
│       ├── deploy-homolog.yml
│       ├── deploy-prod.yml
│       ├── guard-main-requires-homolog.yml
│       └── sitemap.yml
├── docs/
│   ├── ambientes-e-deploy.md              # runbook de deploy/infra (pré-existente)
│   └── architecture/                      # esta documentação
├── public/                                # ⭐ raiz do site servido
│   ├── _redirects                         # redirects estilo Netlify (não confirmado em uso)
│   ├── vercel.json                        # redirects estilo Vercel (não confirmado em uso — ver 12-technical-debt.md)
│   ├── robots.txt
│   ├── sitemap.xml                        # gerado automaticamente por CI
│   ├── index.html                         # home (PT-BR)
│   ├── como-funciona.html
│   ├── diagnostico.html                   # ferramenta interativa
│   ├── seguranca.html
│   ├── governo.html / empresas.html / pessoas.html   # páginas por vertical
│   ├── ativos-digitais/                   # pillar page jurídica (5 páginas)
│   ├── insights/                          # blog jurídico (13 artigos + 2 índices)
│   ├── legal/                             # termos, privacidade, fundamentos (7 páginas)
│   ├── en/digital-assets/                 # página física em inglês
│   ├── es/activos-digitales/              # página física em espanhol
│   ├── pt/ativos-digitais/                # página física em português (par do en/es)
│   ├── prova-digital-validade-juridica/   # página standalone
│   ├── partials/                          # includes SSI (header, footer, scripts)
│   ├── docs/                              # markdown editorial/prompts (não é o app)
│   └── assets/
│       ├── config/i18n-config.json
│       ├── css/                           # ~36 arquivos, ver detalhado abaixo
│       ├── js/                            # 7 scripts vanilla
│       ├── lang/{pt,en,es}.json           # traduções
│       ├── images/flags/{br,us,es}.svg
│       ├── illustrations/                 # favicon, ilustrações SVG/PNG
│       └── search-index.json              # gerado automaticamente por CI
├── public_backup/                         # backup local, ignorado pelo Git (.gitignore)
├── test-results/                          # artefato do Playwright, não rastreado
├── package.json / package-lock.json       # não rastreados pelo Git
└── .gitignore
```

## Raiz do repositório

| Item | Tipo | Rastreado pelo Git? | Observação |
| --- | --- | --- | --- |
| `public/` | diretório | Sim | Raiz do site estático |
| `docs/` | diretório | Sim | Documentação (runbook + esta pasta) |
| `.github/` | diretório | Sim | Workflows de CI/CD |
| `public_backup/` | diretório | Não (`.gitignore:6`) | Vazio no momento da análise |
| `package.json`, `package-lock.json` | arquivo | Não (`git status` mostra `??`) | Único conteúdo: devDependency `@playwright/test` |
| `test-results/` | diretório | Não | Artefato de execução do Playwright (`.last-run.json` com `"status": "failed"`) |
| `.claude/` | diretório | Não | Configuração local do assistente Claude Code, fora do escopo desta documentação de produto |
| `.gitignore` | arquivo | Sim | Ignora `node_modules/`, backups, `.vscode/`, `.codex`, arquivos de análise avulsos |

## public/ — conteúdo servido

`public/` é a raiz efetiva do site (documentado em `docs/ambientes-e-deploy.md:20`). Contém:

| Subpasta/arquivo | Conteúdo | Nº de páginas HTML |
| --- | --- | --- |
| raiz de `public/` | Páginas institucionais principais + config (`robots.txt`, `sitemap.xml`, `_redirects`, `vercel.json`) | 7 (`index`, `como-funciona`, `diagnostico`, `seguranca`, `governo`, `empresas`, `pessoas`) |
| `ativos-digitais/` | Pillar page jurídica com 4 subpáginas temáticas | 5 |
| `insights/` | Blog jurídico com 2 categorias (`ativos-digitais`, `prova-digital`) | 15 (2 índices + 13 artigos, incluindo 1 stub de redirecionamento) |
| `legal/` | Termos de uso, privacidade, custódia, fundamentos jurídicos | 7 |
| `en/`, `es/`, `pt/` | Páginas físicas traduzidas do pillar de ativos digitais | 3 |
| `prova-digital-validade-juridica/` | Página standalone (não linkada no menu principal — necessita validação sobre seu propósito atual) | 1 |
| `partials/` | Includes SSI + partials específicos do pillar de ativos digitais | 6 arquivos (não são rotas) |
| `docs/` (dentro de `public/`) | Markdown de prompts/editorial para produção de conteúdo (cluster de artigos) | não é HTML servido como página |

Total: **35 páginas HTML roteáveis** rastreadas pelo Git (excluindo `partials/`), confirmado via `git ls-files public | grep '\.html$'`.

## public/assets/ — detalhado

| Subpasta | Conteúdo | Volume |
| --- | --- | --- |
| `css/` | Estilos modulares (foundation, layout, components, sections, pages, utilities) | 36 arquivos, ~12.500 linhas totais |
| `js/` | Scripts vanilla | 7 arquivos, ~1.080 linhas totais |
| `lang/` | Traduções JSON | 3 arquivos (`pt.json` 829 linhas, `en.json`/`es.json` 784 linhas cada) |
| `config/` | Configuração do sistema de i18n | 1 arquivo (`i18n-config.json`) |
| `images/flags/` | Bandeiras do seletor de idioma | 3 SVGs |
| `illustrations/` | Favicon e ilustrações decorativas | 4 arquivos (2 SVG, 1 PNG, e o favicon SVG duplicado como PNG) |
| `search-index.json` | Índice de busca gerado por CI | 1 arquivo, gerado, não editado manualmente |

Tabela de scripts JS (ver detalhes funcionais em [05-components.md](05-components.md)):

| Arquivo | Linhas | Papel |
| --- | --- | --- |
| `search.js` | 279 | Widget de busca client-side (índice JSON + destaque de trecho) |
| `i18n.js` | 260 | Motor de internacionalização |
| `mobile-menu.js` | 118 | Controlador real de navegação (dropdowns desktop + menu mobile) — apesar do nome |
| `diagnostico.js` | 362 | Lógica do questionário de diagnóstico de risco |
| `legal-animations.js` | 38 | Animações de entrada (scroll reveal) nas páginas `legal-page` |
| `dropdown-menu.js` | 13 | Script "ponte", apenas emite aviso no console — lógica real está em `mobile-menu.js` |
| `navigation.js` | 7 | Desativado intencionalmente (`NAVIGATION DISABLED (MPA MODE)`) |

Não há build/minificação: os números de linha acima refletem o código-fonte tal como servido em produção.

## Inventário de páginas HTML

A lista completa e roteável (com URLs finais) está em [04-routing.md](04-routing.md#tabela-completa-de-rotas), gerada a partir do próprio `public/sitemap.xml` (37 entradas) e da árvore de arquivos.

## Configuração de projeto encontrada vs. ausente

| Configuração | Status |
| --- | --- |
| `package.json` | Presente, mas não rastreado pelo Git e sem uso de build (única dependência: Playwright) |
| `tsconfig.json` | Não identificado no projeto |
| `next.config.js` | Não identificado no projeto |
| `.eslintrc*` / `eslint.config.*` | Não identificado no projeto |
| `.prettierrc*` | Não identificado no projeto |
| `tailwind.config.js` | Não identificado no projeto |
| `postcss.config.js` | Não identificado no projeto |
| `docker-compose.yml` | Não identificado no projeto — vive em `/opt/tutela-v2` no servidor (`docs/ambientes-e-deploy.md:20`) |
| `Dockerfile` | Não identificado no repositório |
| `.github/workflows/*.yml` | Presente — 4 workflows (deploy homolog, deploy produção, guard de branch, sitemap) |
| `vercel.json` | Presente em `public/vercel.json`, mas não confirmado como parte do pipeline de deploy ativo |
| `.env` / `.env.*` | Não identificado no projeto — nenhuma variável de ambiente ou segredo versionado |
| `playwright.config.*` | Não identificado no projeto (apesar da dependência estar instalada localmente) |

## Documentos relacionados
- [02-stack.md](02-stack.md) — tecnologias por trás de cada pasta.
- [04-routing.md](04-routing.md) — mapeamento arquivo → URL.
- [12-technical-debt.md](12-technical-debt.md) — itens de configuração órfã ou inconsistente.
