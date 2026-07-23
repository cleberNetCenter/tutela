# 16 — Backlog Arquitetural Oficial

> Status: Referência oficial para toda implementação futura.
>
> Nenhum desenvolvimento deverá começar sem estar representado neste backlog.
>
> Este documento não altera nem substitui `12-technical-debt.md` (fatos observados) nem `15-architecture-roadmap.md` (prioridades e épicos) — ele os operacionaliza em itens rastreáveis e executáveis.

## Índice
- [Convenção de identificadores](#convenção-de-identificadores)
- [Fontes utilizadas](#fontes-utilizadas)
- [Épico 1 — Segurança (ARQ-1xx)](#épico-1--segurança-arq-1xx)
- [Épico 2 — SEO (ARQ-2xx)](#épico-2--seo-arq-2xx)
- [Épico 3 — Design System (ARQ-3xx)](#épico-3--design-system-arq-3xx)
- [Épico 4 — Consolidação Arquitetural (ARQ-4xx)](#épico-4--consolidação-arquitetural-arq-4xx)
- [Épico 5 — Engenharia (ARQ-5xx)](#épico-5--engenharia-arq-5xx)
- [Épico 6 — Acessibilidade (ARQ-6xx)](#épico-6--acessibilidade-arq-6xx)
- [Épico 7 — Governança (ARQ-7xx)](#épico-7--governança-arq-7xx)
- [Marcos Arquiteturais](#marcos-arquiteturais)
- [Validação do Backlog](#validação-do-backlog)

## Convenção de identificadores

- Prefixo `ARQ-` seguido de 3 dígitos. O primeiro dígito identifica o épico do roadmap (`15-architecture-roadmap.md`): `1xx` Segurança, `2xx` SEO, `3xx` Design System, `4xx` Consolidação Arquitetural, `5xx` Engenharia, `6xx` Acessibilidade, `7xx` Governança.
- **Identificadores são permanentes.** Uma vez atribuído, um ID nunca é reatribuído a outro item — mesmo que o item original seja cancelado, o ID permanece reservado e aparece no backlog com `Status: CANCELADO`.
- Novos itens dentro de um épico usam o próximo número livre na faixa correspondente (não há preenchimento retroativo de "buracos").
- Próximo ID livre por épico neste momento: `ARQ-109`, `ARQ-204`, `ARQ-305`, `ARQ-407`, `ARQ-506`, `ARQ-605`, `ARQ-704`.

## Fontes utilizadas

`README.md`, `EXECUTIVE_SUMMARY.md`, `01-overview.md` a `14-glossary.md`, `15-architecture-roadmap.md`, e o documento de validação do roadmap produzido na etapa anterior (revisão crítica, backlog preliminar, matriz de dependências e parecer arquitetural). Onde um item deste backlog não corresponde a nenhum dos 16 itens numerados de `12-technical-debt.md`, isso é sinalizado explicitamente no campo "Item da dívida técnica".

---

## Épico 1 — Segurança (ARQ-1xx)

### ARQ-101 — Auditoria e documentação do tratamento de dados de `/api/diagnostico` (LGPD)

| Campo | Valor |
|---|---|
| Objetivo | Tornar auditável, a partir de evidência documentada, como nome/e-mail/respostas coletados no formulário de diagnóstico são validados, transmitidos e armazenados. |
| Descrição | O endpoint `/api/diagnostico` não tem implementação, proxy ou contrato documentado neste repositório. É necessário obter da equipe responsável pelo backend uma descrição auditável do fluxo (validação server-side, armazenamento, retenção, criptografia em trânsito/repouso) e registrá-la na documentação de arquitetura. |
| Origem | Débito técnico #2 |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #2 |
| Arquivos afetados | Nenhum arquivo de código deste repositório (o endpoint é externo); documentação a atualizar: `09-security.md` |
| Dependências (depende de) | Nenhuma dependência técnica interna |
| Dependências (desbloqueia) | Nenhuma diretamente; informa o escopo final de ARQ-107 |
| Pré-requisitos | Acesso à equipe/infra responsável pelo backend do endpoint (fora deste repositório) |
| Critérios de Aceite | Documento descrevendo validação server-side, armazenamento e retenção de dados publicado e revisado por jurídico e pela equipe de backend |
| Critérios de Regressão | Não aplicável (item de auditoria/documentação, não altera código) |
| Impacto | Alto — dado pessoal, LGPD, é o item #2 nos "3 riscos de maior impacto" do `EXECUTIVE_SUMMARY.md` |
| Risco | Alto |
| Complexidade | Alta (depende de coordenação entre times/sistemas fora deste repositório) |
| Estimativa | G |
| Responsável | Segurança |
| Status | BLOQUEADO |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 100% dos campos coletados (nome, e-mail, score, consentimento) com tratamento documentado e auditável |
| Observações | Item mais crítico do backlog por envolver dado pessoal em empresa cujo produto é conformidade regulatória. Bloqueio é externo ao código — não deve travar o início de outros épicos (ver Fase 4 do documento de validação do roadmap). |

### ARQ-102 — Implantar Content-Security-Policy (CSP)

| Campo | Valor |
|---|---|
| Objetivo | Mitigar XSS em profundidade declarando explicitamente as origens permitidas para scripts, estilos e conexões. |
| Descrição | Nenhum CSP é declarado hoje (nem header, nem `<meta>`). Origens externas já conhecidas: Google Fonts, Google Tag Manager/Analytics, Google reCAPTCHA. Definir política (preferencialmente via header Nginx; alternativa: `<meta http-equiv>` por página) que libere só essas origens. |
| Origem | Débito técnico #3 |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #3 |
| Arquivos afetados | Configuração Nginx (fora do repositório) e/ou `<head>` das 37 páginas HTML, caso a alternativa `<meta>` seja escolhida |
| Dependências (depende de) | Nenhuma (inventário de origens externas já levantado em `09-security.md`) |
| Dependências (desbloqueia) | Nenhuma diretamente; coordenar com ARQ-107 (banner de cookies também carrega/bloqueia scripts) |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Header `Content-Security-Policy` presente em 100% das respostas; GA, GTM, reCAPTCHA e Google Fonts funcionando sem violação de política |
| Critérios de Regressão | Nenhum erro de bloqueio de recurso no console em nenhuma das 37 páginas após ativação |
| Impacto | Alto |
| Risco | Médio-Alto (política mal configurada pode quebrar analytics/formulário/fontes) |
| Complexidade | Média |
| Estimativa | M-G |
| Responsável | Segurança |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 violações de CSP reportadas no console em auditoria manual das 37 páginas |
| Observações | Recomenda-se modo `Content-Security-Policy-Report-Only` antes de aplicar em modo bloqueante. |

### ARQ-103 — Implantar HSTS (Strict-Transport-Security)

| Campo | Valor |
|---|---|
| Objetivo | Forçar HTTPS em todas as conexões subsequentes do navegador, mitigando downgrade attacks. |
| Descrição | Nenhum header HSTS é declarado. Requer configuração no Nginx de produção (não versionado neste repositório). |
| Origem | Débito técnico #3 |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #3 |
| Arquivos afetados | Configuração Nginx (fora do repositório) |
| Dependências (depende de) | Confirmação de que HTTPS está 100% funcional em todos os subdomínios antes de ativar `max-age` alto |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Acesso à configuração Nginx de produção |
| Critérios de Aceite | Header `Strict-Transport-Security` presente com `max-age` inicial conservador, escalonado progressivamente |
| Critérios de Regressão | Nenhum subdomínio ou ambiente fica inacessível por forçar HTTPS prematuramente |
| Impacto | Médio |
| Risco | Médio (rollback é difícil depois de `max-age` alto e `preload`) |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Infraestrutura |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Header presente em 100% das respostas; `max-age` ≥ 6 meses após período de validação |
| Observações | Não ativar `preload` na primeira iteração. |

### ARQ-104 — Implantar X-Frame-Options / frame-ancestors

| Campo | Valor |
|---|---|
| Objetivo | Impedir que o site seja embutido em `<iframe>` de terceiros (clickjacking). |
| Descrição | Nenhum header ou diretiva CSP `frame-ancestors` é declarado hoje. |
| Origem | Débito técnico #3 |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #3 |
| Arquivos afetados | Configuração Nginx (fora do repositório) |
| Dependências (depende de) | Nenhuma; pode ser combinado com a diretiva `frame-ancestors` do CSP (ARQ-102) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Header presente; teste de clickjacking (embutir o site em iframe de outro domínio) falha como esperado |
| Critérios de Regressão | Nenhuma funcionalidade legítima de embed (não identificada nenhuma no site) é quebrada |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Infraestrutura |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Header presente em 100% das respostas |
| Observações | Pode ser resolvido em conjunto com ARQ-102 (`frame-ancestors` no CSP substitui `X-Frame-Options`). |

### ARQ-105 — Implantar Referrer-Policy

| Campo | Valor |
|---|---|
| Objetivo | Controlar quanta informação de referrer vaza para destinos externos ao navegar a partir do site. |
| Descrição | Nenhuma política de referrer é declarada hoje (nem header, nem `<meta name="referrer">`). |
| Origem | Débito técnico #3 |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #3 |
| Arquivos afetados | Configuração Nginx (preferencial) ou `<meta>` nas 37 páginas |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Header/meta `Referrer-Policy` presente (ex.: `strict-origin-when-cross-origin`) |
| Critérios de Regressão | Nenhum impacto em analytics que dependa de referrer completo |
| Impacto | Baixo-Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Infraestrutura |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Header presente em 100% das respostas |
| Observações | — |

### ARQ-106 — Implantar Permissions-Policy

| Campo | Valor |
|---|---|
| Objetivo | Restringir explicitamente o acesso a APIs sensíveis do navegador (câmera, microfone, geolocalização) não usadas pelo site. |
| Descrição | Nenhuma `Permissions-Policy` é declarada hoje. O site não usa nenhuma dessas APIs, então a política pode ser restritiva por padrão. |
| Origem | Débito técnico #3 |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #3 |
| Arquivos afetados | Configuração Nginx (fora do repositório) |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Header presente restringindo câmera, microfone e geolocalização |
| Critérios de Regressão | Nenhuma funcionalidade do site depende dessas APIs (confirmado — não identificado uso) |
| Impacto | Baixo-Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Infraestrutura |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Header presente em 100% das respostas |
| Observações | — |

### ARQ-107 — Banner de consentimento de cookies (CMP) para Google Analytics

| Campo | Valor |
|---|---|
| Objetivo | Obter consentimento explícito antes de carregar cookies de analytics de terceiros, endereçando a lacuna de conformidade LGPD/GDPR. |
| Descrição | GA4 roda em todas as páginas sem qualquer mecanismo de consentimento prévio. É necessário um banner/CMP que bloqueie o carregamento do GTM/gtag até consentimento, nos 3 idiomas suportados. Este item existia apenas de forma ambígua no roadmap original, sob o rótulo genérico "LGPD" do Épico 1 — aqui é desdobrado explicitamente para não ser confundido com ARQ-101. |
| Origem | Débito técnico #16; desdobrado do rótulo "LGPD" do roadmap (ver F1-1 do documento de validação) |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #16 |
| Arquivos afetados | Novo `public/partials/cookie-banner.html`; `public/partials/scripts.html`; `public/assets/lang/pt.json`, `en.json`, `es.json`; lógica de carregamento condicional do GTM/gtag em todas as páginas |
| Dependências (depende de) | Aprovação de texto jurídico (LGPD/GDPR); recomenda-se coordenar com ARQ-102 (CSP) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Texto de consentimento aprovado por jurídico, nos 3 idiomas |
| Critérios de Aceite | Banner exibido no primeiro acesso, nos 3 idiomas; GA/GTM só carrega após consentimento explícito; opção de recusa funcional |
| Critérios de Regressão | Relatórios de Analytics continuam recebendo dados após consentimento (não há perda silenciosa de rastreamento para usuários que consentem) |
| Impacto | Alto (conformidade legal e credibilidade de marca — empresa vende conformidade como produto) |
| Risco | Médio |
| Complexidade | Média |
| Estimativa | M |
| Responsável | Jurídico |
| Status | BLOQUEADO |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 disparos de `gtag`/GTM antes do consentimento explícito, verificado via inspeção de rede |
| Observações | Bloqueado por aprovação jurídica do texto de consentimento, não por complexidade técnica. |

### ARQ-108 — Auditoria e documentação da infraestrutura real (Nginx: headers, hostname de homologação, redirects)

| Campo | Valor |
|---|---|
| Objetivo | Fechar os pontos cegos de auditoria listados na tabela "Itens que necessitam validação" de `12-technical-debt.md`, confirmando o que de fato está ativo em produção/homologação. |
| Descrição | A configuração real do Nginx não é versionada. É necessário rodar `nginx -T`/`curl -I` em produção e homologação e documentar: (a) headers HTTP realmente ativos, (b) hostname do ambiente de homologação (hoje não versionado), (c) se os redirects de `_redirects`/`vercel.json` são de fato replicados no Nginx. |
| Origem | Tabela "Itens que necessitam validação" de `12-technical-debt.md` (não é um dos 16 itens numerados, mas decorre diretamente deles) |
| Documento | `09-security.md`, `11-build-deploy.md`, `12-technical-debt.md` |
| Item da dívida técnica | N/A — relacionado aos itens #2, #3, #15 via a tabela de validação externa |
| Arquivos afetados | `docs/ambientes-e-deploy.md` (atualização do runbook com os achados) |
| Dependências (depende de) | Nenhuma dependência técnica interna |
| Dependências (desbloqueia) | ARQ-102 a ARQ-106 (confirma se já existe algo a manter/substituir); ARQ-403 (confirma se Nginx replica os redirects) |
| Pré-requisitos | Acesso de leitura à configuração Nginx de produção e homologação |
| Critérios de Aceite | Relatório de auditoria publicado no runbook, com data da checagem e evidência (`curl -I` ou equivalente) |
| Critérios de Regressão | Não aplicável (auditoria, não altera comportamento) |
| Impacto | Alto (resolve incerteza que bloqueia decisões de 6 outros itens) |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Infraestrutura |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 3/3 pontos cegos (headers, hostname homolog, redirects) documentados com evidência |
| Observações | Item de maior retorno/menor esforço do Épico 1 — deveria ser um dos primeiros a ser feito, pois desbloqueia decisão técnica em outros 6 itens. |

---

## Épico 2 — SEO (ARQ-2xx)

### ARQ-201 — Criar e versionar `og-image.jpg`

| Campo | Valor |
|---|---|
| Objetivo | Restaurar a pré-visualização de compartilhamento social (WhatsApp, LinkedIn, X, Facebook) em todas as páginas com Open Graph. |
| Descrição | Todas as páginas com metadata social referenciam `og-image.jpg`, que não existe em nenhum lugar do repositório versionado. É necessário produzir a arte final e versioná-la em `public/assets/images/`. |
| Origem | Débito técnico #1 |
| Documento | `07-seo.md`, `08-performance.md`, `12-technical-debt.md` |
| Item da dívida técnica | #1 |
| Arquivos afetados | Novo `public/assets/images/og-image.jpg` (nenhum HTML precisa mudar — os paths já apontam corretamente) |
| Dependências (depende de) | Arte final produzida pelo time de conteúdo/design |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Asset de imagem finalizado (1200×630px, formato recomendado por Open Graph) |
| Critérios de Aceite | Arquivo servindo `200 OK`; preview correto no Facebook Sharing Debugger e Twitter Card Validator |
| Critérios de Regressão | Nenhuma — item puramente aditivo |
| Impacto | Alto (risco #1 do `EXECUTIVE_SUMMARY.md`) |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Conteúdo |
| Status | BLOQUEADO |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 100% das páginas com Open Graph exibindo preview de imagem correto |
| Observações | Bloqueado apenas pela entrega da arte — zero complexidade técnica. Resolve também a incerteza "og-image.jpg existe só em produção?" da tabela de validação de `12-technical-debt.md`. |

### ARQ-202 — Reciprocidade completa de `hreflang` no cluster Ativos Digitais

| Campo | Valor |
|---|---|
| Objetivo | Garantir que o Google reconheça o cluster de 4 páginas como totalmente recíproco para segmentação internacional de idioma. |
| Descrição | `/pt/ativos-digitais/`, `/en/digital-assets/` e `/es/activos-digitales/` declaram hreflang completo apontando para `/ativos-digitais/` como `x-default`, mas essa página não declara o bloco de volta. |
| Origem | Débito técnico #5 |
| Documento | `04-routing.md`, `07-seo.md`, `12-technical-debt.md` |
| Item da dívida técnica | #5 |
| Arquivos afetados | `public/ativos-digitais/index.html` |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Bloco `hreflang` completo (incluindo `x-default`) presente nas 4 páginas do cluster |
| Critérios de Regressão | Nenhuma URL do cluster passa a apontar para destino incorreto |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | SEO |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 4/4 páginas do cluster validadas sem erro de hreflang no Google Search Console |
| Observações | — |

### ARQ-203 — Investigar divergência entre rotas reais (35) e URLs no sitemap (37)

| Campo | Valor |
|---|---|
| Objetivo | Eliminar a incerteza sobre por que o sitemap gerado contém 2 URLs a mais do que as rotas físicas confirmadas via `git ls-files`. |
| Descrição | `04-routing.md` registra essa divergência como "não investigada a fundo", sem virar item catalogado em `12-technical-debt.md`. Pode indicar URLs órfãs sendo indexadas ou apenas timing de geração — precisa de investigação para descartar impacto de SEO. |
| Origem | Achado da revisão do roadmap (F1-4 do documento de validação) — não catalogado nos 16 itens originais |
| Documento | `04-routing.md`, `07-seo.md` |
| Item da dívida técnica | N/A — identificado na revisão do roadmap, não em `12-technical-debt.md` |
| Arquivos afetados | `.github/workflows/sitemap.yml`, `public/sitemap.xml` |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Causa raiz documentada; contagem do sitemap igual à contagem real de rotas (ou divergência justificada por escrito) |
| Critérios de Regressão | Nenhuma URL legítima deixa de ser indexada após a correção |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | SEO |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | `sitemap.xml` com contagem de `<url>` = contagem de `git ls-files public/**/*.html` (excluindo partials) |
| Observações | Item novo, adicionado pela revisão arquitetural do roadmap, não pelo catálogo original de dívida técnica. |

---

## Épico 3 — Design System (ARQ-3xx)

### ARQ-301 — Unificar `--ux-*` em `--ad-*` (fonte única de tokens de marca)

| Campo | Valor |
|---|---|
| Objetivo | Eliminar a segunda fonte de verdade de cor de marca para o cluster de páginas de Ativos Digitais. |
| Descrição | `--ux-*`, definido inline em `partials/ativos-digitais-pillar-styles.html`, duplica conceitualmente `--ad-*` (definido em `foundation/tokens.css`) com valores de marca próximos mas não idênticos. Consolidar em um único namespace. |
| Origem | Débito técnico #6 |
| Documento | `06-design-system.md`, `12-technical-debt.md` |
| Item da dívida técnica | #6 |
| Arquivos afetados | `public/partials/ativos-digitais-pillar-styles.html`, `public/assets/css/foundation/tokens.css` |
| Dependências (depende de) | ARQ-501 (rede de segurança de regressão visual) |
| Dependências (desbloqueia) | ARQ-302, ARQ-404, ARQ-604 |
| Pré-requisitos | Playwright básico configurado (ARQ-501) para comparação visual antes/depois |
| Critérios de Aceite | Nenhum token `--ux-*` remanescente no repositório; todo estilo do cluster referencia `--ad-*` |
| Critérios de Regressão | Nenhuma mudança visual perceptível fora do intencional nas 4-5 páginas do cluster Ativos Digitais (diff de screenshot) |
| Impacto | Alto (consistência de marca) |
| Risco | Médio (regressão visual no cluster) |
| Complexidade | Média |
| Estimativa | M |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 ocorrências de `--ux-*` (hoje: 1 namespace inteiro) |
| Observações | Deve preceder ARQ-404, que remove o CSS que o comentário do próprio código já aponta como substituído por este partial. |

### ARQ-302 — Tokenizar breakpoints (`--breakpoint-*`)

| Campo | Valor |
|---|---|
| Objetivo | Substituir os 13 valores de `max-width` usados como números mágicos por uma escala de tokens compartilhada. |
| Descrição | 13 valores distintos (480px a 1200px) espalhados em `@media` queries sem token correspondente, com formatação inconsistente em alguns arquivos. |
| Origem | Débito técnico #10 |
| Documento | `06-design-system.md`, `12-technical-debt.md` |
| Item da dívida técnica | #10 |
| Arquivos afetados | `public/assets/css/foundation/tokens.css` + `assets-digital.css`, `diagnostico.css`, `homepage.css`, `insights-pilar.css`, `layout/layout.css`, `legal-shared.css`, `pages/como-funciona.css`, `pages/institucional.css`, `pages/pages-consolidated.css`, `pages/solucoes.css`, `sections/footer.css`, `sections/hero.css`, `sections/verticals.css`, `seguranca.css`, `styles-header-final.css`, `utilities/exec-compact.css` (16 arquivos) |
| Dependências (depende de) | ARQ-301 (evitar retrabalho), ARQ-501 (rede de segurança) |
| Dependências (desbloqueia) | Nenhuma diretamente; facilita ARQ-303/304 |
| Pré-requisitos | Playwright cobrindo responsividade nos breakpoints atuais antes da mudança |
| Critérios de Aceite | Todo `max-width` em `@media` referenciando um token `--breakpoint-*` |
| Critérios de Regressão | Responsividade idêntica testada em todos os 13 breakpoints originais, nas páginas de maior tráfego |
| Impacto | Médio |
| Risco | Médio-Alto (maior superfície de arquivos tocados do backlog) |
| Complexidade | Alta |
| Estimativa | G |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 valores `max-width` mágicos fora de token (hoje: 13) |
| Observações | Item de maior risco de regressão visual do Épico 3 — executar por último dentro do épico. |

### ARQ-303 — Criar tokens globais `--radius-*`/`--shadow-*`

| Campo | Valor |
|---|---|
| Objetivo | Eliminar valores literais de raio de borda e sombra fora da extensão `--ad-*`, trazendo-os para a camada `foundation/`. |
| Descrição | Raios e sombras hoje só têm token na extensão `--ad-*`; fora dela aparecem como valores literais espalhados (ex. `components/cards.css:13`). |
| Origem | Débito técnico #6 (contexto de fragmentação de design tokens) |
| Documento | `06-design-system.md` |
| Item da dívida técnica | #6 (mesma raiz da fragmentação de tokens, aspecto radius/shadow) |
| Arquivos afetados | `public/assets/css/foundation/tokens.css`, `public/assets/css/components/cards.css` e demais arquivos com valores literais |
| Dependências (depende de) | Nenhuma dependência forte; pode rodar em paralelo com ARQ-302 |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Nenhum `border-radius`/`box-shadow` literal fora de token, exceto onde documentado como exceção deliberada |
| Critérios de Regressão | Nenhuma mudança visual de raio/sombra fora do intencional |
| Impacto | Baixo-Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | M |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Contagem de valores literais de radius/shadow fora de token = 0 |
| Observações | — |

### ARQ-304 — Padronizar formatação de `@media` (espaçamento após `:`)

| Campo | Valor |
|---|---|
| Objetivo | Eliminar a inconsistência de formatação `max-width:768px` vs. `max-width: 768px` no mesmo arquivo. |
| Descrição | `layout/layout.css:24,30` mistura as duas formatações; provavelmente presente em outros arquivos CSS também. |
| Origem | Débito técnico #10 |
| Documento | `06-design-system.md`, `12-technical-debt.md` |
| Item da dívida técnica | #10 |
| Arquivos afetados | `public/assets/css/layout/layout.css` e demais arquivos CSS a auditar |
| Dependências (depende de) | Pode ser resolvido no mesmo commit de ARQ-302 |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Lint de CSS sem inconsistência de espaçamento em `@media` |
| Critérios de Regressão | Nenhuma (mudança puramente cosmética/formatação, sem efeito em cascata) |
| Impacto | Baixo |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 inconsistências reportadas por lint (Stylelint ou equivalente) |
| Observações | Candidato natural a ser resolvido junto de ARQ-504 (lint em CI). |

---

## Épico 4 — Consolidação Arquitetural (ARQ-4xx)

### ARQ-401 — Remover `navigation.js`

| Campo | Valor |
|---|---|
| Objetivo | Eliminar script morto remanescente da migração SPA → MPA. |
| Descrição | `navigation.js` contém apenas um IIFE com `return` imediato e comentário `NAVIGATION DISABLED (MPA MODE)`. Confirmado por busca em todo `public/**/*.html`: **0 páginas o referenciam**. |
| Origem | Débito técnico #14 |
| Documento | `12-technical-debt.md` |
| Item da dívida técnica | #14 |
| Arquivos afetados | `public/assets/js/navigation.js` (remoção) |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Arquivo removido do repositório |
| Critérios de Regressão | Build/deploy funciona normalmente; nenhuma página quebrada (confirmado: 0 referências) |
| Impacto | Baixo |
| Risco | Baixíssimo (confirmado via grep: nenhuma inclusão) |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Frontend |
| Status | CONCLUÍDO (Sprint 1, 2026-07-23) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Arquivo ausente do repositório; 0 erros 404 de asset em produção após deploy |
| Observações | Item de risco confirmado mais baixo de todo o backlog — pode ser feito a qualquer momento. Removido em Sprint 1: revalidado via grep (0 referências em HTML/JS/JSON/YAML do repositório inteiro) e via `partials/scripts.html` (nunca incluído entre os 4 scripts globais). Validação funcional: servidor local confirma `404` para `/assets/js/navigation.js` após a remoção. |

### ARQ-402 — Remover IDs vestigiais de `i18n-config.json`

| Campo | Valor |
|---|---|
| Objetivo | Eliminar referência a IDs de DOM que não existem mais em nenhuma página atual. |
| Descrição | `legalPages` em `i18n-config.json` lista IDs (`page-institucional` etc.) que nenhuma página usa como `id` hoje — o padrão atual usa a classe `legal-page`. `isLegalPage()` já funciona só pelo fallback de classe (`i18n.js:75`); o array de IDs é código morto. |
| Origem | Débito técnico #13 |
| Documento | `12-technical-debt.md` |
| Item da dívida técnica | #13 |
| Arquivos afetados | `public/assets/config/i18n-config.json`, `public/assets/js/i18n.js:74-79` |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Array `legalPages` removido (ou documentado como intencionalmente reservado, se decidido manter); `isLegalPage()` usando só o fallback de classe |
| Critérios de Regressão | Detecção de páginas legais continua funcionando em 100% das páginas `legal-page` |
| Impacto | Baixo |
| Risco | Baixo (fallback por classe já cobre 100% dos casos hoje) |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Frontend |
| Status | CONCLUÍDO (Sprint 1, 2026-07-23) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 IDs vestigiais remanescentes em `i18n-config.json` |
| Observações | Removido em Sprint 1: array `legalPages` eliminado de `i18n-config.json` e do fallback de config em `i18n.js` (mesma duplicação, não catalogada individualmente antes); `isLegalPage()` simplificado para usar só `body.classList.contains('legal-page')`. Validação: confirmado que as 7 páginas legais usam `legal-page` como classe (nunca como `id`) via grep; JSON e sintaxe JS validados (`node --check`); servidor local confirma que `i18n-config.json` e `i18n.js` servem o conteúdo simplificado. |

### ARQ-403 — Decidir e consolidar `vercel.json`/`_redirects`

| Campo | Valor |
|---|---|
| Objetivo | Eliminar a ambiguidade de ter dois arquivos de redirect (sintaxe Netlify e Vercel) quando a produção real roda em Nginx + Docker self-hosted. |
| Descrição | `public/_redirects` e `public/vercel.json` implementam as mesmas ~4-5 regras de redirect legado em sintaxes de plataformas não usadas em produção. É preciso confirmar se o Nginx replica esses redirects e, então, escolher uma única fonte de verdade (documentar no Nginx, ou remover os arquivos se comprovadamente inertes). |
| Origem | Débito técnico #15 |
| Documento | `04-routing.md`, `12-technical-debt.md` |
| Item da dívida técnica | #15 |
| Arquivos afetados | `public/vercel.json`, `public/_redirects` |
| Dependências (depende de) | ARQ-108 (confirmação se Nginx replica os redirects) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Resultado da auditoria de ARQ-108 |
| Critérios de Aceite | Uma única fonte de verdade para redirects legados, confirmada ativa em produção |
| Critérios de Regressão | As ~5 URLs legadas continuam redirecionando corretamente após a mudança |
| Impacto | Médio |
| Risco | Médio (remover sem confirmar pode quebrar redirects se, inesperadamente, algo depender do arquivo) |
| Complexidade | Baixa |
| Estimativa | P-M |
| Responsável | DevOps |
| Status | BLOQUEADO |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Teste de todas as URLs legadas retornando 301 correto após a consolidação |
| Observações | Bloqueado por ARQ-108, não por complexidade técnica própria. |

### ARQ-404 — Remover 6 arquivos CSS "deprecated" e seus `<link>` associados

| Campo | Valor |
|---|---|
| Objetivo | Eliminar requisições HTTP que não entregam estilo nenhum. |
| Descrição | `dropdown-menu.css`, `pages/ativos-digitais-pillar-styles.css`, `pages/fundamento-juridico.css`, `pages/politica-de-privacidade.css`, `pages/preservacao-probatoria-digital.css` e `pages/termos-de-custodia.css` foram esvaziados, mas continuam referenciados via `<link>` em 21 ocorrências HTML. |
| Origem | Débito técnico #9 |
| Documento | `08-performance.md`, `12-technical-debt.md` |
| Item da dívida técnica | #9 |
| Arquivos afetados | 6 arquivos CSS deprecated (remoção) + 21 `<link rel="stylesheet">` em páginas HTML (ex. `public/legal/termos-de-uso.html`, `public/legal/institucional.html`, cluster `/ativos-digitais/`) |
| Dependências (depende de) | ARQ-301 (garantir que nada em `ativos-digitais-pillar-styles.css` ainda é necessário), ARQ-501 (rede de segurança) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | ARQ-301 concluído |
| Critérios de Aceite | 0 arquivos CSS "deprecated" no repositório; 0 `<link>` órfão apontando para eles |
| Critérios de Regressão | Nenhuma página perde estilo (confirmado que os arquivos já estão vazios hoje, então a remoção do `<link>` não deveria afetar nada visualmente) |
| Impacto | Baixo (performance marginal) |
| Risco | Baixo (mecânico, mas fácil esquecer 1 dos 21 `<link>`) |
| Complexidade | Média (superfície ampla, baixo risco individual) |
| Estimativa | M |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 requisições HTTP para CSS vazio (hoje: 21) |
| Observações | Depende de ARQ-301 estar concluído para não remover algo ainda em uso. |

### ARQ-405 — Resolver nomenclatura `mobile-menu.js`/`dropdown-menu.js`

| Campo | Valor |
|---|---|
| Objetivo | Alinhar o nome dos arquivos à responsabilidade real, evitando que um desenvolvedor futuro edite o arquivo errado ou duplique lógica. |
| Descrição | `mobile-menu.js` controla tanto o menu mobile quanto os dropdowns de desktop, apesar do nome sugerir escopo apenas mobile. `dropdown-menu.js`, cujo nome sugeriria a lógica de dropdown, hoje só emite um `console.warn`. Decidir entre renomear `mobile-menu.js` (ex. `navigation-menu.js`) ou mover de fato a lógica de dropdown para `dropdown-menu.js`. |
| Origem | Débito técnico #4 — não estava representado em nenhum épico do roadmap original (achado F1-1 do documento de validação); adicionado explicitamente aqui |
| Documento | `12-technical-debt.md` |
| Item da dívida técnica | #4 |
| Arquivos afetados | `public/assets/js/mobile-menu.js`, `public/assets/js/dropdown-menu.js`, `public/partials/scripts.html` |
| Dependências (depende de) | ARQ-501 (rede de segurança — script ativo em 100% das páginas) |
| Dependências (desbloqueia) | ARQ-603 |
| Pré-requisitos | Playwright cobrindo o fluxo de navegação/menu antes da mudança |
| Critérios de Aceite | Nome do arquivo reflete a responsabilidade real; nenhuma duplicação de lógica de dropdown entre os dois arquivos |
| Critérios de Regressão | Menu mobile e dropdowns de desktop continuam funcionando de forma idêntica em todas as páginas (teste manual + Playwright) |
| Impacto | Médio (manutenibilidade futura) |
| Risco | Médio-Alto (script de navegação usado em 100% das páginas) |
| Complexidade | Média |
| Estimativa | M |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 duplicação de lógica de dropdown entre arquivos; nome do arquivo corresponde à responsabilidade documentada em `05-components.md` |
| Observações | Item adicionado nesta revisão — ausente do roadmap original (`15-architecture-roadmap.md`), ver F1-1. |

### ARQ-406 — Corrigir direção do sync `main → homolog` no workflow de sitemap

| Campo | Valor |
|---|---|
| Objetivo | Alinhar o workflow automatizado ao fluxo de validação documentado (`feature → homolog → main`), evitando que o ambiente de homologação seja sobrescrito com conteúdo de produção antes de qualquer validação. |
| Descrição | `.github/workflows/sitemap.yml` faz merge de `main` em `homolog` automaticamente a cada push em `main`, o oposto do fluxo de validação recomendado. O próprio runbook já registra isso como pendência de revisão da equipe. |
| Origem | Débito técnico #7 — não estava representado em nenhum épico do roadmap original (achado F1-1); adicionado explicitamente aqui |
| Documento | `11-build-deploy.md`, `12-technical-debt.md` |
| Item da dívida técnica | #7 |
| Arquivos afetados | `.github/workflows/sitemap.yml` |
| Dependências (depende de) | Decisão de processo com o time (não é uma decisão puramente técnica) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Alinhamento do time sobre o fluxo correto de sync entre branches |
| Critérios de Aceite | Direção do sync alinhada ao fluxo documentado em `13-development-workflow.md`, ou decisão documentada de manter o comportamento atual com justificativa explícita |
| Critérios de Regressão | Deploy automático de homolog e produção continuam funcionando após a mudança do workflow |
| Impacto | Médio (integridade do fluxo de homologação) |
| Risco | Médio (mexe em pipeline de deploy compartilhado) |
| Complexidade | Baixa |
| Estimativa | P-M |
| Responsável | DevOps |
| Status | BLOQUEADO |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Direção de sync documentada e consistente com o fluxo de branches oficial |
| Observações | Bloqueado por decisão de processo do time, não por complexidade técnica. Item adicionado nesta revisão — ausente do roadmap original. |

---

## Épico 5 — Engenharia (ARQ-5xx)

### ARQ-501 — Configurar Playwright (config + smoke tests)

| Campo | Valor |
|---|---|
| Objetivo | Criar a primeira rede de segurança automatizada contra regressão, servindo de pré-requisito transversal para os itens de maior risco visual/funcional do backlog. |
| Descrição | `@playwright/test` está instalado localmente (não commitado), sem `playwright.config.*` nem nenhum arquivo `*.spec.*`. É necessário configurar a suíte, commitar as dependências e cobrir ao menos os fluxos críticos (menu de navegação, i18n, formulário de diagnóstico). |
| Origem | Débito técnico #11 |
| Documento | `10-dependencies.md`, `13-development-workflow.md`, `12-technical-debt.md` |
| Item da dívida técnica | #11 |
| Arquivos afetados | Novo `playwright.config.ts`, `tests/*.spec.ts`; commit de `package.json`/`package-lock.json`; novo workflow de CI para rodar a suíte |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | ARQ-301, ARQ-302, ARQ-404, ARQ-405, ARQ-502, ARQ-504 |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Suíte roda em CI a cada PR; cobre no mínimo menu de navegação, troca de idioma e submissão do formulário de diagnóstico (mockado) |
| Critérios de Regressão | Não aplicável (item aditivo, cria a própria rede de regressão) |
| Impacto | Alto (rede de segurança para todo o restante do backlog) |
| Risco | Baixo (aditivo, não modifica comportamento existente) |
| Complexidade | Alta (primeira suíte do zero, sem precedente no projeto) |
| Estimativa | G |
| Responsável | DevOps |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Cobertura Playwright ≥ 3 fluxos críticos rodando em CI a cada PR |
| Observações | **Deve ser o primeiro item do backlog a ser executado**, antes de qualquer item com risco Médio ou superior (ver Fase 4 do documento de validação do roadmap). Apesar de estar numerado no Épico 5, sua execução não deve esperar o Épico 5 começar. |

### ARQ-502 — Unificar esquema de cache-busting

| Campo | Valor |
|---|---|
| Objetivo | Eliminar o risco de cache desatualizado por convenção de versionamento inconsistente. |
| Descrição | Três esquemas convivem hoje: contador simples (`main.css?v=7`), data `AAAAMMDDNN` (`i18n.js?v=2026041001`) e contador por arquivo (`lang/pt.json?v=10`). Definir e aplicar uma única convenção. |
| Origem | Débito técnico #12 |
| Documento | `08-performance.md`, `12-technical-debt.md` |
| Item da dívida técnica | #12 |
| Arquivos afetados | Todos os `<link>`/`<script>` com `?v=` nas 37+ páginas; `main.css`, `i18n.js`, `search.js`, `mobile-menu.js`, `search-index.json`, `lang/*.json` |
| Dependências (depende de) | ARQ-501 (regressão de cache é difícil de detectar manualmente) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Playwright ativo para validar que assets corretos são carregados após a mudança |
| Critérios de Aceite | 1 única convenção documentada e aplicada em 100% das referências versionadas |
| Critérios de Regressão | Nenhum asset servido com versão desatualizada em cache do navegador após deploy |
| Impacto | Médio |
| Risco | Médio (cache antigo servido incorretamente durante a transição) |
| Complexidade | Média (mecânico, mas alto número de arquivos) |
| Estimativa | G |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 arquivos fora da convenção única (hoje: 3 esquemas distintos) |
| Observações | — |

### ARQ-503 — Eliminar `preconnect` duplicado de fontes

| Campo | Valor |
|---|---|
| Objetivo | Remover a duplicação de `<link rel="preconnect">` para Google Fonts, declarado tanto estaticamente quanto via injeção JS. |
| Descrição | A maioria das páginas carrega o par de `preconnect` duas vezes: uma vez estática no `<head>` (quando presente) e novamente via injeção dinâmica em `header.html` (mitigado por guarda, mas ainda redundante na declaração). |
| Origem | Achado da revisão do roadmap (F1-4 do documento de validação) — não catalogado nos 16 itens originais |
| Documento | `08-performance.md` |
| Item da dívida técnica | N/A — identificado na revisão do roadmap, não em `12-technical-debt.md` |
| Arquivos afetados | `public/index.html`, `public/partials/header.html` |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | 1 único par de `preconnect` por página carregada |
| Critérios de Regressão | Fontes continuam carregando sem atraso perceptível (preconnect ainda ocorre, só não duplicado) |
| Impacto | Baixo |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 1 par de preconnect por página (hoje: 2) |
| Observações | Item novo, adicionado pela revisão arquitetural do roadmap. |

### ARQ-504 — Automatizar checklist de publicação em CI (lint, `git diff --check`)

| Campo | Valor |
|---|---|
| Objetivo | Substituir a validação manual do checklist de publicação por um gate automatizado em CI. |
| Descrição | O runbook já define um checklist manual (`docs/ambientes-e-deploy.md:42-47`): testar URLs, conferir redirecionamentos, validar chaves de idioma, rodar `git diff --check`. Automatizar o que for possível como workflow de CI. |
| Origem | 13-development-workflow.md |
| Documento | `13-development-workflow.md`, `12-technical-debt.md` |
| Item da dívida técnica | N/A — decorre do Épico 5 do roadmap ("Validações", "Lint"), sem item numerado específico em `12-technical-debt.md` |
| Arquivos afetados | Novo `.github/workflows/lint.yml` |
| Dependências (depende de) | ARQ-501 (mesma infraestrutura de CI) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | CI falha automaticamente em PR com problema hoje detectado só manualmente (ex. merge conflict marker, espaço em branco problemático) |
| Critérios de Regressão | Nenhum PR legítimo passa a falhar por falso positivo do lint |
| Impacto | Médio (reduz erro humano) |
| Risco | Baixo |
| Complexidade | Média |
| Estimativa | M |
| Responsável | DevOps |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 100% dos itens automatizáveis do checklist do runbook rodando em CI |
| Observações | Pode absorver ARQ-304 (lint de formatação CSS) como parte do mesmo workflow. |

### ARQ-505 — Auditar paridade de `docker-compose.yml` entre produção e homologação

| Campo | Valor |
|---|---|
| Objetivo | Confirmar que os ambientes de produção e homologação rodam configurações de container equivalentes, evitando que um bug só se manifeste em um dos dois. |
| Descrição | `docker-compose.yml` vive fora do repositório, em `/opt/tutela-v2` de cada servidor — não há garantia versionada de que os dois arquivos são idênticos. |
| Origem | Tabela "Itens que necessitam validação" de `12-technical-debt.md` |
| Documento | `11-build-deploy.md`, `12-technical-debt.md` |
| Item da dívida técnica | N/A — decorre da tabela de validação externa de `12-technical-debt.md`, não de um dos 16 itens numerados |
| Arquivos afetados | `docs/ambientes-e-deploy.md` (documentação do resultado da auditoria) |
| Dependências (depende de) | Nenhuma dependência técnica interna |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Acesso aos dois servidores (produção e homologação) |
| Critérios de Aceite | Diff entre os dois `docker-compose.yml` documentado; divergências relevantes justificadas ou corrigidas |
| Critérios de Regressão | Não aplicável (auditoria) |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | DevOps |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Diff documentado; 0 divergências não justificadas |
| Observações | Item novo, adicionado para fechar um ponto cego já citado (mas não convertido em item de ação) em `12-technical-debt.md`. |

---

## Épico 6 — Acessibilidade (ARQ-6xx)

### ARQ-601 — Adicionar skip-link (`#main-content`)

| Campo | Valor |
|---|---|
| Objetivo | Permitir que usuários de teclado/leitor de tela pulem a navegação e cheguem direto ao conteúdo principal. |
| Descrição | Nenhuma página do site contém um link "pular para o conteúdo". Como o header é resolvido via SSI a partir de um único partial, esta é a correção de maior retorno/menor esforço do backlog inteiro: 1 arquivo corrige as 37 páginas. |
| Origem | Débito técnico #8 |
| Documento | `12-technical-debt.md` |
| Item da dívida técnica | #8 |
| Arquivos afetados | `public/partials/header.html` (propagado a todas as páginas via SSI) |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | ARQ-602 (mesmo arquivo, sequenciamento natural) |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Skip-link funcional via teclado (primeiro elemento focável) em todas as páginas |
| Critérios de Regressão | Nenhuma mudança visual para usuários de mouse (skip-link visível só no foco) |
| Impacto | Alto/esforço mínimo — melhor relação custo-benefício de todo o backlog |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Skip-link funcional em 37/37 páginas, validado com navegação por Tab |
| Observações | Recomendado como um dos primeiros itens a implementar, independentemente da ordem formal dos épicos, dado o retorno desproporcional ao esforço. |

### ARQ-602 — Auditoria de landmarks/ARIA

| Campo | Valor |
|---|---|
| Objetivo | Garantir que `main`, `nav`, `header` e `footer` tenham roles/landmarks corretos para tecnologia assistiva. |
| Descrição | Auditoria geral de semântica ARIA nos partials compartilhados e templates de página. |
| Origem | Contexto WCAG geral (`06-design-system.md`, `12-technical-debt.md`) |
| Documento | `12-technical-debt.md` |
| Item da dívida técnica | N/A — decorre do Épico 6 do roadmap ("ARIA", "Landmarks"), sem item numerado específico em `12-technical-debt.md` |
| Arquivos afetados | `public/partials/header.html`, `public/partials/footer.html`, templates de página |
| Dependências (depende de) | ARQ-601 (mesmo arquivo, sequenciamento natural) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Landmarks corretos validados com axe-core (ou equivalente) em todos os templates de página |
| Critérios de Regressão | Nenhuma mudança de comportamento visual; apenas semântica |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Média |
| Estimativa | M |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 erros de landmark/ARIA reportados por axe-core |
| Observações | — |

### ARQ-603 — Navegação por teclado nos dropdowns

| Campo | Valor |
|---|---|
| Objetivo | Garantir que os dropdowns de navegação sejam 100% operáveis via teclado (Tab/Enter/Esc). |
| Descrição | Auditoria e correção de comportamento de teclado no script de menu, hoje concentrado em `mobile-menu.js`. |
| Origem | Contexto do débito técnico #4 (mesmo arquivo) e Épico 6 do roadmap ("Keyboard") |
| Documento | `12-technical-debt.md` |
| Item da dívida técnica | N/A — relacionado ao item #4 via arquivo, mas o teste de teclado em si não está numerado em `12-technical-debt.md` |
| Arquivos afetados | Sucessor de `mobile-menu.js`/`dropdown-menu.js` definido em ARQ-405 |
| Dependências (depende de) | ARQ-405 (não auditar código que ainda será reorganizado) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | ARQ-405 concluído |
| Critérios de Aceite | Dropdowns 100% operáveis via teclado (abrir, navegar itens, fechar com Esc) |
| Critérios de Regressão | Comportamento de mouse/touch inalterado |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Média |
| Estimativa | M |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 100% dos itens de dropdown operáveis via teclado, validado manualmente e via Playwright |
| Observações | — |

### ARQ-604 — Auditoria e correção de contraste (WCAG AA)

| Campo | Valor |
|---|---|
| Objetivo | Garantir que todos os pares texto/fundo atendam ao contraste mínimo exigido pelo WCAG AA. |
| Descrição | Auditoria de contraste em toda a paleta de cores em uso, após a consolidação de tokens (ARQ-301). |
| Origem | Contexto WCAG geral (`06-design-system.md`) e Épico 6 do roadmap ("Contraste") |
| Documento | `06-design-system.md`, `12-technical-debt.md` |
| Item da dívida técnica | N/A — decorre do Épico 6 do roadmap, sem item numerado específico em `12-technical-debt.md` |
| Arquivos afetados | `public/assets/css/foundation/tokens.css` e usos de cor em componentes/páginas |
| Dependências (depende de) | ARQ-301 (tokens de cor já unificados, evita retrabalho) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | ARQ-301 concluído |
| Critérios de Aceite | Todos os pares texto/fundo ≥ 4.5:1 (ou 3:1 para texto grande), conforme WCAG AA |
| Critérios de Regressão | Identidade visual de marca preservada (ajustes de contraste não descaracterizam a paleta) |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Média |
| Estimativa | M |
| Responsável | Frontend |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 100% dos pares texto/fundo auditados atendendo WCAG AA |
| Observações | — |

---

## Épico 7 — Governança (ARQ-7xx)

### ARQ-701 — ADRs para decisões arquiteturais relevantes

| Campo | Valor |
|---|---|
| Objetivo | Registrar de forma permanente o "porquê" de cada decisão arquitetural não-óbvia tomada ao longo da execução deste backlog. |
| Descrição | Criar 1 ADR por decisão relevante (ex.: por que `--ad-*` venceu sobre `--ux-*`, por que a direção do sync do sitemap mudou, qual convenção de cache-busting foi escolhida). Recomendado como atividade **contínua**, não um sprint isolado ao final — ver parecer do documento de validação do roadmap. |
| Origem | Roadmap, Épico 7 ("ADRs") |
| Documento | `15-architecture-roadmap.md` |
| Item da dívida técnica | N/A — requisito de governança do roadmap, não corresponde a um item de `12-technical-debt.md` |
| Arquivos afetados | Novo diretório `docs/architecture/adr/` |
| Dependências (depende de) | Nenhuma dependência dura; alimentado pela conclusão de cada ARQ individual |
| Dependências (desbloqueia) | ARQ-702, ARQ-703 |
| Pré-requisitos | Nenhum — pode começar imediatamente e crescer incrementalmente |
| Critérios de Aceite | 1 ADR publicado por decisão não-óbvia tomada, no momento em que a decisão é tomada |
| Critérios de Regressão | Não aplicável |
| Impacto | Alto (rastreabilidade de longo prazo) |
| Risco | Baixo |
| Complexidade | Baixa (por ADR individual) |
| Estimativa | M (contínuo, ao longo de todos os épicos) |
| Responsável | Arquitetura |
| Status | BACKLOG |
| ADR relacionado | Não aplicável (este item cria os ADRs) |
| Métrica de sucesso | Cobertura de ADR = 100% dos ARQs concluídos que envolveram decisão não-óbvia |
| Observações | Este item está explicitamente fora do escopo desta etapa de criação de backlog (restrição: "Não criar ADRs"). Sua execução real começa apenas na fase de implementação. |

### ARQ-702 — Criar `CLAUDE.md` do projeto

| Campo | Valor |
|---|---|
| Objetivo | Permitir que qualquer novo desenvolvedor (humano ou assistente de IA) se oriente sobre convenções e arquitetura do projeto sem depender de conhecimento tácito. |
| Descrição | Consolidar convenções observadas (`13-development-workflow.md`) e decisões estabilizadas em um `CLAUDE.md` na raiz do projeto. |
| Origem | Roadmap, Épico 7 ("CLAUDE.md") |
| Documento | `15-architecture-roadmap.md`, `13-development-workflow.md` |
| Item da dívida técnica | N/A — requisito de governança do roadmap |
| Arquivos afetados | Novo `CLAUDE.md` (raiz do projeto) |
| Dependências (depende de) | ARQ-701 (conteúdo de decisões já registrado em ADRs) |
| Dependências (desbloqueia) | ARQ-703 |
| Pré-requisitos | Conteúdo técnico dos Épicos 1-6 estabilizado |
| Critérios de Aceite | Um desenvolvedor que não participou da criação consegue se orientar lendo só o arquivo |
| Critérios de Regressão | Não aplicável |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Arquitetura |
| Status | BACKLOG |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Validação por um desenvolvedor externo à criação do documento |
| Observações | Este item está explicitamente fora do escopo desta etapa de criação de backlog (restrição: "Não criar CLAUDE.md"). Sua execução real começa apenas na fase de implementação. |

### ARQ-703 — Manifesto/Princípios/Engineering Guide formalizados

| Campo | Valor |
|---|---|
| Objetivo | Consolidar os princípios de evolução (P1-P7 do roadmap) e as convenções de engenharia em um guia único e revisado pelo time. |
| Descrição | Formalizar o conteúdo já esboçado em `15-architecture-roadmap.md` (Objetivos Estratégicos, Princípios de Evolução) em um documento de governança permanente, incluindo o próprio `docs/architecture/15-architecture-roadmap.md` como commit oficial (já realizado). |
| Origem | Roadmap, Épico 7 ("Manifesto", "Princípios", "Engineering Guide") |
| Documento | `15-architecture-roadmap.md` |
| Item da dívida técnica | N/A — requisito de governança do roadmap |
| Arquivos afetados | Novo documento de Engineering Guide em `docs/architecture/` |
| Dependências (depende de) | ARQ-701, ARQ-702 |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | ARQ-701 e ARQ-702 concluídos |
| Critérios de Aceite | Documento único revisado e aprovado pelo time |
| Critérios de Regressão | Não aplicável |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | M |
| Responsável | Arquitetura |
| Status | REDEFINIDO (2026-07-23) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Documento aprovado formalmente pelo time em revisão |
| Observações | Reavaliado na revisão final da fase estrutural. O escopo de conteúdo (princípios de evolução + convenções de engenharia formalizadas permanentemente) foi atendido por [17-architectural-manifesto.md](17-architectural-manifesto.md) (princípios) e [../governance/18-engineering-principles.md](../governance/18-engineering-principles.md) (convenções) — mas como **dois documentos separados**, não o "guia único" originalmente previsto neste item, e sem revisão formal pelo time humano (apenas aprovação "com ressalvas" na revisão arquitetural). Por isso o item é marcado **Redefinido**, não Concluído: o ID permanece reservado e não será reaberto para recriar um "guia único" — 17 e 18 são, a partir de agora, os documentos oficiais que cumprem esse papel. ARQ-701 (ADRs) e ARQ-702 (CLAUDE.md) continuam abertos, sem alteração, pois seu escopo não foi atendido por nenhum documento existente. |

---

## Marcos Arquiteturais

### Marco 1 — Arquitetura Auditável
`ARQ-101` a `ARQ-108` (Segurança) + `ARQ-201` a `ARQ-203` (SEO). Fecha os 3 riscos de maior impacto listados no `EXECUTIVE_SUMMARY.md` (og-image, endpoint de diagnóstico, headers de segurança) e elimina todos os pontos cegos de auditoria hoje dependentes de validação externa ao repositório.

### Marco 2 — Design System Unificado
`ARQ-301` a `ARQ-304`. Nenhum token duplicado remanescente (`--ux-*` eliminado, breakpoints e radius/shadow tokenizados) — critério de aceite explícito do Épico 3 do roadmap.

### Marco 3 — Pipeline de Engenharia Consolidado
`ARQ-401` a `ARQ-406` (Consolidação) + `ARQ-501` a `ARQ-505` (Engenharia). Combina a eliminação de vestígios da arquitetura anterior com a automação do pipeline (Playwright, lint, cache-busting único) — os dois épicos são tratados como um marco só porque a "Definição de Concluído" do roadmap exige rede de testes automatizada para considerar qualquer consolidação como encerrada.

### Marco 4 — Conformidade WCAG
`ARQ-601` a `ARQ-604`. Alinhado ao critério "WCAG AA" do Épico 6 do roadmap.

### Marco 5 — Governança Completa
`ARQ-701` a `ARQ-703`. Todo novo desenvolvedor compreende a arquitetura lendo apenas a documentação — critério de aceite explícito do Épico 7 do roadmap.

---

## Validação do Backlog

Checagem executada antes de finalizar este documento:

- [x] **Todos os 16 itens de dívida técnica de `12-technical-debt.md` possuem pelo menos um ARQ.** Mapeamento: #1→ARQ-201, #2→ARQ-101, #3→ARQ-102/103/104/105/106, #4→ARQ-405, #5→ARQ-202, #6→ARQ-301/303, #7→ARQ-406, #8→ARQ-601, #9→ARQ-404, #10→ARQ-302/304, #11→ARQ-501, #12→ARQ-502, #13→ARQ-402, #14→ARQ-401, #15→ARQ-403, #16→ARQ-107.
- [x] **Todos os 33 ARQs possuem responsável**, restrito às 9 categorias definidas.
- [x] **Todos os 33 ARQs possuem critérios de aceite** (mesmo os de auditoria/documentação, cujo critério é a publicação do achado).
- [x] **Todos os 33 ARQs possuem métrica de sucesso objetiva.**
- [x] **Não há duplicações de ID.** Cada ARQ aparece uma única vez no documento.
- [x] **Não há ARQs órfãos.** Todo ID citado em um campo "Dependências" corresponde a um item de fato definido neste backlog.
- [x] **Todas as dependências são consistentes** (nenhuma dependência circular; toda relação "depende de" tem uma contraparte "desbloqueia" no item referenciado, ou é uma dependência externa explícita ao repositório).
- [x] **Todos os 7 épicos têm backlog suficiente para execução independente**: Segurança (8 itens), SEO (3), Design System (4), Consolidação (6), Engenharia (5), Acessibilidade (4), Governança (3) — nenhum épico depende de detalhamento adicional para que um time comece a trabalhar.

Itens adicionados nesta etapa que não constavam do roadmap original (`15-architecture-roadmap.md`) nem do catálogo de dívida técnica numerado: `ARQ-107` (desdobrado do rótulo genérico "LGPD"), `ARQ-108`, `ARQ-203`, `ARQ-405`, `ARQ-406`, `ARQ-503`, `ARQ-505`. Todos rastreados explicitamente no campo "Origem" de cada item.
