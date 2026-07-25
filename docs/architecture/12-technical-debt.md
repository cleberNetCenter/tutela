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
11 páginas com metadata social (ex. `public/index.html:22,28`, `public/diagnostico.html:21,27`) apontam para `https://tuteladigital.com.br/assets/images/og-image.jpg`. O diretório `public/assets/images/` contém apenas 3 SVGs de bandeiras — nenhum `.jpg` existe em lugar nenhum do repositório versionado.
**Cenário de falha concreto**: qualquer pessoa que compartilhe qualquer página do site no WhatsApp, LinkedIn ou X verá um preview sem imagem (ou imagem quebrada). Confirmado via auditoria externa (ARQ-108, Sprint 5): `404` em produção e homologação — não existe em nenhum ambiente. Ver [07-seo.md](07-seo.md).

**Atualização (Sprint 18, ARQ-201)**: investigação não encontrou nenhum candidato ao asset em lugar algum acessível a partir do repositório (histórico completo, branches remotas, diretórios não versionados) — o bloqueio é real e puramente de entrega de arte, sem complexidade técnica oculta. A investigação encontrou, porém, um problema técnico adjacente não documentado até aqui: 3 páginas (`public/ativos-digitais/prova-digital-judicial/index.html`, `public/ativos-digitais/heranca-digital/index.html`, `public/prova-digital-validade-juridica/index.html`) referenciavam `https://tuteladigital.com.br/assets/img/og-default.jpg` — diretório `assets/img/` (sem "s") que **nunca existiu** no repositório em nenhum commit desde a criação dessas páginas (confirmado via `git log --all --diff-filter=A`). Corrigido nesta sprint: consolidado para `assets/images/og-image.jpg`, mesmo destino das demais 11 páginas. Uma quarta página, `public/ativos-digitais/index.html`, tinha o mesmo problema de diretório mas com nome de arquivo distinto (`og-ativos-digitais.jpg`) — corrigido o diretório (`assets/images/`), mantido o nome, já que pode representar uma decisão de conteúdo (imagem social dedicada ao cluster de Ativos Digitais) e não um typo. Esse segundo asset (`og-ativos-digitais.jpg`) também não existe em nenhum ambiente e fica registrado como pendência adjacente, fora do escopo formal de ARQ-201.

Guard-test executável criado: `tests/og-image.spec.ts` — roda como `fixme` (visível no relatório, não quebra `npm test`) enquanto os arquivos não existirem, e passa a validar de verdade assim que forem adicionados. Inclui também um teste de regressão (roda hoje, sempre) que garante que nenhuma página volte a referenciar o diretório inexistente `assets/img/`.

Especificações técnicas confirmadas para `og-image.jpg` (e por extensão `og-ativos-digitais.jpg`, se produzido): **1200×630px**, formato **JPEG**, peso recomendado **< 300KB** (não há teto formal do protocolo Open Graph, mas é o limite prático usado pelos principais crawlers/apps de mensagem para carregar o preview rapidamente). Não há nota de marca específica para o conteúdo da imagem em `06-design-system.md` além da paleta geral (verde institucional escuro dominante, acento dourado editorial, vermelho reservado a risco) — o conteúdo/composição da imagem em si é uma decisão de design ainda não tomada, não apenas produção técnica de um arquivo.

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

