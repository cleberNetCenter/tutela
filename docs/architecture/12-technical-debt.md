# 12 — Dívida Técnica

## Índice
- [Metodologia](#metodologia)
- [Alta severidade](#alta-severidade)
- [Média severidade](#média-severidade)
- [Baixa severidade](#baixa-severidade)
- [Itens que necessitam validação (fora do repositório)](#itens-que-necessitam-validação-fora-do-repositório)

## Metodologia

Todos os itens abaixo são **fatos observáveis diretamente no código-fonte do repositório**, sem correção aplicada nesta análise. Severidade é uma estimativa de impacto sobre usuários finais, SEO, segurança ou manutenibilidade — não uma medida de esforço de correção. "Alta" = afeta todos ou quase todos os usuários/páginas, ou envolve dado pessoal/segurança. "Média" = afeta um subconjunto relevante de páginas ou degrada qualidade sem quebrar funcionalidade. "Baixa" = cosmético, redundante, ou impacto marginal.

## Alta severidade

### 1. Imagem de Open Graph (`og-image.jpg`) referenciada mas ausente do repositório
Todas as páginas com metadata social (ex. `public/index.html:22,28`, `public/diagnostico.html:19,24`) apontam para `https://tuteladigital.com.br/assets/images/og-image.jpg`. O diretório `public/assets/images/` contém apenas 3 SVGs de bandeiras — nenhum `.jpg` existe em lugar nenhum do repositório versionado.
**Cenário de falha concreto**: qualquer pessoa que compartilhe qualquer página do site no WhatsApp, LinkedIn ou X verá um preview sem imagem (ou imagem quebrada), a menos que o arquivo exista apenas em produção fora do controle de versão — o que por si só seria um risco (arquivo de produção não reproduzível a partir do Git). Ver [07-seo.md](07-seo.md).

### 2. `/api/diagnostico` sem implementação auditável no repositório
`public/assets/js/diagnostico.js:294` envia nome, e-mail e respostas do questionário via `POST /api/diagnostico`. Não há função serverless, rota estática ou proxy documentado no repositório que implemente esse endpoint.
**Cenário de falha concreto**: não é possível, a partir deste repositório, auditar se os dados pessoais coletados são validados, sanitizados ou armazenados de forma compatível com a LGPD — relevante porque a própria empresa comercializa conformidade regulatória como parte de sua proposta de valor. Ver [09-security.md](09-security.md).

### 3. Ausência de headers de segurança versionados (CSP, HSTS, X-Frame-Options)
Nenhum header de segurança é definido pela aplicação (não há meta CSP, não há `vercel.json` com seção `headers`). A configuração real depende do Nginx do servidor, não versionado.
**Cenário de falha concreto**: se o Nginx de produção também não define esses headers (necessita validação), o site fica sem proteção declarada contra clickjacking (falta de `X-Frame-Options`/`frame-ancestors`) e sem mitigação de XSS em profundidade via CSP. Ver [09-security.md](09-security.md).

## Média severidade

### 4. Scripts de navegação com nomenclatura que não reflete a responsabilidade real
`public/assets/js/mobile-menu.js` controla tanto o menu mobile quanto os dropdowns de desktop (hover, clique, `aria-expanded`) — apesar do nome sugerir escopo apenas mobile. `public/assets/js/dropdown-menu.js`, cujo nome sugeriria a lógica de dropdown, hoje só emite um `console.warn` caso o outro script não tenha rodado antes (`dropdown-menu.js:1-13`).
**Cenário de falha concreto**: um desenvolvedor futuro que precise alterar o comportamento de dropdown vai procurar em `dropdown-menu.js` primeiro, não encontrará a lógica, e pode duplicá-la por engano ou editar o arquivo errado.

### 5. Cluster de hreflang sem reciprocidade completa
As páginas `/pt/ativos-digitais/`, `/en/digital-assets/` e `/es/activos-digitales/` declaram um bloco `hreflang` completo (incluindo `x-default` apontando para `/ativos-digitais/`), mas a própria página `/ativos-digitais/index.html` **não declara nenhum `hreflang`** de volta.
**Cenário de falha concreto**: buscadores podem não reconhecer o cluster como totalmente recíproco, reduzindo a eficácia da segmentação de idioma nos resultados de busca internacionais. Ver [04-routing.md](04-routing.md) e [07-seo.md](07-seo.md).

### 6. Três sistemas de design tokens paralelos para o mesmo cluster de páginas
`foundation/tokens.css` define tokens globais (`--color-*`) e uma extensão `--ad-*` para Ativos Digitais. Um `<style>` inline em `public/partials/ativos-digitais-pillar-styles.html` define um terceiro conjunto, `--ux-*`, com valores de marca próximos mas não idênticos aos de `--ad-*` (ex.: `--ux-brand: #0f4a36` vs. `--ad-brand-dark: #0d2b1a`).
**Cenário de falha concreto**: um ajuste de cor de marca feito em `tokens.css` (`--ad-*`) não se propaga para elementos estilizados com `--ux-*`, produzindo inconsistência visual sutil entre seções da mesma página. Ver [06-design-system.md](06-design-system.md).

### 7. Sincronização automática de sitemap na direção main → homolog
`.github/workflows/sitemap.yml` faz merge de `main` em `homolog` automaticamente a cada push em `main`, o oposto do fluxo de validação que o próprio time documenta como prática recomendada (validar em homolog antes de promover a main). O próprio runbook já registra isso como pendência: *"Essa regra deve ser revisada pela equipe, pois o fluxo usual de validação é homologação antes de produção."* (`docs/ambientes-e-deploy.md:99`).
**Cenário de falha concreto**: uma mudança feita diretamente contra `main` (fora do fluxo de PR guardado) sincroniza para `homolog` e, via `workflow_dispatch`, força um redeploy de homolog com conteúdo de produção — misturando o que deveria ser um ambiente de validação prévia com o estado já publicado.

### 8. Ausência de skip-link / bypass block de acessibilidade
Nenhuma página do site analisada contém um link "pular para o conteúdo" (`<a href="#main-content">` ou padrão equivalente) — busca por `skip-link`/`#main-content` em todo `public/**/*.html` não retornou resultados.
**Cenário de falha concreto**: um usuário de teclado ou leitor de tela precisa tabular por todos os itens de navegação (logo, 8+ links/dropdowns, seletor de idioma, busca, CTA) em toda página antes de alcançar o conteúdo principal — relevante para WCAG 2.4.1 (Bypass Blocks).

## Baixa severidade

### 9. Arquivos CSS "descontinuados" ainda referenciados por `<link>` em produção
Seis arquivos CSS foram esvaziados e reduzidos a um comentário de descontinuação (`dropdown-menu.css`, `pages/ativos-digitais-pillar-styles.css`, `pages/fundamento-juridico.css`, `pages/politica-de-privacidade.css`, `pages/preservacao-probatoria-digital.css`, `pages/termos-de-custodia.css`), mas continuam sendo referenciados via `<link rel="stylesheet">` em 20+ páginas (ex. `public/legal/termos-de-uso.html`, `public/legal/institucional.html`, todas as páginas do cluster `/ativos-digitais/`).
**Cenário de falha concreto**: cada carregamento de página soma requisições HTTP que não entregam nenhum estilo — impacto real pequeno (arquivos triviais), mas puro desperdício de uma conexão/roundtrip por página. Ver [08-performance.md](08-performance.md).

### 10. Ausência de escala de breakpoints tokenizada
13 valores de `max-width` distintos (480px a 1200px) são usados como números mágicos em `@media` queries espalhadas por múltiplos arquivos CSS, sem token compartilhado (`--breakpoint-*`). Formatação também é inconsistente (`max-width:768px` sem espaço convive com `max-width: 768px` com espaço no mesmo arquivo `layout/layout.css:24,30`).
**Cenário de falha concreto**: um redesenho de grid responsivo exige caçar manualmente cada valor em vez de alterar um único token — risco de esquecer um breakpoint e deixar uma página com comportamento inconsistente das demais. Ver [06-design-system.md](06-design-system.md).

### 11. `package.json`/Playwright instalado sem uso
Há um `package.json` com `@playwright/test` como devDependency, `package-lock.json` e uma pasta `test-results/` (com `.last-run.json` indicando `"status": "failed"`), mas nenhum destes está rastreado pelo Git, não existe `playwright.config.*` nem qualquer arquivo `*.spec.*`/`*.test.*` no repositório.
**Cenário de falha concreto**: nenhum, hoje — mas indica uma tentativa de configurar testes E2E que não chegou a ser commitada nem finalizada, e pode gerar confusão sobre se "existem testes" no projeto (não existem, apesar da dependência estar presente no diretório de trabalho).

### 12. Três esquemas de cache-busting diferentes convivendo
Query strings de versão usam três convenções distintas: contador simples (`main.css?v=7`), data no formato `AAAAMMDDNN` (`i18n.js?v=2026041001`) e contador simples separado por arquivo (`search-index.json?v=2`, `lang/pt.json?v=10`).
**Cenário de falha concreto**: sem uma convenção única, é fácil esquecer de incrementar a query string certa ao editar um arquivo, fazendo o navegador do usuário servir uma versão em cache desatualizada daquele arquivo específico. Ver [08-performance.md](08-performance.md).

### 13. Configuração `i18n-config.json` com referência a IDs de DOM vestigiais
`public/assets/config/i18n-config.json` lista `legalPages` como uma lista de IDs (`page-institucional`, `page-politica-de-privacidade`, etc.), e `i18n.js:74-79` tenta `document.getElementById(pageId)` para detectar páginas legais. Nenhuma página atual usa esses valores como `id` — o padrão atual usa a classe `legal-page` no `<body>` (ex. `public/legal/termos-de-uso.html:195`, `class="exec-compact legal-page page page-termos-de-uso"` — aqui `page-termos-de-uso` é uma *classe*, não um `id`). A função `isLegalPage()` funciona corretamente hoje só porque tem um fallback anterior que checa `body.classList.contains('legal-page')` (`i18n.js:75`) — o array de IDs em `i18n-config.json` é, na prática, código morto, vestígio da arquitetura SPA anterior à migração para MPA (mesma migração que deixou `navigation.js` desativado, ver item a seguir).
**Cenário de falha concreto**: nenhum hoje (o fallback cobre o caso), mas gera confusão para quem lê `i18n-config.json` e presume que aquela lista de IDs é ativa.

### 14. `navigation.js` mantido apenas como script morto
`public/assets/js/navigation.js` contém unicamente um IIFE com `return` imediato e o comentário `NAVIGATION DISABLED (MPA MODE)`. Não está claro, a partir do repositório, se o arquivo ainda é referenciado por alguma página (não aparece em `scripts.html`) — necessita validação se algum HTML legado ainda o inclui.
**Cenário de falha concreto**: nenhum funcional; é peso morto no repositório que pode confundir sobre o que está realmente ativo.

### 15. `vercel.json` presente sem confirmação de uso no pipeline real
`public/vercel.json` declara redirects no formato Vercel, mas o pipeline de deploy documentado (`docs/ambientes-e-deploy.md`, workflows de `.github/`) usa exclusivamente runners self-hosted + Docker + Nginx — nenhuma menção à Vercel.
**Cenário de falha concreto**: um desenvolvedor pode presumir que editar `vercel.json` altera o comportamento de produção, quando na realidade (necessita validação) esse arquivo pode não ter efeito algum no ambiente real.

### 16. Ausência de banner de consentimento de cookies
Google Analytics 4 está presente em todas as páginas sem um mecanismo visível de consentimento prévio (cookie banner/CMP). Ver [09-security.md](09-security.md).
**Cenário de falha concreto**: potencial não-conformidade com LGPD/GDPR quanto a cookies de analytics de terceiros — validação jurídica recomendada, fora do escopo técnico desta análise.

## Itens que necessitam validação (fora do repositório)

| Item | Por que não pode ser confirmado só pelo código |
| --- | --- |
| Headers HTTP reais (CSP, HSTS, X-Frame-Options) em produção | Configuração do Nginx não é versionada (`docs/ambientes-e-deploy.md:116-118`) |
| Se `og-image.jpg` existe apenas no servidor de produção | Repositório é a única fonte disponível para esta análise |
| Comportamento real de `/api/diagnostico` | Endpoint não versionado neste repositório |
| Se o Nginx aplica os redirects de `_redirects`/`vercel.json` | Depende da config real do servidor |
| URL do ambiente de homologação | Não versionada; deve ser obtida do DNS/Nginx do servidor |
| Se `docker-compose.yml` em produção e homologação estão em paridade | Vive fora do repositório, em `/opt/tutela-v2` de cada servidor |

## Documentos relacionados
- Cada achado linka de volta ao documento temático correspondente para contexto completo.
- [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) — leitura executiva priorizada destes achados.