### 10. ~~Ausência de escala de breakpoints tokenizada~~ — RESOLVIDO (Sprint 12, 2026-07-24, ARQ-302)
13 valores de `max-width` distintos (480px a 1200px) eram usados como números mágicos em `@media` queries espalhadas por múltiplos arquivos CSS, sem token compartilhado (`--breakpoint-*`). Formatação também era inconsistente (`max-width:768px` sem espaço convivia com `max-width: 768px` com espaço no mesmo arquivo `layout/layout.css:24,30`).
**Confirmação**: CSS não permite `var()` dentro da condição de `@media` (limitação de especificação, não de suporte de navegador), e o projeto não usa pré-processador nem build step (`02-stack.md`) — não há forma de tokenizar a query em si sem mudar a arquitetura de build. Os 13 valores reais (13º valor, `1180px`, descoberto num 17º arquivo não listado originalmente: `partials/ativos-digitais-pillar-styles.html`) foram declarados como tokens `--breakpoint-*` em `foundation/tokens.css` (utilizáveis via `var()` fora de `@media`), e `tests/breakpoint-tokens.spec.ts` passou a validar automaticamente que nenhum `@media (max-width: ...)` do repositório usa um valor fora dessa lista, e que a formatação é consistente. As 3 ocorrências com formatação divergente foram corrigidas. Ver [16-architecture-backlog.md](16-architecture-backlog.md#arq-302--tokenizar-breakpoints---breakpoint-) para a decisão técnica completa e evidência.

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

### 15. ~~`vercel.json` presente sem confirmação de uso no pipeline real~~ — RESOLVIDO (Sprint 6, 2026-07-24, ARQ-403)
`public/vercel.json` e `public/_redirects` declaravam redirects em sintaxes de plataformas (Vercel/Netlify) não usadas no pipeline real, que roda exclusivamente em runners self-hosted + Docker + Nginx.
**Confirmação**: a auditoria ARQ-108 (Sprint 5) confirmou via `nginx -T` na fonte, em produção e homologação, que nenhum dos dois Nginx lê esses arquivos — a normalização de URL é feita por uma regra genérica do Nginx, independente deles (ver `docs/ambientes-e-deploy.md`, seção "Auditoria externa (ARQ-108)"). Grep em todo o repositório (incluindo `.github/workflows/`) não encontrou nenhuma outra referência funcional a esses arquivos. Ambos foram removidos na Sprint 6; `npm test` permaneceu 7/7 após a remoção.

### 16. Ausência de banner de consentimento de cookies
Google Analytics 4 está presente em todas as páginas sem um mecanismo visível de consentimento prévio (cookie banner/CMP). Ver [09-security.md](09-security.md).
**Cenário de falha concreto**: potencial não-conformidade com LGPD/GDPR quanto a cookies de analytics de terceiros — validação jurídica recomendada, fora do escopo técnico desta análise.

## Itens que necessitam validação (fora do repositório)

Auditoria em três etapas (ARQ-108, 2026-07-24 — ver [docs/ambientes-e-deploy.md](../ambientes-e-deploy.md#nginx) para evidência completa): `curl` externo, depois `nginx -T` no host de produção, depois investigação de `docker ps`/`ss -ltnp` + `nginx -T` dentro do container em homologação (necessária porque o `nginx -T` do host de homologação inicialmente não batia com o `curl` — o Nginx real ali roda dentro do container `tutela_v2_nginx`, publicado direto nas portas 80/443; o `/etc/nginx` do host está morto). Juntas, **resolveram os 6 itens originais** e revelaram fatos novos não previstos nesta lista. Itens resolvidos, mantidos aqui só para rastreabilidade:

- ~~Headers HTTP reais (CSP, HSTS, X-Frame-Options) em produção~~ — **resolvido, confirmado na config-fonte via `nginx -T`** em produção (host) e homologação (container): HSTS/X-Frame-Options/X-Content-Type-Options/Referrer-Policy ativos em produção; CSP e Permissions-Policy **ausentes** em ambos; HSTS **ausente** em homologação.
- ~~Se `og-image.jpg` existe apenas no servidor de produção~~ — **resolvido**: confirmado `404` em produção e homologação; o arquivo não existe em nenhum ambiente.
- ~~Se o Nginx aplica os redirects de `_redirects`/`vercel.json`~~ — **resolvido, causa raiz confirmada no arquivo de configuração, nos dois ambientes**: não aplica. Tanto produção quanto homologação têm uma regra genérica (`location ~ ^/(?!partials/)(.*)\.html$ { return 301 ...; }`) que intercepta qualquer `.html` antes de qualquer lógica de `_redirects`/`vercel.json` — esses dois arquivos nunca são lidos por nenhum dos dois Nginx. As 5 URLs legadas resultam em `404` hoje em ambos os ambientes.
- ~~URL do ambiente de homologação~~ — **resolvido**: `homolog.tuteladigital.com.br` (CNAME para `dev.tuteladigital.com.br`).
- ~~Arquivo Nginx ativo / upstream / SSI~~ — **resolvido nos dois ambientes**: produção usa `/etc/nginx/sites-enabled/tutela.conf` no host (`proxy_pass http://localhost:8080`); homologação usa a config dentro do container `tutela_v2_nginx`, publicado direto em 80/443 — arquiteturas diferentes entre os dois ambientes, ver `ambientes-e-deploy.md`. `ssi on` confirmado nos dois.
- ~~Se `docker-compose.yml` em produção e homologação estão em paridade~~ — **resolvido, via observação direta (`docker ps`), não apenas confirmado como pendente**: **não estão em paridade**. Produção roda `tutela_v2_nginx` + `tutela_v2_api`; homologação roda só `tutela_v2_nginx` — o container de API não aparece ativo em homologação.

Itens que continuam pendentes de acesso direto ao servidor/rede:

| Item | Por que não pode ser confirmado só pelo código |
| --- | --- |
| Comportamento real de `/api/diagnostico` | Endpoint não versionado neste repositório. Achado incidental desta auditoria: existe um container `tutela_v2_api` rodando em produção (porta 3000, interna) que pode ser a implementação — não investigado, fora do escopo de ARQ-108; pista para ARQ-101. |
| Renovação automática de certificado (produção e homologação) | Requer `certbot certificates` ou equivalente em cada servidor, não rodado nesta auditoria |
| Correção do redirect para porta `:445` em `http://tuteladigital.com.br/` (porta 80) | **Confirmado que não vem de nenhum dos dois Nginx** (nem o de produção nem o de homologação fazem esse redirect ou adicionam esses headers) — origem é o firewall Fortinet que faz o acesso externo aos servidores. Causa provável **informada pelo usuário, não verificada diretamente**: a porta de administração web do Fortinet foi remapeada de 443 para 445 (para não conflitar com o tráfego HTTPS real dos sites que ele atende), e a regra de redirect HTTP→HTTPS de `tuteladigital.com.br` provavelmente herda essa porta administrativa em vez da porta 443 do site — erro de configuração conhecido em FortiGate. Correção requer acesso ao Fortinet, fora do escopo deste repositório. |

## Documentos relacionados
- Cada achado linka de volta ao documento temático correspondente para contexto completo.
- [EXECUTIVE_SUMMARY.md](EXECUTIVE_SUMMARY.md) — leitura executiva priorizada destes achados.
- [16-architecture-backlog.md](16-architecture-backlog.md) — os 16 itens acima foram convertidos em itens `ARQ-xxx` rastreáveis, com critérios de aceite, risco e responsável.
