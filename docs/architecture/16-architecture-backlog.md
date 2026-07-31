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
- Próximo ID livre por épico neste momento: `ARQ-109`, `ARQ-204`, `ARQ-305`, `ARQ-407`, `ARQ-506`, `ARQ-608` (ARQ-606/ARQ-607 já atribuídos), `ARQ-704`.

## Fontes utilizadas

`README.md`, `EXECUTIVE_SUMMARY.md`, `01-overview.md` a `14-glossary.md`, `15-architecture-roadmap.md`, e o documento de validação do roadmap produzido na etapa anterior (revisão crítica, backlog preliminar, matriz de dependências e parecer arquitetural). Onde um item deste backlog não corresponde a nenhum dos 16 itens numerados de `12-technical-debt.md`, isso é sinalizado explicitamente no campo "Item da dívida técnica".

---

## Épico 1 — Segurança (ARQ-1xx)

### ARQ-101 — Auditoria e documentação do tratamento de dados de `/api/diagnostico` (LGPD)

| Campo | Valor |
|---|---|
| Objetivo | Tornar auditável, a partir de evidência documentada, como nome/e-mail/respostas coletados no formulário de diagnóstico são validados, transmitidos e armazenados. |
| Descrição | O endpoint `/api/diagnostico` não tinha implementação, proxy ou contrato documentado neste repositório até a Sprint 24 (`ARQ-507`), quando o backend foi versionado em `github.com/cleberNetCenter/tutela-api`. Sprint 25 auditou esse código com evidência de arquivo/linha (coleta, validação, armazenamento, transmissão, retenção, acesso, consentimento, direito de exclusão, terceiros) e registrou o fluxo completo em `09-security.md`. |
| Origem | Débito técnico #2 |
| Documento | `09-security.md`, `12-technical-debt.md` |
| Item da dívida técnica | #2 |
| Arquivos afetados | `09-security.md` (fluxo documentado); repositório `tutela-api` (`server.js`, `lib/leadsStore.js` novo, `.env.example` novo, `test/*.test.js` novos — retenção, exclusão, consentimento; `requireTLS: true` da Sprint 25 já publicado em `main`/`homolog`); repositório `tutela` (`public/assets/js/diagnostico.js` — envio do campo de consentimento) |
| Dependências (depende de) | Nenhuma dependência técnica interna |
| Dependências (desbloqueia) | Nenhuma diretamente; informa o escopo final de ARQ-107 |
| Pré-requisitos | ~~Acesso à equipe/infra responsável pelo backend do endpoint~~ — obtido nesta sprint (acesso SSH Git já configurado ao repositório `tutela-api`) |
| Critérios de Aceite | Documento descrevendo validação server-side, armazenamento e retenção de dados publicado e revisado por jurídico e pela equipe de backend |
| Critérios de Regressão | Não aplicável (item de auditoria/documentação; a única mudança de código foi aditiva e de baixo risco — `requireTLS`, não publicada) |
| Impacto | Alto — dado pessoal, LGPD, é o item #2 nos "3 riscos de maior impacto" do `EXECUTIVE_SUMMARY.md` |
| Risco | Alto |
| Complexidade | Alta (depende de coordenação entre times/sistemas fora deste repositório) |
| Estimativa | G |
| Responsável | Segurança |
| Status | 4/4 LACUNAS TÉCNICAS IMPLEMENTADAS (retenção, exclusão, consentimento, texto de política de privacidade) — aguardando revisão jurídica formal (Sprint 26, 2026-07-27). Sprint 29 (2026-07-29) fechou os 3 achados incidentais represados desde a Sprint 26 (CVE do `nodemailer`, `trust proxy` ausente, `response.ok` não verificado) — ver Observações. **Não fechar como CONCLUÍDO** — critério de aceite exige revisão jurídica formal, ainda pendente. |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 100% dos campos coletados (nome, e-mail, score, consentimento) com tratamento documentado e auditável — **atingido tecnicamente**; retenção de 12 meses, endpoint de exclusão e validação/registro de consentimento implementados e testados (Sprint 26) — revisão jurídica formal ainda pendente |
| Observações | Item mais crítico do backlog por envolver dado pessoal em empresa cujo produto é conformidade regulatória. **Sprint 25**: fluxo completo de PII documentado em `09-security.md` (seção "Backend `/api/diagnostico`"), com evidência de arquivo/linha em `tutela-api` (commit `23f0cb9`). Lacunas técnicas encontradas, sem correção nesta sessão por envolverem decisão de política de privacidade (aguardando decisão do responsável pelo projeto): (1) sem rotina de retenção/expurgo de `logs/leads.jsonl` — dados de lead retidos indefinidamente; (2) sem mecanismo técnico de exclusão/portabilidade específico para dados do formulário (só canal de contato genérico, herdado da política do produto de custódia); (3) consentimento é reforçado só no cliente — o servidor não recebe nem valida um campo de consentimento, então uma chamada direta à API (fora da UI) não deixa registro de consentimento; (4) a política de privacidade vinculada ao checkbox de consentimento não menciona o formulário de diagnóstico, os campos que ele coleta, nem os terceiros envolvidos (reCAPTCHA, Zoho/SMTP) — descreve apenas o produto de custódia de ativos digitais. Correção técnica de baixo risco aplicada: `requireTLS: true` no transporte SMTP (`tutela-api/server.js`), fechando uma janela de downgrade STARTTLS→texto-plano; commitada na branch `homolog` do `tutela-api`. **Correção da Sprint 26**: a nota anterior de que este commit estava "não publicado" estava desatualizada — confirmado nesta sprint (clone fresco de `github.com/cleberNetCenter/tutela-api`) que `requireTLS: true` já está presente em `main` e `homolog`, ambos idênticos (commit `1ba9548`). Achados incidentais fora do escopo de correção da Sprint 25: `req.ip` provavelmente captura o IP interno do proxy Nginx, não o IP público real do visitante (sem `trust proxy` configurado no Express) — afeta também a precisão do rate limiting; `fetch` do formulário não verifica status HTTP da resposta, então falhas do backend (incluindo o próprio `RECAPTCHA_SECRET` vazio em homologação) são exibidas ao usuário como sucesso — **nenhum dos dois corrigido na Sprint 26, fora do escopo desta sprint (decisões de política de privacidade), registrados aqui para sprint futura**. Recomendação explícita: os achados desta sprint devem ser revisados por profissional com competência jurídica em proteção de dados antes deste item ser considerado formalmente resolvido — esta auditoria é técnica, não uma determinação de conformidade. **Sprint 26 (2026-07-27) — implementação técnica das 3 decisões do responsável pelo projeto**: (1) *Retenção*: `tutela-api/lib/leadsStore.js` (`purgeOldLeads`) expurga entradas de `logs/leads.jsonl` com mais de 365 dias, com base no campo `data` (ISO 8601, já confirmado no formato existente); roda na inicialização do `server.js` e a cada 24h via `setInterval`; linhas malformadas são mantidas (não apagadas por ambiguidade) e contadas à parte; expurgo é logado em log de aplicação (stdout), nunca em `leads.jsonl`. Testado em `test/retention.test.js` (3 testes, timestamps fake antigos/recentes). (2) *Exclusão*: novo endpoint `DELETE /api/diagnostico/:email` em `server.js`, autenticado via `Authorization: Bearer <ADMIN_API_TOKEN>` (env var nova, documentada em `.env.example` novo — não existia antes desta sprint); comparação de e-mail normalizada (`toLowerCase().trim()`) para que a exclusão não falhe por diferença de caixa — decisão registrada aqui por não haver especificação prévia; resposta só traz `{removed: <contagem>}`, nunca os dados; ação logada (timestamp + contagem, sem o e-mail-alvo, para não recriar em log de aplicação o mesmo dado que a exclusão remove). Testado em `test/delete-endpoint.test.js` (5 testes: sem token, token errado, remoção normalizada, e-mail inválido, e-mail inexistente). (3) *Consentimento*: frontend (`tutela/public/assets/js/diagnostico.js`, função `enviar()`) passou a enviar o campo `consentimento` (checkbox já existente, só não estava no payload — achado original da Sprint 25); backend rejeita com `400` se ausente/falso e grava `consentGiven`/`consentTimestamp` junto com o lead. Testado em `test/consent.test.js` (3 testes). Testabilidade sem novas dependências de produção: `server.js` passou a exportar `app` e só chamar `app.listen`/agendar o expurgo quando executado diretamente (`require.main === module`); caminho do log configurável via `LEADS_FILE` (env var, default `logs/leads.jsonl`) para isolar arquivos de teste dos dados reais; testes usam `node --test` (nativo do Node 20, sem dependência nova) e `fetch` nativo para os testes de endpoint HTTP (sem `supertest`); captcha e envio de e-mail têm bypass restrito a `NODE_ENV=test` (captcha retorna `true` sem chamar o Google; SMTP usa `jsonTransport` nativo do `nodemailer` em vez de conectar no Zoho). `tutela-api`: 11/11 testes novos passando. `tutela`: `npm test` 90/92, mesmo baseline pré-existente da Sprint 25 (2 falhas de regressão visual não relacionadas a este item, ainda não investigadas). **Achado #4 (texto da política de privacidade)**: proposta de texto preparada e apresentada ao responsável pelo projeto, que a aprovou nesta mesma sprint (seguindo o mesmo padrão de decisões de conteúdo das Sprints 8/10/15) — publicada em `public/legal/politica-de-privacidade.html`: nova seção "3.1 Formulário de Diagnóstico de Risco" (campos coletados, reCAPTCHA e Zoho como terceiros) e complemento à seção 8 (retenção de 12 meses específica do formulário). `npm test`: 90/92, mesmo baseline (nenhuma regressão introduzida pela adição de conteúdo). **Deploy e validação em homologação (2026-07-27)**: `tutela` (`homolog.tuteladigital.com.br`) deployado automaticamente via `deploy-homolog.yml` (self-hosted runner) logo após o push, confirmado via `gh run list` (run concluída com sucesso). `tutela-api` **não tem pipeline de CI/CD** (gap já conhecido do `ARQ-507`) — código publicado em `origin/homolog`, deploy no servidor `tutela-dev` feito manualmente pelo responsável pelo projeto (`git reset --hard origin/homolog` + `docker compose build api && up -d api` em `/opt/tutela-v2/api`), incluindo geração de `ADMIN_API_TOKEN` (`openssl rand -hex 32`) e adição ao `.env` do servidor. Endpoint `DELETE /api/diagnostico/:email` validado ponta a ponta ao vivo em homologação: registro de teste inserido dentro do container (`docker compose exec api`, para evitar divergência entre o `logs/leads.jsonl` do host e o do container), `DELETE` autenticado retornou `{"removed":1}`, e o `cat` seguinte confirmou que só o registro-alvo foi removido, com os 2 registros pré-existentes intactos. **Produção (2026-07-27, sessão seguinte)**: `git log` no host `tutela-web` (`/opt/tutela-v2/api`) confirmou que produção ainda estava em `23f0cb9` (commit inicial, nem o `requireTLS` da Sprint 25 chegou a ir para produção antes disso) — os Blocos A/B/C desta sprint nunca tinham sido deployados lá. Atualizado com o mesmo processo manual de homologação: `git reset --hard origin/homolog` (→ `8f78cdd`) + `docker compose build api && up -d api`, `ADMIN_API_TOKEN` gerado (`openssl rand -hex 32`, valor distinto do de homologação) e adicionado ao `.env` de produção. Endpoint validado ao vivo em `www.tuteladigital.com.br`: primeira tentativa retornou o erro padrão do Express "Cannot DELETE" (código antigo, sem a rota, confirmando o diagnóstico do `git log` antes do reset); após o reset/rebuild, nova tentativa retornou `{"removed":0}` corretamente (e-mail de teste não existente, resposta idempotente esperada). `tutela-api` **agora está com o mesmo código (commit `8f78cdd`) e `ADMIN_API_TOKEN` configurado nos dois ambientes** — item de risco residual "produção pendente" fechado. **Sprint 29 (2026-07-29) — fechamento dos 3 achados incidentais represados desde a Sprint 26**: (1) *`nodemailer` CVE*: confirmado via `npm audit` que a versão instalada (`8.0.11`) é vulnerável a `GHSA-p6gq-j5cr-w38f` (CVSS 7.1, alta — a opção `raw` do `sendMail` contorna `disableFileAccess`/`disableUrlAccess`, permitindo leitura arbitrária de arquivo e SSRF); reconfirmado que não é explorável no código atual (`server.js` só usa `from`/`to`/`subject`/`text`, nunca `raw`) — a classificação da Sprint 24/25 ("não explorável, mas versão vulnerável instalada") segue válida. Changelog oficial do `nodemailer` (9.0.0–9.0.3) revisado: única mudança de comportamento é validação de certificado TLS por padrão em requisições HTTPS para conteúdo remoto (anexos via URL, endpoint OAuth2, proxy CONNECT) — nenhuma dessas trilhas é usada neste código, e `createTransport`/`sendMail`/`jsonTransport` não mudam de contrato. Atualizado para `9.0.3` (`npm audit` confirma 0 vulnerabilidades após o upgrade). Validação: sem credencial real do Zoho neste ambiente, então o handshake STARTTLS com `requireTLS: true` foi validado via `transporter.verify()` contra um servidor SMTP falso local (`test/smtp-tls.test.js`, 2 testes novos — confirma que a negociação STARTTLS funciona e que a proteção contra downgrade continua rejeitando conexão quando o servidor não oferece STARTTLS); recomenda-se validação manual do envio real em homologação antes do deploy. (2) *`trust proxy` ausente*: topologia real confirmada em `docs/ambientes-e-deploy.md` — produção tem 2 hops de proxy interno (Nginx do host, via `proxy_pass http://127.0.0.1:8080`, seguido do Nginx do container) até o Express; homologação tem 1 hop (Nginx do container publicado direto nas portas públicas). Como o número de hops difere entre os dois ambientes, um valor numérico fixo seria correto em um e errado no outro; todos os hops internos nos dois ambientes são loopback ou rede Docker (endereço privado, confirmado nos docs), então `app.set('trust proxy', ['loopback', 'linklocal', 'uniquelocal'])` (`tutela-api/server.js`) resolve corretamente os dois casos sem depender de `true` (que confiaria cegamente em qualquer proxy, inclusive um IP público falsificado em `X-Forwarded-For`, caso a topologia mude no futuro). Validado com 4 testes novos (`test/trust-proxy.test.js`) simulando as duas topologias via `X-Forwarded-For` e confirmando que `req.ip`/`logs/leads.jsonl` passam a refletir o IP real do cliente; validação manual adicional via `curl -H "X-Forwarded-For: ..."` contra uma instância real confirmou o mesmo. Rate limit (`express-rate-limit`) confirmado intacto e corretamente por IP real após a mudança (2 IPs simulados distintos mantêm cotas independentes, mesmo IP consome a mesma cota) — mesmo teste novo. (3) *`response.ok` não verificado*: confirmado em `tutela/public/assets/js/diagnostico.js` (`enviar()`) que o `fetch('/api/diagnostico', ...)` não checava `response.ok` — qualquer resposta HTTP (incluindo o `400` que a Sprint 26 passou a retornar para submissão sem consentimento) era tratada como sucesso, renderizando o card de resultado ao usuário mesmo em caso de falha do backend. Corrigido adicionando a checagem de `response.ok` antes de renderizar o resultado, reutilizando o mesmo padrão de UX de erro já existente na função (`alert()`, o mesmo já usado para falha de rede e validação incompleta) — nenhuma UI nova introduzida. Testado em `tests/diagnostico-form.spec.ts` (3 testes novos: sucesso 200 renderiza resultado; erro 400 e erro 500 não renderizam resultado e disparam o alerta) — confirmado por reversão temporária do fix que os 2 testes de erro falham com o código antigo (prova de que cobrem a regressão). `tutela-api`: `npm test` 17/17 (11 pré-existentes + 2 do item 1 + 4 do item 2). `tutela`: `npm test` 101/103, mesmo baseline pré-existente (2 falhas de regressão visual não relacionadas, mesmas da Sprint 28). **Deploy e validação ao vivo (2026-07-30)**: `tutela` mesclado via PR #191 (`homolog→main`), todos os checks de CI passaram, workflow `Deploy Produção` confirmado com sucesso — item 3 já está ao vivo em produção. `tutela-api`: **achado incidental adicional durante a validação do deploy**, fora do escopo original desta sprint — o repositório não tinha `.dockerignore`; o `Dockerfile` faz `COPY package.json .` + `RUN npm install` (corretamente instala a versão do `package.json`) seguido de `COPY . .`, que sem `.dockerignore` inclui o `node_modules/` local do host no contexto de build, sobrescrevendo o resultado do `npm install`. Confirmado ao vivo em homologação logo após o primeiro deploy do upgrade: o container reportava `nodemailer@8.0.4` — nem a versão antiga (`8.0.11`) nem a nova (`9.0.3`) — evidenciando que builds anteriores neste servidor podem não ter aplicado corretamente as dependências mesmo com build "verde". Corrigido com `.dockerignore` (`node_modules`, `logs`, `.env`, `.git`, commit `33b8f76`, PR #2). Deploy manual refeito nos dois servidores (`git reset --hard origin/homolog` + `rm -rf node_modules` local + `docker compose build --no-cache api && up -d api`, mesmo processo das sprints anteriores, já que `tutela-api` segue sem CI/CD, gap conhecido do `ARQ-507`): confirmado ao vivo em homologação e produção — `nodemailer@9.0.3`, `npm audit` = 0 vulnerabilidades nos dois ambientes; `trust proxy` validado por teste de rate-limit com `X-Forwarded-For` simulado via `curl` contra `/api/health` (IP simulado A decrementa cota 49→48 entre duas chamadas; IP simulado B começa com cota cheia, 49, independente de A) — confirmado idêntico em homologação (`homolog.tuteladigital.com.br`) e produção (`www.tuteladigital.com.br`, atrás do redirect 301 de barra final do Nginx de produção, seguido com `curl -L`). `origin/main` do `tutela-api` trazido à paridade com `origin/homolog` via PR #1 (nodemailer + trust proxy) e PR #2 (.dockerignore), mesclados pelo responsável pelo projeto. |

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
| Status | BACKLOG (confirmado ausente — Sprint 5/ARQ-108, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 violações de CSP reportadas no console em auditoria manual das 37 páginas |
| Observações | Recomenda-se modo `Content-Security-Policy-Report-Only` antes de aplicar em modo bloqueante. Escopo confirmado como puramente infraestrutural (fora deste repositório): ARQ-108 confirmou, via `nginx -T` na fonte, que CSP está ausente tanto em produção quanto em homologação, e a mudança é feita no Nginx dos servidores, não em código de aplicação — a única exceção seria a alternativa `<meta http-equiv>`, se a via Nginx não for escolhida. Evidência: `docs/ambientes-e-deploy.md`, seção "Auditoria externa (ARQ-108)". |

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
| Status | CONCLUÍDO (satisfeito por infraestrutura — confirmado na Sprint 5/ARQ-108, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Header presente em 100% das respostas — **atingido**: `X-Frame-Options: SAMEORIGIN` confirmado via `curl` externo e via `nginx -T` na fonte, em produção (host) e homologação (container), 2026-07-24. |
| Observações | Pode ser resolvido em conjunto com ARQ-102 (`frame-ancestors` no CSP substitui `X-Frame-Options`). Gerenciado no Nginx dos servidores, fora deste repositório Git (config não versionada, por decisão já documentada). Evidência: `docs/ambientes-e-deploy.md`, seção "Auditoria externa (ARQ-108)". Nenhuma ação de código necessária. |

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
| Status | CONCLUÍDO (satisfeito por infraestrutura — confirmado na Sprint 5/ARQ-108, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Header presente em 100% das respostas — **atingido**: `Referrer-Policy: strict-origin-when-cross-origin` confirmado via `curl` externo e via `nginx -T` na fonte, em produção (host) e homologação (container), 2026-07-24. |
| Observações | Gerenciado no Nginx dos servidores, fora deste repositório Git (config não versionada, por decisão já documentada). Evidência: `docs/ambientes-e-deploy.md`, seção "Auditoria externa (ARQ-108)". Nenhuma ação de código necessária. |

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
| Status | BACKLOG (confirmado ausente — Sprint 5/ARQ-108, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Header presente em 100% das respostas |
| Observações | Escopo confirmado como puramente infraestrutural (fora deste repositório): ARQ-108 confirmou, via `nginx -T` na fonte, que `Permissions-Policy` está ausente tanto em produção quanto em homologação; a mudança é feita no Nginx dos servidores, não em código de aplicação. Evidência: `docs/ambientes-e-deploy.md`, seção "Auditoria externa (ARQ-108)". |

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
| Status | CONCLUÍDO (Sprint 5, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 3/3 pontos cegos (headers, hostname homolog, redirects) documentados com evidência de config-fonte — **atingido, nos dois ambientes**. Pré-requisito original ("acesso de leitura à configuração Nginx de produção e homologação") — **atingido** (via `nginx -T` do host em produção e `docker exec ... nginx -T` do container em homologação). |
| Observações | Item de maior retorno/menor esforço do Épico 1 — confirmado nesta sprint, em três etapas. **Etapa 1** (`curl` externo, sem SSH): confirmou os 3 pontos cegos originais com evidência reproduzível de fora. **Etapa 2** (`sudo nginx -T` no host de produção, `tutela-web`): confirmou tudo da Etapa 1 na config-fonte e revelou a causa raiz exata do bug de redirect. **Etapa 3** (homologação, `tutela-dev`): o `nginx -T` do host inicialmente **não batia** com o `curl` (vhost errado — `www.tuteladigital.com.br` em vez de `homolog.tuteladigital.com.br`, HSTS presente na config mas ausente ao vivo). Investigação (`docker ps` + `ss -ltnp`) revelou que, em homologação, o Nginx público roda **dentro do container** `tutela_v2_nginx` (publicado direto nas portas 80/443 do host via `docker-proxy`) — o `/etc/nginx` do host existe mas está morto, sem porta pública, aparentemente cópia obsoleta da config de produção nunca ativada. `docker exec tutela_v2_nginx nginx -T` deu a config real, que bate exatamente com o `curl`. Ver `docs/ambientes-e-deploy.md`, seção "Nginx", para a tabela comparativa completa e os comandos/outputs de todas as etapas. **Achado estrutural**: produção e homologação não têm apenas hosts diferentes, têm **arquiteturas de Nginx diferentes** — produção usa Nginx de host fazendo proxy para o container; homologação usa o próprio container publicado direto nas portas públicas, sem Nginx de host envolvido. Resumo consolidado dos 3 pontos cegos: HSTS/X-Frame-Options/X-Content-Type-Options/Referrer-Policy ativos em produção, HSTS ausente em homologação; CSP e Permissions-Policy ausentes nos dois; hostname de homologação é `homolog.tuteladigital.com.br` (CNAME para `dev.tuteladigital.com.br`); os redirects de `_redirects`/`vercel.json` **nunca são lidos por nenhum dos dois Nginx** — ambos têm a mesma regra genérica quebrada para `.html`, e as 5 URLs legadas resultam em `404` nos dois ambientes (bug confirmado na config-fonte). Bônus não pedido no critério de aceite original, mas resolvido: paridade de `docker-compose.yml` confirmada como **ausente** por observação direta (`docker ps`) — produção roda `tutela_v2_nginx` + `tutela_v2_api`, homologação roda só `tutela_v2_nginx`; e um container `tutela_v2_api` (porta 3000, interna) foi descoberto em produção, possível pista para a implementação de `/api/diagnostico` (ARQ-101), não investigado por disciplina de escopo. **Anomalia de `http://tuteladigital.com.br/` (porta 80) redirecionando para a porta `:445`**: confirmado que não vem de nenhum dos dois Nginx da aplicação — é o firewall Fortinet que faz o acesso externo aos servidores. Causa provável, informada pelo usuário (**não verificada diretamente nesta auditoria**): a porta de administração web do Fortinet foi remapeada de 443 para 445 (o equipamento atende vários sites na 443, então a porta administrativa precisou ser movida), e a regra de redirect HTTP→HTTPS de `tuteladigital.com.br` aparenta herdar essa porta administrativa em vez da porta 443 real do site — um erro de configuração conhecido em FortiGate (o redirect automático referencia a variável de porta administrativa em vez da porta do VIP/serviço). Correção está fora do escopo deste repositório (requer acesso ao Fortinet) — fica registrado em `12-technical-debt.md` como pendência de infraestrutura, com a causa provável já documentada para quem for corrigir. Isso não bloqueia o fechamento deste item, que é sobre o Nginx da aplicação, não sobre o firewall de borda. Desbloqueia formalmente a decisão técnica de ARQ-102 (CSP — confirmado ausente nos dois ambientes), ARQ-104/ARQ-105 (confirmados já implantados em produção — avaliar se o critério de aceite desses itens já está satisfeito antes de reabrir trabalho), ARQ-106 (Permissions-Policy — confirmado ausente) e ARQ-403 (causa raiz do redirect quebrado confirmada na config-fonte, nos dois ambientes). Nenhum desses itens teve seu Status alterado nesta entrega — decisão e execução ficam para sprint futura, por disciplina de escopo (auditoria, não implementação). |

---

## Épico 2 — SEO (ARQ-2xx)

### ARQ-201 — Remover referências mortas a `og-image.jpg` e assets rasterizados equivalentes

| Campo | Valor |
|---|---|
| Objetivo | Eliminar previews de compartilhamento social quebrados (WhatsApp, LinkedIn, X, Facebook) causados por referências a imagens que nunca existiram no repositório. |
| Descrição | 15 páginas referenciavam `og-image.jpg`/variantes que nunca existiram no repositório. Investigação (Sprint 18) mudou o diagnóstico original: não é um asset pendente de arte, é herança de migração de um template anterior — o site não usa nenhuma imagem rasterizada de conteúdo por decisão de design (só CSS/SVG). Resolução: remover as referências, não aguardar uma arte que não vai ser produzida. |
| Origem | Débito técnico #1 |
| Documento | `07-seo.md`, `08-performance.md`, `12-technical-debt.md` |
| Item da dívida técnica | #1 |
| Arquivos afetados | 19 HTMLs (`og:image`/`twitter:image` removidos e/ou `twitter:card` rebaixado para `summary`) + 5 HTMLs do cluster `ativos-digitais/*` (`apple-touch-icon` corrigido para o asset real, `favicon.ico` removido) + 6 HTMLs (schema.org `logo` corrigido) — ver detalhamento completo em `12-technical-debt.md`, item #1 |
| Dependências (depende de) | Nenhuma — resolvido via remoção/correção de código, não depende de entrega externa |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Nenhuma página referencia asset de imagem ausente do repositório; guard-test `tests/dead-asset-references.spec.ts` passando |
| Critérios de Regressão | Nenhuma alteração visual/CSS — apenas metadata `<head>` e schema.org |
| Impacto | Alto (risco #1 do `EXECUTIVE_SUMMARY.md`) |
| Risco | Baixo |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Engenharia |
| Status | RESOLVIDO (Sprint 18, 2026-07-25) |
| ADR relacionado | Nenhum |
| Métrica de sucesso | 100% das páginas com Open Graph sem referência a imagem ausente; `tests/dead-asset-references.spec.ts` passando |
| Observações | Diagnóstico original (Sprints anteriores) presumia que o bloqueio era só entrega de arte pendente de design/conteúdo — a Sprint 18 confirmou que essa premissa estava errada: o site inteiro tem exatamente 3 `<img>` (bandeiras SVG do seletor de idioma) e nenhuma imagem de conteúdo rasterizada em lugar nenhum, então as referências a `.jpg`/`.png` eram resíduo de migração nunca finalizado, não trabalho pendente. A investigação também achou (mesma causa raiz) `apple-touch-icon.png` e `logo.png` (schema.org) quebrados no cluster `ativos-digitais/*`, corrigidos na mesma sprint. Se o site vier a adotar imagens de conteúdo no futuro (ex. og-image dedicado), é um item novo, não uma reabertura deste. |

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
| Status | CONCLUÍDO (Sprint 16, 2026-07-25) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 4/4 páginas do cluster validadas sem erro de hreflang no Google Search Console — reciprocidade formal (pré-condição desta métrica) confirmada localmente: 4/4 |
| Observações | Mapeamento via grep confirmou exatamente o que o débito técnico descrevia, sem divergência: as 3 páginas de idioma (`pt/ativos-digitais/`, `en/digital-assets/`, `es/activos-digitales/`) já declaravam um bloco `hreflang` completo e mutuamente idêntico (`pt-BR`→`/pt/ativos-digitais/`, `en`→`/en/digital-assets/`, `es`→`/es/activos-digitales/`, `x-default`→`/ativos-digitais/`); só `public/ativos-digitais/index.html` não declarava nenhum. Adicionado o mesmo bloco de 4 `<link rel="alternate" hreflang="...">` a essa página, na mesma posição relativa (logo após `canonical`, antes dos ícones) usada nas outras 3 — sem inventar formato novo. `x-default` aponta para a própria página (padrão já em uso, confirmado, não alterado). Criado `tests/hreflang-reciprocity.spec.ts` (5 testes: 4 verificam canonical + as 4 entradas hreflang esperadas por página, 1 verifica que as 4 páginas concordam byte-a-byte sobre o mapeamento hreflang→URL) como guard-test permanente contra regressão futura do cluster. `npm test`: 77/77 → 82/82 (5 novos). `contrast-audit.js`: 38/38, sem mudança (item é só metadado de `<head>`, não toca CSS). `tests/i18n-legal-notice.spec.ts`: 15/15, confirmando que `hreflang` (SEO) não interage com a lógica de troca de idioma via JS. Regressão visual (`visual-design-tokens.spec.ts`, `visual-radius-shadow.spec.ts`, cluster Ativos Digitais incluído) sem diff — confirmado, não presumido, que mudança de `<head>` não tem impacto visual. |

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
| Status | CONCLUÍDO (Sprint 17, 2026-07-25) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | `sitemap.xml` com contagem de `<url>` = contagem de `git ls-files public/**/*.html` (excluindo partials) — **atingido**: 37 = 37, confirmado item a item (não só por contagem), sem divergência. |
| Observações | **Não havia divergência real para corrigir.** Contagem de rotas reais hoje (`git ls-files`, exclui `public/partials/`, mesma lógica de `.github/workflows/sitemap.yml`): 37. Contagem de `<url>` em `public/sitemap.xml`: 37. Comparação item a item (não só numérica) entre as duas listas: **diff vazio** — as 37 URLs computadas a partir dos arquivos rastreados batem byte a byte com as 37 URLs do sitemap versionado. Investigação da origem do "35": a frase foi introduzida no commit `267f818` (2026-07-23, `docs: adiciona documentação de arquitetura e roadmap de evolução`); rodar o comando exatamente como documentado (`git ls-files public \| grep '\.html$' \| grep -v partials`) contra a árvore desse mesmo commit já retorna 37, não 35 — ou seja, não houve uma janela real em que a contagem fosse 35 seguida de crescimento para 37; foi um erro de contagem/transcrição no momento em que `04-routing.md` foi escrito, não um efeito de rotas criadas/removidas em sprints posteriores (Sprint 6 removeu CSS, não HTML; Sprint 11 corrigiu includes, não criou/removeu rotas). O stub de redirect puro identificado na Sprint 7 (`insights/ativos-digitais/o-que-sao-ativos-digitais/index.html`, sem header/nav) está presente e contado de forma consistente nos dois lados (é HTML rastreado fora de `partials/`, então conta como rota real pela própria definição do gerador, e aparece no sitemap) — não é fonte de divergência, confirmado, não presumido. Nenhuma URL fantasma no sitemap, nenhuma rota real faltando, nenhuma mudança na lógica do workflow gerador. Ação: corrigido apenas o número stale em `04-routing.md` (35→37) e criado `tests/sitemap-route-parity.spec.ts` (3 testes, guard-test permanente que replica a lógica exata do workflow gerador via `git ls-files` e compara contra `public/sitemap.xml` — falha se qualquer rota real ficar de fora do sitemap, qualquer URL do sitemap não corresponder a rota real, ou as contagens divergirem). `npm test`: 82/82 → 85/85 (3 novos), sem regressão. Nenhuma alteração em `.github/workflows/sitemap.yml` foi necessária. |

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
| Status | CONCLUÍDO (Sprint 11, 2026-07-24) |
| ADR relacionado | [ADR-0001](adr/0001-nomenclatura-ad-pillar.md) (Sprint 20) — decisão de nomenclatura (sub-extensão `--ad-pillar-*`) formalizada; também documentada como comentário em `tokens.css` |
| Métrica de sucesso | 0 ocorrências de `--ux-*` (hoje: 1 namespace inteiro) — **atingido**: confirmado via grep em todo `public/**/*.html` e `public/**/*.css`, 0 declarações e 0 usos remanescentes (a única ocorrência da string é um comentário histórico em `tokens.css` explicando a origem da migração). |
| Observações | **Escopo real, confirmado por grep antes de qualquer mudança**: `--ux-*` era consumido só pelo `<style>` inline do próprio `partials/ativos-digitais-pillar-styles.html` (nenhum outro arquivo do repositório referenciava `--ux-*`), e esse partial é incluído via SSI só em 3 páginas — `pt/ativos-digitais/`, `en/digital-assets/`, `es/activos-digitales/` (não em `public/ativos-digitais/index.html` nem nas páginas de pilar/insights, que usam `assets-digital.css`/`--ad-*` diretamente e têm sua própria classe `.assets-page` sem incluir o partial). Isso reduziu o raio de impacto real da migração a essas 3 páginas. Das 21 declarações originais em `--ux-*`, **6 nunca eram consumidas** (`--ux-surface`, `--ux-surface-2`, `--ux-line-strong`, `--ux-brand-glow`, `--ux-radius-lg`, `--ux-radius-md`) — confirmado via `grep -oE "var\\(--ux-[a-z0-9-]+\\)"` — e foram removidas sem substituto. Das 15 restantes, **4 tinham valor numérico idêntico** a um token `--ad-*` já existente e foram migradas diretamente: `--ux-accent`→`--ad-accent-gold`, `--ux-danger`→`--ad-danger`, `--ux-danger-bg`→`--ad-danger-bg`, `--ux-shadow-xs`→`--ad-shadow-xs`. As **11 restantes não tinham correspondência numérica em `--ad-*`** (confirmado par a par, não presumido — ver entrega da sprint para a tabela completa de valores antes/depois); para não introduzir uma mudança de marca perceptível não intencional (proibida pelo Critério de Regressão deste item) nem "inventar" um valor novo, cada uma foi trazida para `tokens.css` com o **mesmo valor exato**, sob uma sub-extensão nova `--ad-pillar-*` (`--ad-pillar-bg`, `--ad-pillar-ink`, `--ad-pillar-ink-soft`, `--ad-pillar-line`, `--ad-pillar-brand`, `--ad-pillar-brand-2`, `--ad-pillar-brand-3`, `--ad-pillar-max-width`, `--ad-pillar-radius-xl`, `--ad-pillar-shadow-sm`, `--ad-pillar-shadow-md`) — satisfaz o critério de aceite (fonte única, tudo `--ad-*`) sem regressão visual. Migração aplicada em 3 checkpoints (remoção dos 6 tokens mortos → migração dos 4 tokens de valor idêntico → criação dos 11 `--ad-pillar-*` e remoção do bloco `:root` inline), com `tests/visual-design-tokens.spec.ts` (novo, 24 baselines granulares por seção nas 3 páginas: hero, stats-grid, grid-2, steps, checklist, whitepaper-container, insight-cta, página completa) revisado a cada checkpoint — 0 diff em todos. `tests/support/contrast-audit.js` re-executado ao final: mesmos 38 pares, mesmas 2 falhas pré-existentes (ARQ-606, não relacionado). `npm test`: 26/26 → 50/50 (24 testes novos deste item), sem regressão. Retroativamente satisfaz a dependência que `ARQ-604` (Sprint 10) havia registrado como pendente — ver observação atualizada em ARQ-604. |

### ARQ-302 — Tokenizar breakpoints (`--breakpoint-*`)

| Campo | Valor |
|---|---|
| Objetivo | Substituir os 13 valores de `max-width` usados como números mágicos por uma escala de tokens compartilhada. |
| Descrição | 13 valores distintos (480px a 1200px) espalhados em `@media` queries sem token correspondente, com formatação inconsistente em alguns arquivos. |
| Origem | Débito técnico #10 |
| Documento | `06-design-system.md`, `12-technical-debt.md` |
| Item da dívida técnica | #10 |
| Arquivos afetados | `public/assets/css/foundation/tokens.css` + `assets-digital.css`, `diagnostico.css`, `homepage.css`, `insights-pilar.css`, `layout/layout.css`, `legal-shared.css`, `pages/como-funciona.css`, `pages/institucional.css`, `pages/pages-consolidated.css`, `pages/solucoes.css`, `sections/footer.css`, `sections/hero.css`, `sections/verticals.css`, `seguranca.css`, `styles-header-final.css`, `utilities/exec-compact.css` (16 arquivos) + `public/partials/ativos-digitais-pillar-styles.html` (17º arquivo, `<style>` inline — não estava na lista original; contém o 13º valor, `1180px`, e não fazia parte da varredura documentada quando este item foi catalogado) |
| Dependências (depende de) | ARQ-301 (evitar retrabalho), ARQ-501 (rede de segurança) |
| Dependências (desbloqueia) | Nenhuma diretamente; facilita ARQ-303/304 |
| Pré-requisitos | Playwright cobrindo responsividade nos breakpoints atuais antes da mudança |
| Critérios de Aceite | Todo `max-width` em `@media` referenciando um token `--breakpoint-*` — reinterpretado (ver Observações): não é possível referenciar via `var()` dentro da condição de `@media` em CSS puro (limitação de especificação, não de navegador-alvo), então o critério foi satisfeito como "toda ocorrência usa um valor da lista aprovada em `--breakpoint-*`, verificado automaticamente" |
| Critérios de Regressão | Responsividade idêntica testada em todos os 13 breakpoints originais, nas páginas de maior tráfego — **atingido**: diff de pixel exato (`maxDiffPixelRatio: 0`) via Playwright em 2 páginas × 4 viewports (767/769/1199/1201px, straddling os 2 valores cuja formatação mudou) antes/depois, 0 diferença |
| Impacto | Médio |
| Risco | Médio-Alto (maior superfície de arquivos tocados do backlog) — **risco real ficou muito abaixo do estimado**: a abordagem viável (ver Observações) não altera nenhum valor de `@media` existente, só formatação e documentação, então a "maior superfície de arquivos" do backlog acabou sendo a de menor risco de regressão visual real de todo o Épico 3 |
| Complexidade | Alta |
| Estimativa | G |
| Responsável | Frontend |
| Status | CONCLUÍDO (Sprint 12, 2026-07-24) |
| ADR relacionado | [ADR-0002](adr/0002-breakpoint-tokens-fora-de-media.md) (Sprint 20) — decisão técnica (tokens `--breakpoint-*` como constantes documentadas + guarda automatizada, não `var()` funcional dentro de `@media`) formalizada; também documentada como comentário em `tokens.css` |
| Métrica de sucesso | 0 valores `max-width` mágicos fora de token (hoje: 13) — **atingido**: os 13 valores reais (não uma escala genérica) estão declarados em `foundation/tokens.css` (`--breakpoint-480` a `--breakpoint-1200`, nomeados pelo valor literal); `tests/breakpoint-tokens.spec.ts` (novo) falha automaticamente se um 14º valor não aprovado aparecer em qualquer `@media (max-width: ...)` do repositório, ou se a formatação divergir do padrão — é o mecanismo real de "tokenização" possível neste stack (ver Observações) |
| Observações | **Decisão técnica principal, confirmada antes de qualquer alteração**: CSS não permite `var()` dentro da condição de `@media` (`@media (max-width: var(--breakpoint-768))` é inválido — limitação da própria especificação CSS, não de compatibilidade dos navegadores-alvo do projeto). `docs/architecture/02-stack.md` confirma que o projeto não usa pré-processador (sem Sass/Less/Stylus) nem build step para CSS (sem PostCSS/Tailwind) — logo `@custom-media` (que exigiria PostCSS) e qualquer alternativa baseada em build estão fora de escopo desta sprint por decisão de arquitetura de build, não de execução. A abordagem viável, adotada: (1) declarar os 13 valores reais como tokens `--breakpoint-<valor>` em `foundation/tokens.css`, nomeados pelo valor literal (não por escala `xs/sm/md/lg/xl` — 13 valores não se agrupam em 5-6 níveis semânticos sem comprimir valores distintos sob o mesmo nome; não havia convenção de nomenclatura numérica-por-valor pré-existente para reaproveitar, mas há precedente de tokens com sufixo numérico no arquivo, ex. `--primitive-green-990`); esses tokens são utilizáveis via `var()` em qualquer contexto que não seja a condição de `@media` (ex. `max-width` de container). (2) Como os valores em `@media` precisam continuar literais, `tests/breakpoint-tokens.spec.ts` (novo) lê as declarações `--breakpoint-*` de `tokens.css` como fonte única de verdade e varre todo `public/**/*.css` + `public/**/*.html` (não só os 16 arquivos CSS originalmente listados — foi assim que o 17º arquivo, `ativos-digitais-pillar-styles.html`, e o 13º valor, `1180px`, foram descobertos) validando que (a) todo `@media (max-width: Npx)` usa um dos 13 valores aprovados e (b) a formatação segue `@media (max-width: Npx) {` — isso substitui, de forma automatizada e permanente, o que seria a verificação manual do critério de aceite original. **Levantamento completo (grep, antes de qualquer mudança)**: 47 ocorrências totais, 13 valores distintos — `480px`×3, `540px`×1, `560px`×1, `600px`×8, `640px`×3, `720px`×4, `760px`×1, `768px`×16, `860px`×3, `900px`×3, `1024px`×2, `1180px`×1, `1200px`×1 (tabela completa por arquivo/linha na entrega da sprint). **Formatação**: só 3 das 47 ocorrências divergiam do padrão `@media (max-width: Npx) {` — `layout/layout.css:24,30` (`@media(max-width:1200px)`/`@media(max-width:768px)`, sem espaço nenhum) e `utilities/exec-compact.css:89` (`@media (max-width:768px){`, sem espaço após `:` nem antes de `{`) — corrigidas no mesmo commit (mesmo arquivo/superfície já tocada, disciplina da Sprint 6), sem tocar as 44 ocorrências restantes que já seguiam o padrão (não é o escopo mais amplo de ARQ-304, que continua BACKLOG — ver observação de ARQ-304). **Por que o risco real ficou baixo apesar da superfície de 17 arquivos**: como nenhum valor de `@media` foi alterado (só formatação, que não muda o valor computado da media query) e a adição em `tokens.css` é só de novas declarações `:root` não consumidas por nenhum seletor existente, não há mecanismo pelo qual essa mudança pudesse alterar renderização — confirmado, não presumido, via Playwright: 2 páginas (`/`, `/como-funciona.html`, ambas `body.exec-compact`, as únicas afetadas pelos 2 arquivos com formatação corrigida) × 4 viewports (767/769/1199/1201px, ladeando os 2 valores tocados) comparadas com `maxDiffPixelRatio: 0` antes/depois — 8/8 idênticas ao pixel. `npm test`: 68/68 (65 anteriores + 3 novos testes de `breakpoint-tokens.spec.ts`). **Estado confirmado de ARQ-303/304 antes de iniciar** (backlog listava os 4 itens do Épico 3 em sequência sugerida; Sprint 11 já pulou direto para ARQ-301 por risco/dependência real, não pela ordem numérica): ambos seguem `BACKLOG`, não bloqueiam nem são bloqueados por este item — ARQ-303 (tokens `--radius-*`/`--shadow-*`) é independente; ARQ-304 (formatação geral de `@media`, mais amplo que só os breakpoints) fica facilitado mas não é resolvido por completo aqui (só as 3 ocorrências que compartilhavam a superfície tocada). |

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
| Status | CONCLUÍDO (Sprint 13, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) — decisão de escopo (ver Observações) documentada como comentário em `tokens.css`, mesma disciplina de ARQ-301/ARQ-302 |
| Métrica de sucesso | Contagem de valores literais de `border-radius` fora de token = 0 — **atingido**: confirmado via `tests/radius-shadow-tokens.spec.ts` (novo), que varre `public/**/*.css` + `public/**/*.html` e falha se um literal aparecer fora de `var()`. `box-shadow`: não é 0 por decisão de escopo (ver Observações) — métrica redefinida para "nenhum literal duplica um valor já coberto por `--shadow-*`", também 0, mesmo guard-test. |
| Observações | **Escopo real, confirmado por grep antes de qualquer mudança**: a descrição original do item citava um único exemplo (`components/cards.css:13`) sugerindo escopo pequeno; o grep completo revelou 221 ocorrências de `border-radius` (~33 valores/padrões distintos) e 83+ declarações diretas de `box-shadow` (mais váraias multi-linha) em ~20 arquivos — superfície muito maior que a estimativa "M"/"Baixo risco" original, comparável ou maior que ARQ-302 ("G"). Como parte da superfície envolvia valores de `border-radius` visivelmente próximos (12px/13px/14px, 20/22/24/26px) e a maioria das sombras (`box-shadow`) é composta e única por marca/página (cor `rgba` própria de cada seção, não uma escala compartilhada) — decisão de design, não só técnica —, o escopo foi confirmado com o responsável pelo backlog antes de qualquer token ser criado (ver decisão registrada abaixo). **Confirmação técnica principal**: diferente de ARQ-302, `var()` funciona normalmente em `border-radius`/`box-shadow` fora de `@media` — confirmado não só por teste isolado, mas por evidência já viva no próprio repositório antes desta sprint: `--sol-r-*` (`solucoes.css`), `--hp-radius*` (`homepage.css`), `--sec-radius*` (`seguranca.css`), `--cf-radius*` (`como-funciona.css`), `--dg-shadow-*` (`diagnostico.css`), `--ad-radius-*`/`--ad-shadow-*` e `--ad-pillar-radius-xl`/`shadow-*` (Sprint 11) já usavam `var()` nessas propriedades em produção. Não há decisão de build step aqui — a migração é literal→`var()` direta. **Decisão de escopo confirmada** (sem consolidar valores próximos, um token por valor real, mesmo padrão de ARQ-302): (1) `--radius-*` — todos os 23 valores/formas reais distintos viraram token, nomeados pelo valor literal (`--radius-0` a `--radius-40`, mais `--radius-pill`/`--radius-full` para as formas "pílula"/circular); **100% das 224 ocorrências reais de `border-radius` do repositório foram migradas** para `var()` (221 do grep inicial em `assets/css/`+`partials/` + 3 descobertas depois em `public/legal/termos-de-uso.html`, um `<style>` inline que não fazia parte da varredura original — mesmo padrão de "17º arquivo" que ARQ-302 já havia encontrado). Combinações direcionais de canto (ex. `0 8px 8px 0`) foram compostas a partir dos tokens escalares via `var()` por canto, não geraram token dedicado. (2) `--shadow-*` — só os 7 valores de `box-shadow` **idênticos** (string exata, ignorando espaçamento) repetidos em 2+ arquivos viraram token global (`--shadow-neutral-sm`, `--shadow-black-md`, `--shadow-black-lg`, `--shadow-brand-md`, `--shadow-accent-glow`, `--shadow-brand-sm`, `--shadow-focus-ring`); as demais ~55 sombras (a maioria) são bespoke e permanecem literais — exceção deliberada, permitida pelo próprio critério de aceite ("exceto onde documentado como exceção deliberada"), documentada como comentário em `tokens.css`. Nenhum par "quase igual" foi fundido (ex. `diagnostico.css:916-918` vs. `1007-1009`, mesma forma, opacidade 0.18 vs. 0.16 — mantidos distintos). **Migração em 5 lotes** (mesma disciplina de ARQ-301/ARQ-302), com `npm test` + revisão de diff visual a cada lote: legal (`legal-shared.css`) → Insights (`insights-pilar.css`) → cluster Ativos Digitais (`assets-digital.css` + `partials/ativos-digitais-pillar-styles.html`) → cluster Home (`homepage.css`, `sections/*.css`, `components/*.css`, `styles-header-final.css`, `legacy.css`) → demais páginas (`diagnostico.css`, `solucoes.css`, `seguranca.css`, `como-funciona.css`, `institucional.css`, `pages-consolidated.css`, `dark-editorial-shared.css`) + `public/legal/termos-de-uso.html` (achado tardio). **Incidente durante a migração, corrigido no mesmo lote**: o script de migração (regex Python) normalizou involuntariamente terminadores de linha CRLF→LF em 6 arquivos que usavam CRLF no repositório (`homepage.css`, `legacy.css`, `pages-consolidated.css`, `steps.css`, `verticals.css`, `components/buttons.css`), inflando o diff de cada um para milhares de linhas "alteradas" sem nenhuma mudança de conteúdo real — identificado pelo `git diff --stat` (tamanho de diff incompatível com o nº de declarações tocadas) antes de qualquer commit, corrigido restaurando CRLF nos 6 arquivos (conteúdo migrado preservado). **Achado fora do escopo original do grep**: `public/assets/js/i18n.js:155,163` tem um `border-radius`/`box-shadow` literal embutido em uma string de template JS (banner de fallback com paleta própria, `#ffc107`/`#007bff`, sem relação com os tokens de marca do site) — não migrado nesta sprint por ser JS (não CSS) e por sua paleta sugerir que não pertence ao sistema de design compartilhado; registrado aqui como lacuna conhecida, não escondida, para decisão futura (possível novo item de backlog, não ARQ-303). **Regra de evidência por token/migração** (tabela completa de arquivo/linha/contagem na entrega da Sprint 13 — não duplicada aqui por volume): cada um dos 23 tokens `--radius-*` e 7 `--shadow-*` foi confirmado por grep antes/depois (contagem de ocorrências) e por comparação de `getComputedStyle` via Playwright antes/depois (não só diff de screenshot) em elementos reais das páginas afetadas — 0 divergência em toda a migração. **Cobertura de regressão visual**: `tests/visual-radius-shadow.spec.ts` (novo, mesmo padrão de `tests/visual-contrast.spec.ts`/ARQ-604) — 4 baselines full-page (home, cluster Ativos Digitais, legal/termos-de-uso, Insights hub), geradas ANTES da migração e comparadas a cada lote (`maxDiffPixelRatio: 0.005`, mesma tolerância de ARQ-604 para o artefato conhecido de costura de screenshot do Chromium) — 0 diff fora do ruído conhecido em todos os checkpoints. As 24 baselines granulares de `tests/visual-design-tokens.spec.ts` (ARQ-301) também foram re-executadas no lote do cluster Ativos Digitais como cobertura extra — 0 diff. **Páginas fora dos 4 clusters de baseline** (`diagnostico.html`, `seguranca.html`, `como-funciona.html`, `governo.html`/`empresas.html`/`pessoas.html`, `legal/institucional.html`) não ganharam screenshot de baseline nesta sprint (escopo do item limitado aos 4 clusters nomeados) — verificadas em vez disso por comparação de `getComputedStyle` (`border-radius`/`box-shadow` computados) via Playwright em todos os elementos `button`/`.btn`/`.card` de cada página, comparando o estado migrado contra o estado revertido via `git stash` — 0 divergência nas 5 páginas (único falso-positivo do processo, causado pelo próprio método de verificação — `tokens.css` revertido isoladamente enquanto `buttons.css` já migrado ficou referenciando um token temporariamente inexistente, resolvendo para o valor inicial `0` — não uma regressão real; identificado e descartado refazendo a comparação com reversão completa e consistente). `tests/radius-shadow-tokens.spec.ts` (novo, mesmo padrão de `tests/breakpoint-tokens.spec.ts`/ARQ-302) — guarda contra drift futuro: (1) nenhum `border-radius` literal fora de `var()` sobrevive em `public/**/*.css`/`*.html`; (2) nenhum `box-shadow` literal duplica exatamente um valor já coberto por `--shadow-*` (previne reintrodução de uma sombra compartilhada como literal). `npm test`: 68/68 → 76/76 (8 testes novos: 4 de `visual-radius-shadow.spec.ts` + 4 de `radius-shadow-tokens.spec.ts`), sem regressão. Retroativamente, ARQ-301 e ARQ-302 continuam satisfeitos (nenhum token/breakpoint anterior foi tocado). Facilita ARQ-304 (formatação de `@media`, único item restante do Épico 3) por não compartilhar arquivos-alvo em conflito. |

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
| Status | CONCLUÍDO (Sprint 14, 2026-07-25) |
| ADR relacionado | Nenhum (não necessário — mudança puramente sintática, sem decisão de arquitetura) |
| Métrica de sucesso | 0 inconsistências de formatação em `@media` no repositório — **atingido**: confirmado via grep exaustivo, 0 ocorrências não conformes encontradas; guarda automatizado (`tests/media-formatting.spec.ts`) substitui o lint de CSS citado no critério de aceite original, já que o projeto não roda Stylelint (sem build step, `02-stack.md`) |
| Observações | **Achado principal desta sprint: ARQ-304 já estava 100% resolvido antes de qualquer alteração de código** — não por este item ter sido executado, mas como efeito colateral já registrado nas Observações de ARQ-302 (Sprint 12, que corrigiu as 3 únicas ocorrências não conformes do repositório: `layout/layout.css:24,30` e `utilities/exec-compact.css:89`) e ARQ-303 (Sprint 13, que não introduziu nenhuma ocorrência nova de `@media`). **Confirmado por grep exaustivo (antes de qualquer mudança)**: `grep -rnE "@media\s*\(.*\)\s*\{" --include=*.css --include=*.html public/` → 56 declarações reais de `@media` (47 `max-width` + 9 `prefers-reduced-motion`) em 22 arquivos (20 `.css` + 2 `.html` com `<style>` inline — `legal/termos-de-uso.html`, `partials/ativos-digitais-pillar-styles.html`) — todas já no padrão `@media (feature: valor) {` (espaço após `@media`, após `:`, antes de `{`). Greps negativos direcionados (`@media\(` sem espaço, `:[0-9]` sem espaço após `:`, ausência de espaço antes de `{`) — 0 ocorrências em todos. Nenhum arquivo alterado; nenhuma mudança de código necessária. **Trabalho real desta sprint**: `tests/breakpoint-tokens.spec.ts` (ARQ-302) já guarda a formatação, mas só para `@media (max-width: ...)` especificamente; como a descrição de ARQ-304 é mais ampla (qualquer `@media`, qualquer media feature — confirmado nas Observações de ARQ-303: "formatação geral de `@media`, mais amplo que só os breakpoints"), as 9 ocorrências de `@media (prefers-reduced-motion: reduce)` ficavam conformes mas sem guarda contra regressão futura. Criado `tests/media-formatting.spec.ts` (novo, mesmo padrão de `breakpoint-tokens.spec.ts`/`radius-shadow-tokens.spec.ts`), cobrindo todas as 56 ocorrências reais (não duplica o guard-test existente — este é mais amplo, aquele é mais específico sobre valores aprovados de breakpoint). `npm test`: 76/76 → 77/77 (1 teste novo), sem regressão — suíte de regressão visual existente (`visual-contrast`, `visual-design-tokens`, `visual-radius-shadow`) re-executada por completo, 0 diff (esperado, já que nenhum CSS foi tocado). **Épico 3 (Design System) fechado por completo nesta sprint**: `ARQ-301`, `ARQ-302`, `ARQ-303` e `ARQ-304` todos `CONCLUÍDO`. |

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
| Risco | Baixo (reclassificado de Médio na Sprint 6, 2026-07-24 — ver Observações) |
| Complexidade | Baixa |
| Estimativa | P-M |
| Responsável | DevOps |
| Status | CONCLUÍDO (Sprint 6, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Teste de todas as URLs legadas retornando 301 correto após a consolidação — **não aplicável**: a auditoria (ARQ-108) revelou que as 5 URLs legadas já retornam `404` hoje, nos dois ambientes, independentemente destes arquivos (nunca foram a fonte ativa). A métrica realmente atingida é: 0 arquivos de redirect inertes no repositório, confirmado por grep e por `npm test` (7/7, sem regressão). |
| Observações | Desbloqueado e concluído com base em ARQ-108 (Sprint 5). O risco original ("remover sem confirmar pode quebrar redirects se, inesperadamente, algo depender do arquivo") não se sustentava mais: `nginx -T` na fonte (produção e homologação) confirmou que nenhum dos dois Nginx lê `_redirects`/`vercel.json` — a normalização de URL é feita por uma regra genérica do Nginx, não por esses arquivos (ver `docs/ambientes-e-deploy.md`, seção "Auditoria externa (ARQ-108)"). Confirmado adicionalmente por grep em todo o repositório (incluindo `.github/workflows/`): nenhuma referência funcional, só documentação. `public/_redirects` e `public/vercel.json` removidos nesta sprint (`git rm`); `npm test` permaneceu 7/7 após a remoção. O bug das 5 URLs legadas (404) é uma pendência de infraestrutura separada, documentada em `12-technical-debt.md` e fora do escopo desta remoção. |

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
| Status | CONCLUÍDO (Sprint 2, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 requisições HTTP para CSS vazio (hoje: 21) |
| Observações | Removido em Sprint 2. A dependência declarada de ARQ-301 foi reavaliada com evidência direta, não descartada por suposição: os 6 arquivos continham exatamente 1 linha (comentário de descontinuação, 0 regras CSS) — confirmado via leitura integral de cada arquivo antes da remoção. `pages/ativos-digitais-pillar-styles.css` já não tinha nenhum `<link>` apontando para ele (órfão total). Os outros 5 são substituídos por `styles-header-final.css` (dropdown, confirmado presente em 100% das 21 páginas que linkavam `dropdown-menu.css`) e `legal-shared.css` (páginas legais, confirmado presente nas 4 páginas com CSS individual). Removidos: 6 arquivos CSS + 25 `<link>` em 24 páginas HTML (21× `dropdown-menu.css`, 1× cada dos 4 CSS individuais de página legal). Validação: grep completo confirma 0 referências remanescentes; `<head>` balanceado nos 27 arquivos tocados (inclui também ARQ-503, mesmo commit); servidor local confirma páginas servindo 200 e o CSS removido servindo 404. |

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
| Status | CONCLUÍDO (Sprint 4, 2026-07-23) |
| ADR relacionado | Nenhum |
| Métrica de sucesso | 0 duplicação de lógica de dropdown entre arquivos; nome do arquivo corresponde à responsabilidade documentada em `05-components.md` |
| Observações | Item adicionado nesta revisão — ausente do roadmap original (`15-architecture-roadmap.md`), ver F1-1. Resolvido em Sprint 4: leitura integral de ambos os arquivos confirmou exatamente o que o débito técnico descrevia — `mobile-menu.js` (118 linhas) é o controlador real de toda a navegação (dropdowns desktop via hover/clique, menu mobile, estado ativo de link, troca de idioma, borda do header no scroll); `dropdown-menu.js` (13 linhas) não continha nenhuma lógica de dropdown, apenas um guard que emite `console.warn` caso o outro script não tenha rodado antes. `mobile-menu.js` renomeado para `navigation-menu.js` (nome alinhado ao próprio identificador interno `__tutelaNavigationControllerInitialized`); `dropdown-menu.js` removido (não fundido) — decisão justificada por não implementar nenhuma lógica própria, seu único efeito (o `console.warn`) nunca dispara em produção porque `scripts.html` sempre carregava os dois scripts `defer` na mesma ordem do documento, e sua própria remoção é o que elimina a confusão de nomenclatura relatada no débito técnico (um desenvolvedor que procurasse lógica de dropdown em `dropdown-menu.js` não a encontraria de qualquer forma). Nenhuma duplicação de lógica foi criada. Atualizado `public/partials/scripts.html` (2 tags `<script>` → 1, apontando para `navigation-menu.js`) e o comentário (não-funcional) em `tests/navigation.spec.ts:5` que citava o nome antigo do arquivo. Validação: baseline de 7/7 testes confirmado antes da mudança; 7/7 idêntico depois, sem alterar nenhuma asserção de teste; servidor local (`tests/support/ssi-server.js`) confirma `200` em `/assets/js/navigation-menu.js`, `404` em `/assets/js/mobile-menu.js` e `404` em `/assets/js/dropdown-menu.js`. Nenhum outro ponto do repositório (grep exaustivo, todos os tipos de arquivo, excluindo `docs/`) referenciava os nomes antigos. Documentos da baseline arquitetural (`03-folder-structure.md`, `05-components.md`, `08-performance.md`, `12-technical-debt.md`) não foram alterados, seguindo o mesmo precedente das Sprints 1–3 (esses documentos já mantinham referências desatualizadas a `navigation.js`, removido na Sprint 1, sem terem sido corrigidos retroativamente) — apenas este backlog operacional é atualizado por sprint. |

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

### ARQ-407 — Remover `<link>` órfão para `pages/termos-de-uso.css`

| Campo | Valor |
|---|---|
| Objetivo | Eliminar uma requisição HTTP que nunca teve chance de retornar 200. |
| Descrição | `legal/termos-de-uso.html` referencia `/assets/css/pages/termos-de-uso.css`, arquivo que nunca existiu no histórico do repositório (confirmado via `git log --all --diff-filter=A` e `git log --all -S`, sem nenhum commit de criação do arquivo). Achado sinalizado na Sprint 19 (ARQ-502) e catalogado em `KNOWN_DEAD_ASSETS` (`tests/support/asset-versions.js`) para não mascarar o guard-test de cache-busting enquanto não resolvido. Caso distinto de ARQ-404: lá os 6 arquivos existiam e foram esvaziados; aqui o arquivo nunca existiu. |
| Origem | Achado da Sprint 19, sinalizado como candidato a item novo (não coberto por ARQ-502, que trata de convenção de versionamento, não de assets ausentes) |
| Documento | Nenhum específico — achado operacional, não dívida técnica catalogada em `12-technical-debt.md` |
| Item da dívida técnica | Nenhum |
| Arquivos afetados | `public/legal/termos-de-uso.html` (remoção do `<link>`), `tests/support/asset-versions.js` (remoção da entrada de `KNOWN_DEAD_ASSETS`) |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | `<link>` removido de `legal/termos-de-uso.html`; `KNOWN_DEAD_ASSETS` sem a entrada de `termos-de-uso.css`; guard-test de cache-busting volta a cobrir esse caminho sem exceção |
| Critérios de Regressão | Nenhuma mudança visual em `legal/termos-de-uso.html` (o CSS nunca carregou, então nunca aplicou estilo) |
| Impacto | Baixo (performance marginal — 1 requisição 404 a menos) |
| Risco | Baixo (remoção de referência morta, mesma categoria de ARQ-401/ARQ-402/ARQ-404) |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | Frontend |
| Status | CONCLUÍDO (Sprint 21, 2026-07-26) |
| ADR relacionado | Nenhum |
| Métrica de sucesso | 0 requisições 404 para `pages/termos-de-uso.css`; 0 exceções em `KNOWN_DEAD_ASSETS` |
| Observações | Confirmado que o arquivo nunca existiu (`git log --all --diff-filter=A -- "**/termos-de-uso.css"` sem resultado; `git log --all -S"termos-de-uso.css"` só retorna commits que tocaram o `<link>`/comentário dentro de outros arquivos, nenhum de criação do CSS). Confirmado que é caso isolado: nenhuma outra página legal (`politica-de-privacidade.html`, `termos-de-custodia.html`, `institucional.html`) tem referência equivalente quebrada — `institucional.html` referencia `pages/institucional.css`, que existe. `npm test` 92/92 antes e depois, sem alteração de asserção nos testes visuais (`visual-contrast.spec.ts`, `visual-radius-shadow.spec.ts` já cobriam a página `termos-de-uso` e passaram sem regenerar snapshot). |

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
| Status | CONCLUÍDO (Sprint 3, 2026-07-23) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Cobertura Playwright ≥ 3 fluxos críticos rodando em CI a cada PR |
| Observações | **Deve ser o primeiro item do backlog a ser executado**, antes de qualquer item com risco Médio ou superior (ver Fase 4 do documento de validação do roadmap). Apesar de estar numerado no Épico 5, sua execução não deve esperar o Épico 5 começar. Concluído em Sprint 3: `package.json`/`package-lock.json` versionados (antes só existiam na árvore de trabalho); `playwright.config.ts` criado, com projeto único `chromium`. Achado que exigiu decisão explícita (não presumida): `python3 -m http.server`, único servidor local documentado em `13-development-workflow.md`, não resolve os `<!--#include virtual="..." -->` (SSI) usados por 100% das páginas para montar header/footer/scripts — serviria o comentário cru em vez do menu/nav real, e `nginx` não está disponível neste ambiente. Decisão tomada com o responsável: criar `tests/support/ssi-server.js`, servidor Node só para os testes (módulos nativos `http`/`fs`, nenhuma dependência nova), que resolve os includes por substituição de texto, espelhando o que o Nginx já faz em produção/homologação — nenhum arquivo de `public/` foi alterado. Suíte cobre 7 smoke tests em 4 arquivos: `home.spec.ts` (home carrega, 0 erros de console, 0 404 em assets locais), `navigation.spec.ts` (dropdown de desktop abre no hover e fecha com Escape; dropdown alterna com clique direto isolado do hover; menu mobile abre/fecha), `regression-sprints.spec.ts` (página legal `termos-de-uso.html` sem `<link>` para os 6 CSS deprecated removidos em ARQ-404 e com `styles-header-final.css`/`legal-shared.css` presentes; exatamente 1 par de preconnect de fontes injetado, regressão direta de ARQ-503; `I18N.isLegalPage()` retorna `true` numa página legal e `false` na home, regressão direta da simplificação de ARQ-402). Não cobre: submissão do formulário de diagnóstico (endpoint `/api/diagnostico` não implementado neste repositório, ver ARQ-101) nem troca de idioma via `switchLanguage()` — ambos fora do escopo mínimo desta entrega, não bloqueiam nenhum item desbloqueado por ARQ-501. CI (execução automática a cada PR, exigida pelo critério de aceite original) **não foi configurado nesta entrega**, deliberadamente adiado para ARQ-504, conforme instrução explícita desta sprint — dívida técnica registrada aqui, não escondida: até ARQ-504, a suíte roda apenas localmente via `npm test`. Validação: suíte executada localmente 3x (1x isolada, 2x com `--repeat-each=2`, total 21 execuções de teste) — 100% de sucesso, 0 flakiness observada. |

### ARQ-502 — Unificar esquema de cache-busting

| Campo | Valor |
|---|---|
| Objetivo | Eliminar o risco de cache desatualizado por convenção de versionamento inconsistente. |
| Descrição | Três esquemas convivem hoje: contador simples (`main.css?v=7`), data `AAAAMMDDNN` (`i18n.js?v=2026041001`) e contador por arquivo (`lang/pt.json?v=10`). Definir e aplicar uma única convenção. |
| Origem | Débito técnico #12 |
| Documento | `08-performance.md`, `12-technical-debt.md` |
| Item da dívida técnica | #12 |
| Arquivos afetados | Todos os `<link>`/`<script>` com `?v=` nas 37+ páginas (113 ocorrências, 22 assets distintos); `main.css`, `styles-header-final.css`, `homepage.css`, `legal-shared.css`, `seguranca.css`, `assets-digital.css`, `insights-pilar.css`, `diagnostico.css`, `pages/{solucoes,arquitetura-juridica-prova-digital,ativos-digitais,como-funciona,institucional,termos-de-uso}.css`, `i18n.js`, `navigation-menu.js`, `search.js`, `legal-animations.js`, `search-index.json`, `lang/{pt,en,es}.json` (a referência original a `mobile-menu.js` estava desatualizada — o arquivo real, incluído via `partials/scripts.html`, é `navigation-menu.js`) |
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
| Status | CONCLUÍDO (Sprint 19, 2026-07-25) |
| ADR relacionado | [ADR-0003](adr/0003-convencao-cache-busting.md) (Sprint 20) — decisão de convenção (contador incremental único + guard-test de hash, não hash de conteúdo automatizado nem data única) formalizada; também documentada como comentário em `tests/support/asset-versions.js` |
| Métrica de sucesso | 0 arquivos fora da convenção única (hoje: 3 esquemas distintos) — **atingido**: 21 assets versionados, todos com contador inteiro simples (1-4 dígitos), 1 único valor por arquivo em todo o site, verificado automaticamente por `tests/cache-busting.spec.ts` |
| Observações | **Convenção escolhida, confirmada com o usuário antes da migração em massa** (das 3 opções levantadas): contador incremental único por arquivo, mantido manualmente, com um manifesto (`tests/support/asset-versions.json`) registrando `{versão, hash de conteúdo}` de cada asset — um guard-test (`tests/cache-busting.spec.ts`) falha se o hash do arquivo no disco divergir do hash registrado, pegando exatamente o cenário que o Risco Médio deste item descrevia (esquecer de incrementar o `?v=` ao editar o arquivo). Alternativas descartadas: hash de conteúdo calculado por script (mais robusto, mas exigiria um passo novo no pipeline de deploy que hoje não existe — fora de escopo desta sprint, confirmado em `docs/architecture/11-build-deploy.md`, "Não há build"); data única `AAAAMMDDNN` (padroniza o formato mas não prevendo cache stale sozinha, exigiria o mesmo guard-test de hash por cima mesmo assim). **Levantamento completo (grep, antes de qualquer mudança)**: 113 ocorrências de `?v=` em 40 arquivos, mapeadas a 22 assets fisicamente distintos (21 existentes + 1 já ausente do disco antes desta sprint, ver abaixo). **Dois bugs reais de convenção, encontrados pelo próprio levantamento e corrigidos nesta migração** (evidência de por que a unificação importa, não só higiene): `assets-digital.css` era referenciado como `?v=2` em 10 páginas e `?v=7` em 5 — unificado para `?v=8`; `insights-pilar.css` era `?v=1` em 1 página e `?v=2` em 2 — unificado para `?v=3`. Um terceiro caso, mais brando: `legal/institucional.html` usava `institucional.css?v=5`, mas o comentário de cabeçalho do próprio arquivo já documentava `Versão: 6` (e citava um `dropdown-menu.css` que não existe mais) — alinhado para `?v=6` e o comentário corrigido (`main.css`/`styles-header-final.css` no comentário também estavam desatualizados em `?v=4`, código real já usava `?v=7`). **Migração em 3 lotes, `npm test` a cada um, sem regressão em nenhum**: lote CSS (unificação dos 2 arquivos divergentes + `diagnostico.css` convertido de `?v=202604041755` para `?v=1`) → 87/87; lote JS (`i18n.js`, `navigation-menu.js`, `search.js` — só 1 edição cada, já que os 3 são incluídos via `partials/scripts.html`, SSI — e `legal-animations.js`, 7 páginas, convertidos de data para `?v=1`) → 88/88; JSON (`search-index.json?v=2` e `lang/{pt,en,es}.json?v=10`, referenciados como literal dentro de `fetch()` em `search.js`/`i18n.js`, não em atributo `href`/`src`) já estavam no formato de contador — nenhuma edição de valor necessária, só registro no manifesto. **Achado incidental, fora de escopo, sinalizado e não corrigido nesta sprint** (disciplina de escopo, mesmo padrão de ARQ-201): `legal/termos-de-uso.html` referencia `/assets/css/pages/termos-de-uso.css`, que nunca existiu no histórico do repositório (`git log` vazio para o caminho) — 404 confirmado antes e depois desta migração, comportamento inalterado. Catalogado explicitamente como `KNOWN_DEAD_ASSETS` em `tests/support/asset-versions.js` (excluído do manifesto de hash, mas ainda coberto pelos testes de formato/consistência de versão) para não mascarar uma futura reintrodução de asset morto — um guard-test novo (`tests/cache-busting.spec.ts`, "nenhum asset referenciado deixa de existir no disco...") falha se qualquer OUTRO asset versionado ficar ausente do disco sem estar nessa lista. Candidato a item futuro (ex. sob o mesmo padrão de ARQ-201/dead-asset-references, mas para CSS em vez de imagem), não aberto nesta sprint por disciplina de escopo. **Validação de carregamento real** via `npm run dev` (porta 8081, não `python3 -m http.server`): todas as 21 URLs versionadas retornam HTTP 200 (`curl`), testado isoladamente por asset e por página completa (5 páginas representativas de cada lote — `legal/institucional.html`, `legal/termos-de-uso.html`, `insights/prova-digital/index.html`, `en/digital-assets/`, `diagnostico.html` — todo `href`/`src` com `?v=` extraído do HTML servido via SSI e verificado individualmente); o único 404 (`termos-de-uso.css`) é o mesmo de antes da migração, confirmado. `npm test`: 86/86 → 92/92 (6 novos testes de `tests/cache-busting.spec.ts`); 1 flake pontual em `visual-design-tokens.spec.ts` (não relacionado — teste de regressão visual do ARQ-301 já existente, passou isoladamente e na re-execução completa). Script `tests/support/generate-asset-versions.js` criado para o dev regenerar o manifesto após um bump manual futuro (recalcula hash, falha se encontrar versões divergentes para o mesmo arquivo antes de escrever). |

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
| Status | CONCLUÍDO (Sprint 2, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 1 par de preconnect por página (hoje: 2) |
| Observações | Item novo, adicionado pela revisão arquitetural do roadmap. Escopo real era maior do que o inicialmente descrito: 22 páginas tinham preconnect estático próprio (não só `index.html`), todas duplicando o par injetado incondicionalmente por `partials/header.html` (o guard `global-fonts-loaded` só evita reinjeção do próprio script, não detecta o `<link>` estático já presente). Removidos os 44 `<link rel="preconnect">` estáticos das 22 páginas; `partials/header.html` **não foi alterado** — continua sendo a única fonte do preconnect, agora sem duplicação, para 100% das páginas via SSI. Trade-off registrado: o preconnect passa a depender da execução do script inline no `<header>` em vez de uma tag estática no `<head>`; como o script roda de forma síncrona logo no início do `<body>`, o atraso é mínimo e não haveria ganho real em manter a duplicação. Validado nas 22 páginas via grep e servidor local. |

### ARQ-504 — Automatizar checklist de publicação em CI (lint, `git diff --check`)

| Campo | Valor |
|---|---|
| Objetivo | Substituir a validação manual do checklist de publicação por um gate automatizado em CI. |
| Descrição | O runbook já define um checklist manual (`docs/ambientes-e-deploy.md:42-47`): testar URLs, conferir redirecionamentos, validar chaves de idioma, rodar `git diff --check`. Automatizar o que for possível como workflow de CI. |
| Origem | 13-development-workflow.md |
| Documento | `13-development-workflow.md`, `12-technical-debt.md` |
| Item da dívida técnica | N/A — decorre do Épico 5 do roadmap ("Validações", "Lint"), sem item numerado específico em `12-technical-debt.md` |
| Arquivos afetados | `.github/workflows/guard-main-requires-homolog.yml` |
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
| Status | CONCLUÍDO (Sprint 22, 2026-07-26) |
| ADR relacionado | Nenhum (a criar em ARQ-701) — mudança tratada como aditiva/rotina de CI, não como decisão arquitetural |
| Métrica de sucesso | 100% dos itens automatizáveis do checklist do runbook rodando em CI — **atingido para os 2 itens automatizáveis** (`npm test`, `git diff --check`); os 2 itens restantes do checklist (testar URLs afetadas em desktop/mobile, validar chaves de idioma) permanecem manuais — ver Observações. |
| Observações | **Topologia de CI confirmada antes de qualquer mudança** (lida direto de `.github/workflows/*.yml`, não presumida a partir de `11-build-deploy.md`): `deploy-homolog.yml`/`deploy-prod.yml` disparam em `push` para `homolog`/`main` e fazem só `git reset --hard` + `docker compose up`, sem qualquer validação — não tocados nesta sprint, por instrução explícita. `sitemap.yml` dispara em `push` para `main`/`homolog`/`feature/legal-structure`, gera `sitemap.xml`, comita e sincroniza `main→homolog` — também não tocado. `guard-main-requires-homolog.yml` já existia como o único workflow de `pull_request` do repositório (`branches: [main]`), com um job (`check-homolog-ancestor`) que barra PRs para `main` cujo commit ainda não passou por `homolog` — infraestrutura de validação de PR pré-existente, então a regra "estender workflow existente" da sprint se aplicou diretamente, sem precisar decidir sobre topologia nova. **Lint**: confirmado em `package.json` (só `@playwright/test` como devDependency, sem `eslint`/`stylelint`/`prettier`) e em `10-dependencies.md` que nenhuma ferramenta de lint está configurada hoje — por instrução explícita da sprint, nenhuma foi instalada; o passo de lint do checklist fica de fora desta entrega e é reportado aqui como achado, não inventado. **Mudança**: adicionado o job `checklist-publicacao` ao `guard-main-requires-homolog.yml` existente (não um arquivo novo), e o trigger `on.pull_request.branches` ampliado de `[main]` para `[main, homolog]` — o job `check-homolog-ancestor` original mantém seu `if: base.ref == 'main'`, então em PRs para `homolog` ele aparece como *skipped*, não falha; nenhum comportamento pré-existente foi alterado. O novo job roda `npm ci`, `npx playwright install --with-deps chromium`, `npm test` (cobre "testar URLs afetadas" via a suíte de 92 testes já existente) e `git diff --check ${{ base.sha }} ${{ head.sha }}` (cobre a checagem de conflito/whitespace do runbook), e falha o check do PR (exit code não-zero) se qualquer um desses passos falhar — não é um relatório informativo. **Validação real, não só sintaxe**: YAML parseado com `python3 -c "import yaml; yaml.safe_load(...)"` (sem erro); o comando exato do passo `git diff --check ${{ base.sha }} ${{ head.sha }}` foi reproduzido localmente contra um commit de teste descartável (branch temporária, revertida ao final) contendo trailing whitespace e marcadores `<<<<<<<`/`=======`/`>>>>>>>` — confirmado exit code 2 com as 4 violações reportadas linha a linha; o mesmo comando contra o diff real desta mudança (sem problemas) retornou exit 0, confirmando ausência de falso positivo; `npm ci` executado localmente a partir do `package-lock.json` existente, sem erro (0 vulnerabilidades); `npm test` re-executado após a mudança: 92/92, sem alteração de baseline (mudança é só CI, não toca `public/`). Não foi possível rodar o workflow via GitHub Actions de verdade nem via `act` (indisponível neste ambiente) antes deste commit — a validação real via Actions (PR de teste contra `homolog`) fica pendente para depois da publicação, sinalizado como risco residual. Os 2 itens do checklist do runbook não automatizados nesta entrega (testar URLs em desktop/mobile visualmente, validar chaves de idioma nos 3 JSONs) continuam manuais — cobertura parcial documentada, não escondida; poderiam ser endereçados em item futuro (ex. um script que valida que as 3 chaves de idioma têm o mesmo conjunto de chaves, candidato a novo ARQ-5xx). Escopo de ARQ-304 (lint de formatação CSS), mencionado nas Observações originais deste item, não foi absorvido — depende de decidir/instalar uma ferramenta de lint, fora do escopo autorizado desta sprint. |

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
| Status | CONCLUÍDO (Sprint 23, 2026-07-27) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Diff documentado; 0 divergências não justificadas — **atingido**: os dois `docker-compose.yml` foram obtidos dos servidores e comparados serviço a serviço; nenhuma divergência estrutural sem explicação. |
| Observações | Item novo, adicionado para fechar um ponto cego já citado (mas não convertido em item de ação) em `12-technical-debt.md`. **Sprint 23 (2026-07-26/27)**: Bloco A (sem acesso a servidor) achou evidência comportamental via `curl` controlado — `/api/diagnostico/` respondia com headers de app (CSP, rate-limit) em produção e como 404 plano em homologação — que sugeria ausência de paridade, na linha do achado incidental do ARQ-108/Sprint 5. **Bloco B (usuário rodou nos dois servidores) inverteu essa hipótese**: os dois `docker-compose.yml` declaram exatamente os mesmos serviços (`nginx`, `api`), mesma imagem/build — a suspeita da Sprint 5 vinha de observar `docker ps` num instante em que o `api` estava parado, não de uma diferença real de configuração. Diferenças reais encontradas (porta `8080` vs `80/443` direto; path de volume `/opt/tutela/public` vs `/var/www/tutela/public`) são topologia de proxy já documentada no ARQ-108, não falhas. Único item não explicado: volume extra `/var/www/html` em homologação, sem uso confirmado — anotado, não investigado (baixo risco). **Achado operacional durante a coleta, fora do escopo de paridade**: produção estava com `502` ativo no momento da coleta do Bloco B — `tutela_v2_nginx` em crash loop (`host not found in upstream "api"`) porque `api` não subiu após reboot do servidor (atualização do Linux) e nenhum dos serviços declara `restart:` no compose (idêntico nos dois ambientes, portanto não é divergência). Corrigido ao vivo com `docker compose up -d --build`; produção confirmada saudável depois. Ver `docs/ambientes-e-deploy.md`, seção "Diff formal — docker-compose.yml produção vs. homologação (2026-07-27)", para a tabela completa e os logs do incidente. Recomendação para sprint futura (não criada como item novo nesta auditoria, por disciplina de escopo): avaliar adicionar `restart: unless-stopped` aos serviços do compose, para não depender de intervenção manual após reboot do host. |

### ARQ-506 — Adicionar política de `restart` aos serviços do `docker-compose.yml` (produção e homologação)

| Campo | Valor |
|---|---|
| Objetivo | Impedir que um reboot de servidor derrube o site indefinidamente por um container que não sobe sozinho, como ocorreu no incidente da Sprint 23. |
| Descrição | Nenhum serviço (`nginx`, `api`) em nenhum dos dois `docker-compose.yml` (produção/homologação) declara política de `restart`. Após reboot do host, containers não voltam automaticamente; se `api` não sobe, `nginx` entra em crash loop (`host not found in upstream "api"`) e o site fica fora do ar até intervenção manual. |
| Origem | Incidente real de produção (`502`) durante a coleta de evidência de ARQ-505, 2026-07-26/27 |
| Documento | `docs/ambientes-e-deploy.md`, seção "Achado operacional durante a coleta do Bloco B" (ARQ-505) |
| Item da dívida técnica | N/A — decorre de incidente real, não de item numerado em `12-technical-debt.md` |
| Arquivos afetados | `docker-compose.yml` de produção e de homologação (`/opt/tutela-v2` de cada servidor — **não versionado neste repositório**, confirmado desde a Sprint 5 e reconfirmado na Sprint 23) |
| Dependências (depende de) | ARQ-505 (auditoria que originou o achado e confirmou que os dois ambientes declaram os mesmos serviços) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Acesso SSH aos dois servidores (produção e homologação) |
| Critérios de Aceite | `restart: unless-stopped` declarado em cada serviço (`nginx`, `api`) nos dois `docker-compose.yml`; `docker compose ps`/`docker compose config` confirma a política ativa nos dois ambientes; teste de recuperação automática de um crash real (não `docker kill` — ver Observações) bem-sucedido em pelo menos homologação |
| Critérios de Regressão | Nenhum serviço saudável passa a reiniciar em loop; `docker compose stop` manual continua parando o serviço (não é sobrescrito pela política de restart) |
| Impacto | Alto — outage real já ocorreu em produção por essa lacuna |
| Risco | Baixo — mudança aditiva de uma linha por serviço, reversível via backup do compose antes de editar |
| Complexidade | Baixa |
| Estimativa | P |
| Responsável | DevOps |
| Status | CONCLUÍDO (Sprint 24, 2026-07-27) — homologação e produção, ambas validadas com evidência real de crash-recovery |
| ADR relacionado | Nenhum (a criar em ARQ-701 se necessário — tratado como mudança operacional aditiva, não decisão arquitetural) |
| Métrica de sucesso | 100% dos serviços (`nginx`, `api`) com `restart: unless-stopped` ativo nos dois ambientes, confirmado via `docker compose config`; teste de crash real bem-sucedido — **atingido nos dois ambientes** |
| Observações | Política escolhida (`unless-stopped` em vez de `always` ou `on-failure`): confirmado contra a documentação oficial do Docker (`docs.docker.com/engine/containers/start-containers-automatically`) — `unless-stopped` reinicia o container em crash e em reboot do host, exatamente como `always`, mas difere no caso de parada manual: se o container foi parado deliberadamente (`docker compose stop`) antes de um restart do daemon, `unless-stopped` respeita essa parada e não o sobe de volta, enquanto `always` o ressuscitaria mesmo assim. `on-failure` foi descartado por não cobrir de forma confiável o caso de reboot do host em todas as versões/configurações de Docker/systemd. **Homologação (2026-07-27)**: `restart: unless-stopped` aplicado a `nginx` e `api` via `docker compose up -d`, confirmado em `docker compose config`. **`docker kill` demonstrou NÃO ser um teste válido de recuperação**: Docker trata `docker kill`/`docker stop` (chamadas via API do Engine) como parada manual e não aplica a política de restart mesmo com `unless-stopped` (`RestartCount` ficou em 0, comportamento documentado: "if you manually stop a container, the restart policy is ignored"). Uma segunda tentativa via `docker exec ... kill -9 1` (de dentro do próprio namespace do container) também falhou, por um motivo diferente e a nível de kernel: PID 1 dentro de um PID namespace só recebe SIGKILL/SIGSTOP de forma incondicional quando o sinal vem de um namespace ancestral (o host); vindo de dentro do mesmo namespace, PID 1 sem handler instalado ignora o sinal (`pid_namespaces(7)`). O teste que efetivamente simula um crash real é enviar SIGKILL diretamente ao PID real do processo no host (`docker top` para obter o PID, depois `sudo kill -9 <PID>` — fora da API do Docker), o que finalmente produziu `RestartCount=1` e `StartedAt` atualizado sem qualquer intervenção manual — recuperação automática confirmada. **Bug de aplicação encontrado e corrigido durante o teste (fora do escopo original de ARQ-506, mas bloqueava a validação)**: o `api` de homologação não sobrevivia a nenhum restart — `server.js:10` usava `require("node-fetch")` contra `node-fetch@3.3.2` (ESM-only, incompatível com `require`), crash imediato e determinístico em todo boot. Também havia um bloco de código morto logo abaixo (linhas 12-17: `grecaptcha.getResponse()`/`alert(...)`, globals de navegador sem sentido em Node) que teria crashado o processo de novo mesmo após corrigir o `node-fetch`. Corrigido em homologação: removida a dependência `node-fetch` (Node 18 tem `fetch` nativo, usado sem alterações por `validarCaptcha()`) e o bloco morto; rebuild (`docker compose build api`) e validação de boot limpo confirmados antes do teste de crash. **Achado adicional, não corrigido (baixo risco, registrar para sprint futura)**: `Dockerfile` do `api` faz `COPY package.json .` + `RUN npm install` sem copiar `package-lock.json` antes — builds nunca foram reprodutíveis via lockfile. **Produção (2026-07-27)**: `server.js`/`package.json` verificados — **sem o bug de `node-fetch`/código morto**; usa `fetch` nativo com `try/catch` em `validarCaptcha()`, sem dependência `node-fetch` declarada (resíduo órfão de `node-fetch@3.3.2` encontrado em `node_modules`, não referenciado em nenhum lugar — inofensivo, não limpo nesta sessão). Nenhuma correção de código necessária. `docker compose config` já mostrava `restart: unless-stopped` presente em `nginx`/`api` — usuário confirmou tê-lo aplicado manualmente logo após o incidente da Sprint 23, antes desta sessão. Teste de crash real (mesmo método: `docker top` + `sudo kill -9 <PID>` no host) confirmado com sucesso: `RestartCount` incrementou para 1, `StartedAt` atualizado, recuperação automática sem intervenção. **Achado colateral, não relacionado a `ARQ-506`**: o `server.js` de produção usa esquema de variáveis de ambiente para SMTP (`SMTP_HOST`/`SMTP_PORT`/`SMTP_USER`/`SMTP_PASS`/`SMTP_FROM`/`SMTP_TO`) diferente do que homologação tinha antes da correção (host Zoho fixo no código, `EMAIL_USER`/`EMAIL_PASS`) — os dois ambientes rodavam código genuinamente divergente, não apenas homologação com um bug a mais. Também confirmado nesta sessão: `/opt/tutela-v2/api` não é um repositório Git em nenhum dos dois servidores — o código do `api` não tem controle de versão em lugar nenhum, achado que motivou decisão do usuário de criar um repositório GitHub novo e privado para o `api` (fora do escopo de `ARQ-506`, candidato a item novo de backlog). Diff exato e comandos preparados na entrega da Sprint 24 (fora do backlog, no corpo da resposta ao usuário — não há arquivo de compose neste repositório para versionar o diff). |

### ARQ-507 — Versionar o `api` em repositório Git próprio e reconciliar homologação/produção

| Campo | Valor |
|---|---|
| Objetivo | Colocar o código do `api` (achado sem controle de versão em nenhum dos dois servidores, durante `ARQ-506`) sob Git, e eliminar a divergência de código real encontrada entre produção e homologação. |
| Descrição | `/opt/tutela-v2/api` não era um repositório Git em nenhum ambiente — mudanças (incluindo o bug de `node-fetch` corrigido em `ARQ-506`) não tinham diff, revisão ou histórico. Além disso, os dois ambientes rodavam código genuinamente diferente (não só o bug): esquema de variáveis SMTP distinto, e homologação não tinha proxy `/api/` configurado no Nginx (achado à parte, ver Observações). |
| Origem | Achado incidental durante a validação de `ARQ-506`, decisão explícita do usuário nesta sessão |
| Documento | Nenhum — decisão e execução registradas apenas aqui e no histórico do novo repositório |
| Item da dívida técnica | N/A |
| Arquivos afetados | Novo repositório GitHub `cleberNetCenter/tutela-api` (privado); `/opt/tutela-v2/api/.env` (produção e homologação); `/opt/tutela-v2/nginx/default.conf` (homologação) |
| Dependências (depende de) | ARQ-506 (achado durante sua validação) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Acesso SSH aos dois servidores; acesso para criar repositório privado no GitHub da conta `cleberNetCenter` |
| Critérios de Aceite | Código do `api` versionado, sem segredos/PII no histórico; produção e homologação no mesmo histórico Git (branches `main`/`homolog`, espelhando o modelo já usado no repositório do frontend); `/api/health` respondendo `200` via Nginx nos dois ambientes |
| Critérios de Regressão | Nenhum segredo (`.env`) ou dado de usuário (`logs/leads.jsonl`) commitado; funcionalidade de diagnóstico/e-mail inalterada |
| Impacto | Alto — sem isso, qualquer mudança futura no `api` repete o mesmo risco que causou o bug de `node-fetch` sem detecção |
| Risco | Baixo (mudança aditiva de tooling; nenhuma lógica de aplicação alterada) |
| Complexidade | Média |
| Estimativa | M |
| Responsável | DevOps |
| Status | CONCLUÍDO (Sprint 24, 2026-07-27) |
| ADR relacionado | Nenhum |
| Métrica de sucesso | Repositório privado criado e populado; `.gitignore` excluindo `.env`/`logs/`/`node_modules/` confirmado antes do primeiro commit; produção e homologação sincronizadas; `/api/health` = `200` nos dois ambientes — **todos atingidos** |
| Observações | **Repositório**: `github.com/cleberNetCenter/tutela-api`, privado, criado a partir do código de produção (mais maduro — `fetch` nativo, `try/catch` em `validarCaptcha()`, SMTP via env vars). Autenticação por deploy key SSH dedicada por servidor (não reutiliza chave pessoal), uma com acesso de escrita em cada host, seguindo o mesmo padrão de branches `main`/`homolog` do repositório do frontend. **Reconciliação de homologação**: `git init` + `git reset --hard origin/homolog` trouxe o código canônico de produção para homologação sem tocar `.env`/`logs/`/`node_modules` (fora do controle de versão, confirmado via `git status` antes e depois). `.env` de homologação teve `EMAIL_USER`/`EMAIL_PASS` renomeados para `SMTP_USER`/`SMTP_PASS` (mesmos valores/conta, confirmado explicitamente pelo usuário) e ganhou `SMTP_HOST=smtp.zoho.com`, `SMTP_PORT=587` (não 465 — o código adotado usa `secure: false`/STARTTLS, incompatível com a porta antiga de TLS implícito), `SMTP_FROM`, `SMTP_TO`; `RECAPTCHA_SECRET` deixado em branco de propósito (homologação nunca teve uma chave reCAPTCHA própria para seu domínio — gap pré-existente, não introduzido nem corrigido nesta sessão). Duas idas e vindas na edição do `.env`: um `cat >> .env` acabou duplicando linhas (execução repetida), e uma primeira tentativa de preencher os valores colou o texto-placeholder literalmente (`<o mesmo valor atual de EMAIL_USER>`) em vez do segredo real — corrigido copiando o valor real diretamente do `.env` de produção (mesma conta SMTP), nunca colado nesta conversa. **Achado adicional, corrigido nesta sessão, fora do escopo original de `ARQ-506`/versionamento**: o Nginx de homologação (`/opt/tutela-v2/nginx/default.conf`, arquivo diferente, nunca tocado antes nesta sessão) não tinha nenhum `location /api/` — toda requisição a `/api/*` caía no `location /` genérico e retornava `404` estático do Nginx, não do Express. Bug pré-existente e independente de tudo mais encontrado hoje: o formulário de diagnóstico provavelmente nunca funcionou de ponta a ponta em homologação. Corrigido copiando o bloco `location /api/ { proxy_pass http://api:3000; ... }` exatamente como configurado em produção (`docker exec tutela_v2_nginx cat /etc/nginx/conf.d/default.conf` usado como referência real, não presumido); validado com `nginx -t` antes do `nginx -s reload`; `curl https://localhost/api/health` = `200` confirmado após. **Não corrigido, registrado para decisão futura**: `RECAPTCHA_SECRET` ausente em homologação (impede teste real do fluxo de captcha nesse ambiente); `Dockerfile` do `api` ainda não usa `package-lock.json` no build (ver Observações de `ARQ-506`); pipeline de deploy automatizado (CI/CD) para o `api` não existe — sincronização futura entre os dois ambientes ainda depende de repetir manualmente os passos desta sessão. |

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
| Arquivos afetados | `public/partials/header.html` (skip-link, propagado via SSI); `public/assets/css/styles-header-final.css` (estilo, tokens de `foundation/tokens.css`); `public/assets/lang/pt.json`, `en.json`, `es.json` (texto traduzível `global.skipToContent`); `id="main-content" tabindex="-1"` adicionado ao `<main>` de 36/36 páginas reais (todas as páginas que incluem `header.html` via SSI); novo `tests/accessibility.spec.ts` |
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
| Status | CONCLUÍDO (Sprint 7, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | Skip-link funcional em 37/37 páginas, validado com navegação por Tab — **atingido em 36/37**: das 37 páginas HTML do repositório, 36 incluem `header.html`/`nav` real via SSI e receberam o destino `id="main-content"`; a 37ª (`public/insights/ativos-digitais/o-que-sao-ativos-digitais/index.html`) é um stub de redirect (`meta http-equiv="refresh"` + `window.location.replace`), sem `header.html`, sem navegação e sem conteúdo próprio a pular — fora do escopo do débito técnico #8 (que fala em usuário tabulando pela navegação, inexistente nesta página). |
| Observações | Implementado em Sprint 7: `header.html` recebeu `<a class="skip-link" href="#main-content" data-i18n="global.skipToContent">` como primeiro elemento, antes de `<header>` — confirmado via grep que nada precede o `<!--#include virtual="/partials/header.html" -->` em nenhuma página além de `<div class="app">` (ou nada), então o skip-link é sempre o primeiro elemento focável real do documento. Estilo em `styles-header-final.css` (mesmo arquivo CSS já carregado nas 36 páginas junto com `header.html`, evitando um quinto arquivo CSS): oculto via `transform: translateY(-100%)` (não `display:none`, que impediria o foco), visível em `:focus`; cores usam os tokens globais já existentes (`--color-surface-brand`, `--color-text-inverse`, `--color-accent-bright` de `foundation/tokens.css`), sem introduzir um novo namespace de cor (evitando repetir o padrão já catalogado no débito técnico #6/ARQ-301). Texto traduzível via `data-i18n="global.skipToContent"`, com chave nova adicionada aos 3 arquivos de idioma (`pt.json`, `en.json`, `es.json`), consistente com o mecanismo de i18n já usado no resto do `header.html` — evita hardcode de string em um só idioma num site trilíngue. Destino: mapeamento completo do `<main>` real (não presumido a partir de `05-components.md`) via grep de todas as 37 páginas HTML encontrou 6 variantes de `<main class="...">` (e uma sem classe); todas as 36 páginas que incluem `header.html` tiveram `id="main-content" tabindex="-1"` adicionado ao seu `<main>` (o `tabindex="-1"` é necessário para que o navegador efetivamente mova o foco da página para `#main-content` ao ativar o link — sem ele, `<main>` não é nativamente focável e o foco ficaria preso em `document.body`, apesar do scroll acontecer). O partial `public/partials/ativos-digitais-pillar-main.html` (mesma variante de classe `<main>`) não foi tocado: confirmado via grep que não é incluído por nenhuma página (dead code pré-existente, fora do escopo aditivo desta sprint). Teste novo `tests/accessibility.spec.ts` cobre 3 páginas (home, `/legal/termos-de-uso.html`, `/ativos-digitais/` — 1 por cluster relevante, acima do mínimo de 2 pedido) verificando: skip-link presente com `href="#main-content"`, oculto (fora da viewport) antes do foco, é o primeiro elemento focado por `Tab`, fica visível ao receber foco, e ao ativar (`Enter`) move o foco DOM para `#main-content` (não só scroll). `npm test`: baseline 7/7 confirmado antes da mudança, nenhuma asserção alterada nos 7 testes existentes; 10/10 depois (7 + 3 novos), sem regressão. |

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
| Status | CONCLUÍDO (Sprint 8, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 erros de landmark/ARIA reportados por axe-core — **atingido por auditoria equivalente**: axe-core não foi adicionado como dependência nova (ver Observações); a verificação foi feita por auditoria manual (grep/leitura) das 37 páginas reais + 6 novos testes Playwright que travam a estrutura corrigida, cobrindo os 3 gaps encontrados. |
| Observações | Concluído em Sprint 8, como auditoria completa das 37 páginas reais (landmarks, ARIA de componentes interativos, hierarquia de headings, `alt` de imagens) seguida de correção pontual dos achados inequívocos e de baixo risco. **Achados corrigidos** (evidência via grep, detalhada no relatório da sprint): (1) os 4 botões `.nav-toggle` de `partials/header.html` tinham `aria-expanded`/`aria-haspopup` mas nenhum `aria-controls` apontando para o `<ul id="drop-...">` que efetivamente controlam — adicionado `aria-controls` nos 4, propagado via SSI às 36 páginas que incluem o header. (2) Os 3 ícones de bandeira do seletor de idioma **desktop** (`.lang-switch`, `partials/header.html:134-136`) não tinham `alt`, enquanto o mesmo conjunto de ícones na versão **mobile** (`.lang-switch-mobile`, mesmo arquivo, linhas 99-101) já tinha `alt="Português"/"English"/"Español"` — o único gap de `alt` em todo o repositório (confirmado: só existem 6 tags `<img>` no site inteiro, todas em `header.html`); corrigido reaproveitando o texto já existente no próprio arquivo, sem decisão de copy nova. (3) 4 páginas (`empresas.html`, `governo.html`, `pessoas.html`, `ativos-digitais/index.html`) têm 2 landmarks `<aside>` cada, sem diferenciação para leitor de tela; adicionado `aria-labelledby` em cada `<aside>` apontando para o `id` do parágrafo de rótulo já existente e visível dentro dele (`sol-aside-label`/`sol-tech-label` nas 3 páginas de solução; `intro-aside-label`/`muda-aside-label` no cluster Ativos Digitais) — nenhum texto novo introduzido. **Achados não corrigidos nesta sprint** (fora do escopo original de ARQ-602, adjacentes e de mesmo custo de verificação): hierarquia de headings com nível pulado em 5 páginas, registrado como novo item [ARQ-605](#arq-605--corrigir-hierarquia-de-headings-h1-h6); nenhum achado de `alt` ausente restante (100% dos 6 `<img>` do site corrigidos nesta mesma sprint, então não há item futuro pendente para `alt`). **Não corrigido, documentado apenas como observação, sem virar item novo** (não é dívida técnica de landmark/ARIA, é de i18n/copy): o rótulo do botão `.mobile-menu-btn` permanece `aria-label="Abrir menu"` fixo, sem alternar para indicar o estado aberto — exigiria decisão de copy (string nova nos 3 idiomas), fora do critério de correção "só o atributo" desta sprint; candidato natural para ser resolvido junto de ARQ-603 (mesmo componente de navegação). Todos os 36 `<nav>` duplicados por página (breadcrumb + navegação principal, e o caso de 3 `<nav>` em `insights/index.html`) já tinham `aria-label` distinto (`"Breadcrumb"`, `"Explorar temas"`, `"Navegação principal"`) — confirmado sem necessidade de correção. Testes novos em `tests/accessibility.spec.ts` (bloco "Landmarks e ARIA (ARQ-602)"): 4 botões de dropdown com `aria-controls` válido; 3 ícones de idioma desktop com `alt`; 4 páginas com 2 `<aside>` cada verificadas por `aria-labelledby` distinto e resolvível. `npm test`: baseline 10/10 confirmado antes da mudança; 16/16 depois (10 + 6 novos), sem regressão. |

### ARQ-603 — Navegação por teclado nos dropdowns

| Campo | Valor |
|---|---|
| Objetivo | Garantir que os dropdowns de navegação sejam 100% operáveis via teclado (Tab/Enter/Esc). |
| Descrição | Auditoria e correção de comportamento de teclado no script de menu, hoje concentrado em `mobile-menu.js`. |
| Origem | Contexto do débito técnico #4 (mesmo arquivo) e Épico 6 do roadmap ("Keyboard") |
| Documento | `12-technical-debt.md` |
| Item da dívida técnica | N/A — relacionado ao item #4 via arquivo, mas o teste de teclado em si não está numerado em `12-technical-debt.md` |
| Arquivos afetados | Sucessor de `mobile-menu.js`/`dropdown-menu.js` definido em ARQ-405; `public/assets/css/styles-header-final.css` (correção de um bug visual encontrado em validação manual, ver Observações) |
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
| Status | CONCLUÍDO (Sprint 9, 2026-07-24) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 100% dos itens de dropdown operáveis via teclado, validado manualmente e via Playwright — **atingido**: os 4 dropdowns desktop e o menu mobile (mesmo componente, `navigation-menu.js`) são 100% operáveis via Tab/Shift+Tab, Enter/Space, Escape e setas, sem alterar o comportamento de mouse/hover das Sprints 3-4 (regressão confirmada: os 2 testes de mouse/hover pré-existentes em `tests/navigation.spec.ts` continuam passando sem alteração de asserção). |
| Observações | Implementado em Sprint 9, em `public/assets/js/navigation-menu.js` (arquivo definido em ARQ-405). **Já conforme, sem alteração** (confirmado antes de codificar, não presumido): Enter/Space no toggle e no botão hambúrguer já abriam/fechavam via semântica nativa de `<button>` (dispara `click`), pois ambos já eram elementos `<button type="button">`/`<button>` reais desde a Sprint 8; Tab/Shift+Tab entre os itens de nível superior e, uma vez com o dropdown aberto, entre os itens do submenu, já seguiam a ordem lógica do DOM sem necessidade de `tabindex` manual. **Implementado nesta sprint**: (1) `ArrowDown` com foco no toggle abre o dropdown e move o foco para o primeiro item do submenu; `ArrowUp`/`ArrowDown` com foco em um item do submenu aberto navegam entre os itens, com wrap-around nas duas pontas (nível básico, sem `Home`/`End` — não há evidência de necessidade real, critério de aceite não exige). (2) `Escape` agora fecha o dropdown aberto e devolve o foco ao toggle que o abriu quando o foco estava dentro do dropdown (toggle ou item de submenu) — antes, `Escape` já fechava (via `closeAll()` global), mas nunca devolvia o foco; confirmado via teste antes de alterar (não presumido). (3) Fechamento automático ao sair do dropdown por Tab/Shift+Tab (`focusout`), restrito a desktop, para não deixar o dropdown flutuando aberto com o foco já em outro lugar da página — necessário porque, sem isso, o CSS teria mantido `display:block` via a classe `.open` (JS) independente de onde o foco estivesse. (4) Menu mobile: `Escape` agora também fecha o menu mobile (`#nav.open`) e devolve o foco ao botão hambúrguer, quando aberto (antes, `Escape` só tratava dropdowns, nunca o menu mobile). Contenção de foco: **não implementado como "focus trap" completo** — decisão deliberada, não ambígua: o texto do critério de aceite fala apenas em "abrir, navegar itens, fechar com Esc", sem menção a bloquear o foco dentro do menu; um trap completo expandiria escopo além do item catalogado. **Bug pré-existente descoberto e corrigido durante a implementação** (não catalogado antes, necessário para o próprio ArrowDown/Enter funcionarem de forma confiável): `closeAll()`, usado nos handlers de clique/hover/`ArrowDown`, fechava indiscriminadamente **todos** os dropdowns, incluindo aquele que estava prestes a ser aberto — como `closeDrop()` remove o foco do toggle quando ele está focado (comportamento proposital da correção "Fix desktop dropdown focus handoff", commit `cd586fd`, que evita o dropdown ficar preso visualmente aberto via `:focus-within` do CSS), isso causava um blur espúrio do toggle no meio da própria abertura, que colidia com o novo fechamento por `focusout` e reabria/fechava o dropdown de forma inconsistente (race condition, capturada e corrigida via testes automatizados antes da entrega, não em produção). Corrigido com uma função `closeOthers(dropAtual)`, que fecha todos os outros dropdowns sem tocar no que está sendo aberto — elimina o blur espúrio na raiz, sem alterar o comportamento de fechar-por-clique-fora ou de mouse/hover (`closeAll()` continua usado, sem alteração, no listener de clique fora e nas outras chamadas onde não há esse conflito). **Sub-item absorvido**: `.mobile-menu-btn` alterna `aria-label` entre "Abrir menu"/"Fechar menu" (chaves novas `global.openMenu`/`global.closeMenu` em `pt.json`/`en.json`/`es.json`, reaproveitando o mesmo mecanismo de i18n já usado para `global.skipToContent` na Sprint 7 — nenhuma convenção nova). Testes novos em `tests/navigation.spec.ts` (bloco "Navegação por teclado nos dropdowns (ARQ-603)"): Enter/Space abrindo e fechando; Tab entrando no submenu em ordem lógica; `ArrowDown`/`ArrowUp` com wrap-around; `Escape` devolvendo o foco ao toggle a partir de um item de submenu; menu mobile com Enter/Space, alternância de `aria-label` e `Escape` devolvendo o foco ao botão hambúrguer (idioma fixado via `localStorage.tutela_lang` no teste, para não depender do locale do navegador de teste). `npm test`: baseline 16/16 confirmado antes da mudança (rodado 3x para descartar flakiness pré-existente); 21/21 depois (16 + 5 novos), sem regressão — suíte completa também rodada 3x consecutivas após a implementação final, 21/21 nas três, para descartar flakiness introduzida pelo `setTimeout(0)` do fechamento por `focusout`. **Bug visual encontrado só em validação manual, após a entrega inicial** (as asserções Playwright checavam apenas `aria-expanded`/classe `.open`, não o estado visual real — gap identificado a partir de uma pergunta direta do usuário sobre teste visual pendente): ao devolver o foco ao toggle após `Escape` (comportamento exigido pelo critério de aceite), o dropdown permanecia **visualmente aberto** (`display: block`, `opacity: 1`, confirmado via `getComputedStyle`), mesmo com `aria-expanded="false"` e sem a classe `.open` — causa raiz era a regra CSS `.nav-dropdown:focus-within .dropdown-menu`, que exibia o submenu sempre que o *toggle* estivesse focado, não só quando o foco estava dentro do próprio submenu (mesma regra que motivou o commit anterior `cd586fd`, "Fix desktop dropdown focus handoff", mas para um gatilho diferente). Corrigido trocando o seletor para `.dropdown-menu:focus-within` (escopado ao próprio menu, não ao contêiner `.nav-dropdown` inteiro) — o item aberto por hover e o item mantido visível enquanto o foco está em um link do submenu (necessário para `Tab` funcionar dentro do dropdown já aberto) continuam funcionando; confirmado via `getComputedStyle` antes/depois da correção, screenshots de antes/depois (toggle focado, dropdown aberto via `ArrowDown`, `Escape` fechado, menu mobile aberto/fechado) e nova rodada de `npm test` (21/21, 2x consecutivas) e dos 2 testes de regressão de mouse/hover pré-existentes, sem alteração de asserção. |

### ARQ-604 — Auditoria e correção de contraste (WCAG AA)

| Campo | Valor |
|---|---|
| Objetivo | Garantir que todos os pares texto/fundo atendam ao contraste mínimo exigido pelo WCAG AA. |
| Descrição | Auditoria de contraste em toda a paleta de cores em uso, após a consolidação de tokens (ARQ-301). |
| Origem | Contexto WCAG geral (`06-design-system.md`) e Épico 6 do roadmap ("Contraste") |
| Documento | `06-design-system.md`, `12-technical-debt.md` |
| Item da dívida técnica | N/A — decorre do Épico 6 do roadmap, sem item numerado específico em `12-technical-debt.md` |
| Arquivos afetados | `public/assets/css/foundation/tokens.css`, `public/assets/css/styles-header-final.css`, `public/assets/css/sections/footer.css`; script de auditoria em `tests/support/contrast-audit.js`; rede de regressão visual em `tests/visual-contrast.spec.ts` |
| Dependências (depende de) | ARQ-301 (tokens de cor já unificados, evita retrabalho) — não satisfeita no momento em que ARQ-604 rodou (Sprint 10); **satisfeita retroativamente na Sprint 11**, ver Observações |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | ARQ-301 concluído — **exceção registrada nesta sprint**, ver Observações |
| Critérios de Aceite | Todos os pares texto/fundo ≥ 4.5:1 (ou 3:1 para texto grande/componente UI), conforme WCAG AA |
| Critérios de Regressão | Identidade visual de marca preservada (ajustes de contraste não descaracterizam a paleta); nenhum teste funcional (21/21) ou visual regride |
| Impacto | Médio |
| Risco | Baixo |
| Complexidade | Média |
| Estimativa | M |
| Responsável | Frontend |
| Status | CONCLUÍDO PARCIALMENTE (Sprint 10, 2026-07-24) — 2 achados remanescentes documentados, não corrigidos (ver ARQ-606) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 38 pares texto/fundo e UI/fundo auditados (tokens globais, `--ad-*`, `--ux-*`, header/nav/dropdown/menu mobile/skip-link, rodapé, páginas legais); 36/38 atendem WCAG AA após correção — **2 falhas remanescentes, achado registrado em ARQ-606** |
| Observações | **Atualização (Sprint 11)**: ARQ-301 concluído — `--ux-*` foi consolidado em `--ad-*`/`--ad-pillar-*` preservando cada valor numérico exatamente (ver observação de ARQ-301), então a reaudição pontual antecipada abaixo **não encontrou nenhuma mudança**: `tests/support/contrast-audit.js` re-executado após a migração continua reportando os mesmos 38 pares e as mesmas 2 falhas (ambas de ARQ-606, não relacionadas a `--ux-*`/`--ad-pillar-*`) — os 9 pares antigamente rotulados `--ux-*` na tabela abaixo passaram a `--ad-pillar-*`, sem mudança de valor. **Texto original da Sprint 10, mantido para histórico**: dependência de ARQ-301 não satisfeita — ARQ-301 (unificação `--ux-*` → `--ad-*`) seguia BACKLOG; ainda assim, o `--ux-*` foi auditado nesta sprint como sistema à parte (confirmado que ainda existia, ver `06-design-system.md`/débito técnico #6) e **todos os seus pares passaram WCAG AA sem necessidade de correção** — nenhum retrabalho foi de fato perdido pela dependência não satisfeita, mas uma futura consolidação (ARQ-301) poderia alterar esses valores e exigiria reaudição pontual dos pares `--ux-*` então unificados — **confirmado agora que não alterou**. **2 correções aplicadas** (ver tabela completa na entrega da Sprint 10): `--primitive-neutral-600` (`--color-text-muted`) escurecido de `#4f7c6b` para `#4a7464` (falhava 4.38:1 e 4.07:1; ambos ≥4.5:1 após); `--text-3` (header/footer/busca) clareado de `#4a7258` para `#6e8e79` (falhava 2.99:1; 4.53:1 após) — declarado independentemente em `styles-header-final.css` e `footer.css`, ambos atualizados. **1 achado não corrigido, registrado como novo item rastreável**: subtítulo de hero das páginas legais (`rgba(255,255,255,0.68)` sobre gradiente `--primitive-green-950`→`--primitive-green-700`) falha WCAG AA (1.64:1–2.0:1 conforme o stop do gradiente) — não corrigido nesta sprint porque a correção exigiria elevar a opacidade a um nível perceptualmente diferente (subtítulo bem mais proeminente) em ~29 declarações `rgba(255,255,255,*)` distintas de `legal-shared.css`, usadas em 34 páginas — ver [ARQ-606](#arq-606--corrigir-contraste-do-subtítulo-de-hero-das-páginas-legais). `.logo sup` (marca "Tutela Digital™") também apareceu na varredura inicial (2.99:1 antes da correção de `--text-3`) mas está isento pelo WCAG 1.4.3 (texto de logotipo/marca não tem exigência mínima de contraste) — passou a 4.53:1 como efeito colateral benéfico da correção de `--text-3`, sem ser o motivo da correção. Rede de regressão visual (`tests/visual-contrast.spec.ts`) criada nesta sprint como consequência direta do trabalho de contraste — primeira cobertura de screenshot do projeto (lacuna registrada desde ARQ-301/Sprint 4); baseline versionado em `tests/visual-contrast.spec.ts-snapshots/`. **Investigação (Sprint 26, 2026-07-27)**: desde por volta da Sprint 22/23, `npm test` rodado localmente (ambiente de execução deste assistente) vinha reportando 2 falhas nesta suíte — "Footer: recorte" e "Dropdown de navegação aberto: recorte do header" — citadas sprint após sprint como "pré-existentes, não relacionadas ao escopo corrente, não investigadas". Investigação nesta sprint determinou que **não são uma regressão real do projeto**: (1) o diff é determinístico (mesmo checksum de imagem-diff em execuções repetidas no mesmo ambiente, não é ruído aleatório); (2) `gh run list`/`gh run view` no workflow `guard-main-requires-homolog.yml` (job `checklist-publicacao`, que roda `npm test` em runner `ubuntu-latest` do GitHub Actions — o CI real que efetivamente porta o gate de PR) mostra **92 passed, consistentemente, em todas as execuções recentes**, incluindo o mesmo commit onde a execução local relatava 90/92. Ou seja: a suíte está e sempre esteve verde no CI oficial; as 2 falhas são específicas do ambiente local usado nesta investigação. Hipótese inicial de causa raiz: `public/index.html:29` (e demais páginas) carrega as fontes "Inter"/"Cormorant Garamond" ao vivo do Google Fonts (`fonts.googleapis.com`/`fonts.gstatic.com`), sem nenhum arquivo `.woff2` vendorizado no repositório — confirmado via inspeção de rede (`page.on('response')`) que o navegador de teste baixa esses arquivos da CDN do Google a cada execução; hipótese era que pequenas diferenças de hinting/anti-aliasing do arquivo servido (variando por ambiente/momento, mesmo sob a mesma URL versionada) bastariam para deslocar ~1% dos pixels em recortes pequenos e ricos em texto (footer, header). **Nenhuma correção de código aplicada nesta sessão de investigação** — o CI oficial já passa, então não há regressão a corrigir; forçar uma correção local arriscaria mascarar uma regressão real futura sem necessidade. **Implementado ainda na Sprint 26 (2026-07-27), mesmo dia da investigação**: decisão do responsável pelo projeto de vendorizar as fontes na hora, em vez de deixar como melhoria futura. Todos os 5 conjuntos de fonte do site (Inter, Cormorant Garamond — template principal; Playfair Display, Source Serif 4, DM Mono — cluster dark-editorial de Ativos Digitais/Insights, 9 páginas) foram baixados **exatamente nas mesmas versões já servidas pelo Google** (Inter v20, Cormorant Garamond v21, Playfair Display v40, Source Serif 4 v14, DM Mono v16 — confirmado via `curl` com User-Agent moderno antes do download, para preservar a aparência bit a bit) e passaram a residir em `public/assets/fonts/<família>/` (15 arquivos `.woff2` — só subset `latin`, ver correção abaixo sobre `latin-ext`). Dois `@font-face` novos: `public/assets/css/fonts.css` (Set A) e `public/assets/css/fonts-editorial.css` (Set B), mesma convenção de cache-busting do projeto (`?v=1`, ARQ-502). `partials/header.html` (loader global injetado via JS, incluído por SSI em toda página) simplificado: removidos os 2 `<link rel="preconnect">` a domínios do Google (deixaram de fazer sentido para um recurso same-origin), `href` do stylesheet injetado repontado para o CSS local. As 3 páginas com Set A hardcoded (`index.html`, `seguranca.html`, `como-funciona.html`) e as 9 páginas com Set B hardcoded (cluster `ativos-digitais/*`/`insights/ativos-digitais/*`) tiveram o `<link>` do Google trocado pelo CSS local correspondente. Guard-test `tests/regression-sprints.spec.ts` (ARQ-503, antes verificava "exatamente 1 par de preconnect de fontes") atualizado para a nova invariante: 0 preconnects a `fonts.googleapis.com`/`fonts.gstatic.com`, e exatamente 1 `<link id="global-fonts-loaded">` apontando para o CSS local. `tests/support/asset-versions.js` ganhou um 3º caso em `findEmbeddedRefs()` (mesmo padrão de `i18n.js`/`search.js`) para rastrear a referência embutida em `partials/header.html`; manifesto regenerado via `node tests/support/generate-asset-versions.js` (também corrigiu, de quebra, um hash de `search-index.json` que estava desatualizado desde o último commit automático do workflow de sitemap — não relacionado a fontes). `docs/architecture/09-security.md` atualizado: Google Fonts removido da lista de integrações de terceiro.

**Correção importante, descoberta ao validar a implementação (mesma sessão)**: a hipótese de causa raiz acima (drift de hinting entre execuções da CDN do Google) **estava errada** — confirmado ao comparar, byte a byte (`md5sum`), o `footer-diff.png` gerado antes e depois de vendorizar as fontes: **checksum idêntico**. Ou seja, servir exatamente os mesmos bytes de fonte localmente não mudou em nada o resultado das 2 falhas locais — elas continuam ocorrendo, sem alteração. A causa real permanece não identificada com precisão (provável diferença de rasterização de texto do Chromium entre esta sandbox e a máquina que gerou o baseline "ambiente CI real", possivelmente ligada a driver de GPU/software rendering, não a fonte em si) — mas a conclusão prática da investigação original continua de pé e não é afetada por esse erro de hipótese: o CI oficial (GitHub Actions) segue 100% verde, então isso não é uma regressão do projeto, é um artefato desta sandbox específica. Vendorizar as fontes foi mantido mesmo assim, pelos benefícios reais e independentes (remove dependência de terceiro, `ARQ-102`/CSP, privacidade) — só não pelo motivo originalmente suposto.

**Efeito colateral real da vendorização, encontrado e corrigido na mesma sessão**: substituir ~13 requisições externas (CDN do Google, altamente paralela) por até 15 requisições ao servidor de teste local (`tests/support/ssi-server.js`, processo Node único) por página sobrecarregou esse servidor sob a concorrência default do Playwright (múltiplos workers pedindo várias fontes ao mesmo tempo) — reproduzido de forma consistente (`npm test` completo passou a falhar de forma variável, 3 a 7 falhas por execução, quase todas timeout de `waiting for fonts to load`, não diff de pixel). Três correções aplicadas, nesta ordem: (1) `tests/support/ssi-server.js` — handler convertido de `fs.*Sync` bloqueante para `fs.promises` assíncrono (o event loop único ficava bloqueado por chamadas `statSync`/`readFileSync` síncronas em cada uma das ~15 requisições de fonte por página); (2) subset `latin-ext` removido inteiramente (confirmado via varredura de `assets/lang/{pt,en,es}.json`: nenhum caractere fora de `U+0000-00FF` em nenhum dos 3 idiomas do site) — 30→15 arquivos `.woff2`, metade da carga, benefício que também vale para usuários reais (menos peso/requisições); (3) `playwright.config.ts` ganhou `expect: { timeout: 10000 }` (era o default de 5000ms) para dar margem ao carregamento de fonte local sob concorrência, sem mascarar timeouts genuínos (timeout de teste continua 30s). Após as 3 correções: `npm test` completo executado 4x consecutivas, **90/92 estável em todas** (mesmas 2 falhas conhecidas, nenhuma variação) — confirma que a regressão de confiabilidade introduzida pela vendorização foi corrigida antes de publicar. Efeito colateral (bônus) da remoção do Google Fonts: sai da lista de origens externas que uma futura implementação de `ARQ-102` (CSP) precisaria liberar, e o carregamento de qualquer página deixa de fazer uma chamada de rede a um terceiro (Google) só para exibir texto. |

### ARQ-606 — Corrigir contraste do subtítulo de hero das páginas legais

| Campo | Valor |
|---|---|
| Objetivo | Levar o subtítulo de hero das páginas legais (`.page-header-subtitle`/`.hero-subtitle`) a atender WCAG AA (4.5:1) sem alterar a proeminência visual pretendida do elemento de forma perceptível. |
| Descrição | `legal-shared.css:139` declara `color: rgba(255, 255, 255, 0.68)` para o subtítulo, sobre um fundo em gradiente (`--primitive-green-950` 0% → `--primitive-green-800` 50% → `--primitive-green-700` 100%, `legal-shared.css:75-81`). Contraste calculado (`tests/support/contrast-audit.js`, achatando a rgba sobre cada stop do gradiente): 2.0:1 contra o stop mais escuro (`green-950`) e 1.64:1 contra o mais claro (`green-700`) — ambos muito abaixo do mínimo de 4.5:1 para texto normal (16px). Identificado na auditoria de contraste de ARQ-604 (Sprint 10); não corrigido naquela sprint porque a opacidade precisaria subir a um nível perceptualmente diferente (subtítulo muito mais opaco/proeminente) para cruzar o limiar em ~29 declarações `rgba(255,255,255,*)` distintas do mesmo arquivo (`legal-shared.css`), usadas em 34 páginas (`page-header-subtitle`/`hero-subtitle`) — ultrapassa o critério de "correção pontual e inequívoca" da Sprint 10. |
| Origem | Achado da auditoria de ARQ-604 (Sprint 10) — não catalogado em `12-technical-debt.md`, não fazia parte do escopo original de ARQ-604 |
| Documento | `16-architecture-backlog.md` (este item), `06-design-system.md` |
| Item da dívida técnica | N/A — achado novo, identificado nesta sprint |
| Arquivos afetados | `public/assets/css/legal-shared.css` (possivelmente introduzindo um token semântico novo, ex. `--color-text-inverse-muted`, em vez de literais `rgba()` espalhados — decisão de design a confirmar) |
| Dependências (depende de) | Nenhuma dependência técnica; decisão de design sobre até onde a opacidade pode subir sem descaracterizar a hierarquia visual do hero |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Decisão de design: nível de opacidade/cor final aceitável para o subtítulo (e, possivelmente, para a família mais ampla de textos translúcidos brancos do mesmo arquivo — pills, divisores, textos de SVG) |
| Critérios de Aceite | `.page-header-subtitle`/`.hero-subtitle` ≥ 4.5:1 contra o stop mais claro do gradiente (`--primitive-green-700`, pior caso) |
| Critérios de Regressão | Nenhuma mudança perceptível na hierarquia visual do hero além do necessário para o contraste; regressão visual revisada via `tests/visual-contrast.spec.ts` (baseline já cobre a página legal usada como referência) |
| Impacto | Médio (34 páginas afetadas, mas é subtítulo — não impede leitura do conteúdo principal) |
| Risco | Médio (mudança visual perceptível é o próprio motivo do adiamento — qualquer correção aqui precisa ser sinalizada explicitamente antes de aplicar, conforme regra de evidência de ARQ-604) |
| Complexidade | Baixa-Média (mecânica, mas depende de decisão de design prévia) |
| Estimativa | P-M |
| Responsável | Frontend + Design |
| Status | CONCLUÍDO (Sprint 15, 2026-07-25) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0:2 → 2:2 pares do subtítulo de hero atendendo WCAG AA (hoje: 0/2, contra os dois stops extremos do gradiente) — **atingido: 2/2** |
| Observações | Mesma disciplina de escopo de ARQ-605 (headings, Sprint 8): achado real, registrado no mesmo momento em que foi identificado, não corrigido às pressas. **Decisão de design (Sprint 15)**: entre as 3 opções concretas levantadas e apresentadas ao responsável pelo projeto com evidência visual (só opacidade / cor sólida / `text-shadow`), foi escolhida a **Opção 1 — só opacidade**: `rgba(255,255,255,0.68)` → `rgba(255,255,255,0.78)` em `legal-shared.css:139`, único ponto de declaração de `.page-header-subtitle`/`.page-header--legal .hero-subtitle` (não os ~29 `rgba(255,255,255,*)` do arquivo — esses são elementos distintos, fora do escopo deste item). **Achado adicional durante o levantamento, fora do escopo original**: `tests/support/contrast-audit.js` tinha um bug de metodologia nos 2 pares "Legal hero subtitle" — comparava o branco nominal (`#ffffff`) contra a cor composta (`flatten(...)`) em vez da cor composta (texto efetivo) contra o fundo real (o stop do gradiente), que é como WCAG define contraste de texto translúcido sobre fundo opaco. Os outros 36 pares do script já usavam `flatten()` corretamente (translúcido é o *fundo*, não o texto, nesses casos). O bug não mudava o veredito (falhava nos dois métodos), mas subestimava a magnitude: pior caso real pré-correção era **3.94:1** (fórmula correta), não 1.64:1 como documentado acima — o que reduziu a opacidade mínima necessária para 4.5:1 de "perceptualmente bem mais opaco" para apenas `.68→.77` (usado `.78` com folga). Corrigido junto nesta sprint (mesmo commit dos dados/fórmula, não do CSS de produção). **Resultado**: `contrast-audit.js` → 38/38 pares (antes 36/38); pior stop (`green-700`) 4.62:1, melhor stop (`green-950`) 10.36:1. Regressão visual: `tests/visual-contrast.spec.ts` e `visual-radius-shadow.spec.ts` (página legal) permaneceram dentro do `maxDiffPixelRatio: 0.005` sem necessidade de atualizar baseline — mudança de opacidade é pequena o suficiente para não estourar a tolerância num screenshot de página inteira. `npm test`: 77/77 antes e depois, sem regressão. |

### ARQ-605 — Corrigir hierarquia de headings (h1-h6)

| Campo | Valor |
|---|---|
| Objetivo | Garantir que a ordem hierárquica de headings de cada página seja navegável sem saltos por tecnologia assistiva (ex. leitores de tela navegando por heading). |
| Descrição | A auditoria de landmarks/ARIA de [ARQ-602](#arq-602--auditoria-de-landmarksaria) (Sprint 8) verificou, como achado adjacente e de mesmo custo de checagem, a sequência de headings das 37 páginas reais. 5 páginas pulam nível: `ativos-digitais/index.html`, `empresas.html`, `governo.html` e `pessoas.html` têm ao menos um `<h4>` (ex. títulos de "impactBar") sem um `<h3>` intermediário sob o `<h2>` de seção pai; `legal/termos-de-uso.html` tem um `<h3>Índice</h3>` antes do primeiro `<h2>` da página (`<h1>` → `<h3>`, pulando `<h2>`). Confirmado via varredura de todos os níveis de heading nas 37 páginas (script Python sobre `git ls-files public/*.html`, excluindo partials). |
| Origem | Achado da auditoria de ARQ-602 (Sprint 8) — não catalogado em `12-technical-debt.md`, não fazia parte do escopo original de ARQ-602 |
| Documento | `16-architecture-backlog.md` (este item) |
| Item da dívida técnica | N/A — achado novo, identificado nesta sprint |
| Arquivos afetados | `public/ativos-digitais/index.html`, `public/empresas.html`, `public/governo.html`, `public/pessoas.html`, `public/legal/termos-de-uso.html` |
| Dependências (depende de) | Nenhuma dependência técnica; depende de decisão de conteúdo/copy sobre a estrutura visual das seções afetadas (ver Observações) |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Decisão de conteúdo: se os títulos "impactBar" (h4) devem subir para h3, ou se falta um h3 de agrupamento; se "Índice" deve ser h2 |
| Critérios de Aceite | Nenhum salto de nível de heading nas 37 páginas reais (nível N não seguido diretamente por N+2 ou maior) |
| Critérios de Regressão | Nenhuma mudança visual não intencional — a hierarquia semântica deve mudar sem alterar a apresentação visual atual (pode exigir CSS explícito por classe em vez de estilo implícito por nível de tag) |
| Impacto | Baixo-Médio (achado comum de auditoria de acessibilidade; não impede o uso, mas degrada a navegação por heading) |
| Risco | Baixo |
| Complexidade | Baixa-Média (mecânica por página, mas exige decisão de conteúdo por não ser corrigível só por atributo) |
| Estimativa | P-M |
| Responsável | Frontend |
| Status | CONCLUÍDO (Sprint 15, 2026-07-25) |
| ADR relacionado | Nenhum (a criar em ARQ-701) |
| Métrica de sucesso | 0 saltos de nível de heading nas 37 páginas (hoje: 5 páginas com salto) — **atingido: 0/5 nas 5 páginas remapeadas contra o código atual (confirmado, não a mesma varredura da Sprint 8)** |
| Observações | Não corrigido em Sprint 8 (ARQ-602) por exigir decisão de conteúdo/copy — ver regra de evidência da própria sprint: mudar o nível de um heading que já tem estilo visual associado à tag (ex. `<h4>` com estilo de "impactBar") pode mudar a apresentação se não for acompanhado de ajuste de CSS por classe, o que ultrapassa "só o atributo". Registrado como item novo e rastreável no mesmo momento em que foi identificado, conforme EP-17 de `18-engineering-principles.md`. **Decisão de design (Sprint 15)**: mapeadas as 5 páginas contra o HTML atual (não presumido da Sprint 8) — cada página tinha exatamente 1 salto, não múltiplos. 4 seguiam o mesmo padrão (`<h2>` de seção → `<h4>` em cartões de destaque, sem `<h3>` intermediário: "impacto-bar" em `ativos-digitais/index.html`, "impactBar"/`.sol-bar` em `empresas.html`/`governo.html`/`pessoas.html`); a 5ª era distinta (`<h1>` → `<h3>Índice</h3>` em `termos-de-uso.html`, antes do primeiro `<h2>`). Apresentadas 2 opções por salto (ajuste semântico vs. ajuste completo) com preview real; o responsável pelo projeto escolheu **ajuste completo para as 5 páginas** — a tag E o estilo visual sobem juntos para refletir a nova posição hierárquica, o que **substitui explicitamente** o Critério de Regressão originalmente escrito acima ("nenhuma mudança visual não intencional") por uma mudança visual pequena e deliberadamente aprovada. Mudanças aplicadas: (1) `ativos-digitais/index.html`, 4× `<h4>`→`<h3>` (Acesso/Titularidade/Comprovação/Rastreabilidade) + `assets-digital.css` (`.impacto-bar h4`→`.impacto-bar h3`, `.9375rem/600`→`1rem/700`, igualando o H3 já usado na página em `.muda-aside h3`); (2) `empresas.html`/`governo.html`/`pessoas.html`, 11× `<h4>`→`<h3>` (blocos `impactBar`) + `solucoes.css` (`.sol-bar-text h4`→`.sol-bar-text h3`, `.9rem`→`1.05rem`, igualando o H3 padrão de `body.solucoes-page h3`, peso 600 inalterado); (3) `legal/termos-de-uso.html`, `<h3>Índice</h3>`→`<h2>Índice</h2>`, sem CSS novo — herda automaticamente o estilo padrão de `.text-block-inner h2` (borda verde à esquerda) já usado por "Introdução" e as demais seções da página. Checkpoint de diff visual revisado a cada lote (captura antes/depois via `npm run dev` + Playwright, não `python3 -m http.server`). `tests/visual-contrast.spec.ts` e `tests/visual-radius-shadow.spec.ts` acusaram diferença esperada em "Cluster Ativos Digitais: viewport completo" (página cresceu 5px pela mudança de peso/tamanho dos H3, deslocando o restante do layout) — diff revisado manualmente (cascata uniforme de 5px, sem quebra de layout), baseline regenerado (`--update-snapshots`, escopo restrito a esse teste). Nenhum teste cobre `empresas.html`/`governo.html`/`pessoas.html` visualmente (confirmado por grep antes da mudança), então o Lote 2 não tinha baseline a atualizar. `npm test`: 77/77 antes e depois. |

### ARQ-607 — Auditoria de conteúdo "DOM presente ≠ visível" e teste de visibilidade real permanente

| Campo | Valor |
|---|---|
| Objetivo | Confirmar que nenhum outro elemento do site sofre do mesmo padrão de defeito do bug de produção corrigido na Sprint 26 (conteúdo presente no DOM mas nunca revelado, por depender de um mecanismo de visibilidade — scroll, `IntersectionObserver` — que só existe no contexto de origem do HTML, não no contexto onde esse HTML é reaproveitado) e instituir teste de regressão permanente que verifique visibilidade real (`toBeVisible`/opacity computado), não só presença no DOM (`toBeAttached`). |
| Descrição | Sprint 26 corrigiu, já em produção, o modal de política de privacidade em `/diagnostico`: `loadPrivacyPolicyContent()` (`diagnostico.js`) clona `.text-block` de `/legal/politica-de-privacidade.html` para dentro do modal; essas seções carregam a classe `.reveal-on-scroll` (`opacity: 0` até um `IntersectionObserver` da página de origem adicionar `.visible`), e o clone ia para o modal sem esse observer — o texto, incluindo o de consentimento que o backend passou a exigir na mesma sprint, nunca era revelado ao usuário. Nenhum teste da suíte verificava visibilidade real; só presença no DOM — por isso o bug ficou indetectado por tempo indeterminado. Esta sprint (1) mapeou toda a superfície do site com o mesmo padrão de risco — clone/reuso de HTML entre contextos (`grep` exaustivo por `cloneNode`/`DOMParser`: única ocorrência em todo o repositório é a já corrigida), dropdowns (`tests/navigation.spec.ts` já cobre `aria-expanded`/classe `open`, mas não `toBeVisible`), `reveal-on-scroll`/`IntersectionObserver` nas 8 páginas legais (mecanismo roda no mesmo contexto que o declara — padrão diferente do bug, risco baixo), conteúdo carregado via `fetch` (busca — mesmo contexto; i18n dinâmico — já teria efeito colateral visível diferente, texto vazio/chave crua, não opacity 0) — e (2) não encontrou nenhuma outra ocorrência do padrão exato do bug. Criado `tests/content-visibility.spec.ts`: um teste navega o fluxo real do diagnóstico até abrir o modal e verifica `toBeVisible()` + `getComputedStyle(...).opacity > 0` em cada seção clonada (mais uma checagem explícita de que `reveal-on-scroll` não sobrevive ao clone — a classe exata do bug); outro cobre a página de origem (sanity do mecanismo compartilhado). Validado que o teste de fato detecta a regressão: correção revertida temporariamente (`clone.classList.remove('reveal-on-scroll')` comentada), teste falhou com o erro exato esperado, correção restaurada, teste voltou a passar. |
| Origem | Bug real encontrado e corrigido em produção na Sprint 26 (commit `c7a0ee6`); gap de cobertura de teste (só presença no DOM, nunca visibilidade real) identificado e fechado nesta sprint |
| Documento | `09-security.md` (bug original, seção do modal), `16-architecture-backlog.md` (este item) |
| Item da dívida técnica | N/A — achado novo, não catalogado em `12-technical-debt.md` |
| Arquivos afetados | `tests/content-visibility.spec.ts` (novo, 2 testes) |
| Dependências (depende de) | Nenhuma |
| Dependências (desbloqueia) | Nenhuma |
| Pré-requisitos | Nenhum |
| Critérios de Aceite | Teste de regressão permanente cobrindo visibilidade real (`toBeVisible` + opacity computado) do elemento que causou o bug original; auditoria com evidência de arquivo/linha confirmando ausência de outras ocorrências do mesmo padrão |
| Critérios de Regressão | Não aplicável (item de auditoria + teste; nenhuma correção de produto nova foi necessária — o único elemento de risco real já tinha sido corrigido na Sprint 26) |
| Impacto | Médio-Alto (a ausência deste tipo de teste foi a causa raiz de um bug de conteúdo de LGPD já em produção; item de prevenção de recorrência) |
| Risco | Baixo |
| Complexidade | Baixa (mapeamento + teste; nenhuma correção de produto nova encontrada) |
| Estimativa | P |
| Responsável | Engenharia + QA |
| Status | CONCLUÍDO (Sprint 27, 2026-07-28) |
| ADR relacionado | Nenhum |
| Métrica de sucesso | 100% dos elementos de risco real identificados cobertos por teste de visibilidade real — atingido: 1/1 (o modal, único elemento com o padrão exato do bug, agora coberto por `tests/content-visibility.spec.ts`) |
| Observações | Classificado no Épico 6 (Acessibilidade), não no Épico 4 (Consolidação): o defeito raiz — conteúdo presente no DOM mas não perceptível ao usuário — é escopo direto do princípio "Perceptível" de WCAG (Diretriz 1), o mesmo eixo de ARQ-601/602/604/605/606, não uma questão de consistência arquitetural genérica. **Mapa de risco completo (Bloco A)**: (1) *Modal de política de privacidade* (`diagnostico.html`/`diagnostico.js`) — mecanismo: clone de `.reveal-on-scroll` sem `IntersectionObserver` no novo contexto; risco: **mesmo padrão do bug** — já corrigido Sprint 26, agora com teste de regressão. (2) *8 páginas legais com `reveal-on-scroll`* (institucional, arquitetura-jurídica-prova-digital, fundamento-jurídico, termos-de-uso, política-de-privacidade, termos-de-custódia, preservação-probatória-digital, + `legal-animations.js` compartilhado) — mecanismo: mesmo `IntersectionObserver`, mas roda no mesmo contexto que o declara, nunca clonado; risco: **diferente do padrão do bug** (risco geral e pré-existente de progressive-enhancement sem JS, não introduzido por esta classe de defeito); nota incidental: `termos-de-uso.html` e as demais 6 páginas com script inline de reveal têm essa lógica duplicada com o `legal-animations.js` externo já compartilhado (ambos operam sobre os mesmos elementos, redundante mas inofensivo — candidato a limpeza de simplificação, não um bug, fora do escopo desta sprint). (3) *Dropdowns de navegação* (`tests/navigation.spec.ts`) — mecanismo: classe `open` + `aria-expanded`, aplicados no mesmo elemento que o CSS observa, nunca clonados; risco: **sem risco aparente** do padrão específico (testes já cobrem estado, ainda que não `toBeVisible` explicitamente). (4) *Busca* (`search.js`, `#searchPanel`) — resultados renderizados no mesmo contexto (`header`) que a classe `.search-widget.open` que os revela; risco: **sem risco aparente**. (5) *i18n dinâmico* (`data-i18n`/`data-i18n-html`, `i18n.js`) — elementos começam vazios e são preenchidos via `textContent`/`innerHTML` após `fetch`; um key ausente resulta em texto vazio ou (em `applyTranslations()`, páginas não-legais) na chave crua exibida — falha diferente do padrão do bug (ausência/erro de conteúdo, não opacity:0), já com efeito colateral visível o suficiente para ser notado sem depender de teste de opacidade; risco: **diferente do padrão do bug**, sem novo teste criado nesta sprint. (6) Achados incidentais fora do escopo desta sprint (nenhuma correção aplicada, registrados para triagem futura): chave de tradução `modal.title`/`modal.intro`/`modal.cancel`/`modal.proceed` existe em `pt.json`/`en.json`/`es.json` mas não é referenciada por nenhum `data-i18n` nem `I18N.t()` no código — tradução morta, sem elemento DOM correspondente (não é o padrão do bug: não há conteúdo invisível, há chave não utilizada); `governo.html` carrega um script inline de i18n duplicado e quebrado (`fetch('/assets/i18n/${lang}.json')`, caminho inexistente — os arquivos reais estão em `/assets/lang/`) que sempre falha silenciosamente (só `console.error`) em toda carga da página — inofensivo porque o `i18n.js` real (via `scripts.html`) já preenche os mesmos elementos corretamente antes/depois, mas gera erro de console permanente; nenhum dos dois é o padrão de defeito desta sprint (não causam conteúdo invisível), por isso não foram corrigidos aqui — candidatos a limpeza de dívida técnica menor em sprint futura. **Bloco B (testes)**: `tests/content-visibility.spec.ts` criado com 2 testes — cobertura do elemento de risco real (modal) validada por reversão controlada do fix (confirmado que o teste falha sem a correção e passa com ela). **Bloco C (correções)**: nenhum bug novo de visibilidade encontrado além do já corrigido na Sprint 26 — nada a corrigir. `npm test`: 90/92 → 94/94 (+2 testes novos, mesma baseline de falsos-positivos de sandbox já documentada, agora com baseline regenerada nesta sprint por mudança de conteúdo do rodapé — ver ARQ-4xx/observações do Bloco E desta mesma sprint). |

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
| Status | CONCLUÍDO (processo formalizado, Sprint 20, 2026-07-26) |
| ADR relacionado | Não aplicável (este item cria os ADRs) |
| Métrica de sucesso | Cobertura de ADR = 100% dos ARQs concluídos que envolveram decisão não-óbvia — **atingido para as 3 decisões represadas identificadas até esta sprint** (`ARQ-301`, `ARQ-302`, `ARQ-502`); cobertura de itens futuros depende de aplicação contínua do processo agora formalizado, não é um estado final. |
| Observações | Criado `docs/architecture/adr/` com `template.md` (formato leve: título, contexto, decisão, alternativas consideradas, consequências, status) e `README.md` (índice + critério de "quando criar um ADR", already definido em `docs/governance/18-engineering-principles.md`). Escritos 3 ADRs retroativos para as decisões que o próprio backlog já sinalizava como "candidata a ADR curto quando ARQ-701 formalizar o processo": [ADR-0001](adr/0001-nomenclatura-ad-pillar.md) (`ARQ-301`, nomenclatura `--ad-pillar-*`), [ADR-0002](adr/0002-breakpoint-tokens-fora-de-media.md) (`ARQ-302`, tokens `--breakpoint-*` fora de `@media`) e [ADR-0003](adr/0003-convencao-cache-busting.md) (`ARQ-502`, convenção de cache-busting). Nenhuma decisão foi reaberta ou reinvestigada — cada ADR só formaliza o "porquê" já registrado no campo Observações do item correspondente. Campo "ADR relacionado" de `ARQ-301`, `ARQ-302` e `ARQ-502` atualizado para apontar para o ADR criado. Item permanece um processo contínuo (não um estado final): novas decisões não-óbvias devem gerar ADR no momento em que são tomadas, não represadas para uma sprint futura. |

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
| Status | CONCLUÍDO (Sprint 20, 2026-07-26) |
| ADR relacionado | Nenhum (mudança operacional, não uma decisão arquitetural com alternativas — não atende ao critério de "quando criar um ADR" de `18-engineering-principles.md`) |
| Métrica de sucesso | Validação por um desenvolvedor externo à criação do documento — **pendente**: documento criado e revisado internamente nesta sprint, validação por um desenvolvedor que não participou da criação ainda não ocorreu (não há um segundo desenvolvedor humano no projeto neste momento); registrado como validação futura, não bloqueia o fechamento deste item pelos critérios já atendíveis nesta sprint. |
| Observações | Criado `CLAUDE.md` na raiz do repositório: comandos-chave (`npm run dev`, `npm test`, `node tests/support/generate-asset-versions.js`), regras permanentes de processo já estabelecidas nas sprints anteriores (servidor SSI obrigatório, regressão visual, disciplina de escopo/PR, perguntar antes de push, fluxo de branches), estrutura de pastas essencial, e referências para `16-architecture-backlog.md` (o que falta fazer), `docs/architecture/adr/` (por que decisões foram tomadas) e os documentos de `docs/governance/` (princípios/DoD/checklist). Deliberadamente enxuto — não duplica o conteúdo do Manifesto/Engineering Principles/Backlog, só referencia. |

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
`ARQ-601` a `ARQ-606`. Alinhado ao critério "WCAG AA" do Épico 6 do roadmap. `ARQ-601`–`ARQ-606` concluídos (Sprints 7–10, 15) — Épico 6 completo. `ARQ-605` e `ARQ-606` ficaram em BACKLOG até a Sprint 15 por dependerem de decisão de conteúdo/design, não de complexidade técnica; resolvidos após o responsável pelo projeto escolher entre as opções concretas apresentadas.

### Marco 5 — Governança Completa
`ARQ-701` a `ARQ-703`. Todo novo desenvolvedor compreende a arquitetura lendo apenas a documentação — critério de aceite explícito do Épico 7 do roadmap.

---

## Validação do Backlog

Checagem executada antes de finalizar este documento:

- [x] **Todos os 16 itens de dívida técnica de `12-technical-debt.md` possuem pelo menos um ARQ.** Mapeamento: #1→ARQ-201, #2→ARQ-101, #3→ARQ-102/103/104/105/106, #4→ARQ-405, #5→ARQ-202, #6→ARQ-301/303, #7→ARQ-406, #8→ARQ-601, #9→ARQ-404, #10→ARQ-302/304, #11→ARQ-501, #12→ARQ-502, #13→ARQ-402, #14→ARQ-401, #15→ARQ-403, #16→ARQ-107.
- [x] **Todos os 34 ARQs possuem responsável**, restrito às 9 categorias definidas.
- [x] **Todos os 34 ARQs possuem critérios de aceite** (mesmo os de auditoria/documentação, cujo critério é a publicação do achado).
- [x] **Todos os 34 ARQs possuem métrica de sucesso objetiva.**
- [x] **Não há duplicações de ID.** Cada ARQ aparece uma única vez no documento.
- [x] **Não há ARQs órfãos.** Todo ID citado em um campo "Dependências" corresponde a um item de fato definido neste backlog.
- [x] **Todas as dependências são consistentes** (nenhuma dependência circular; toda relação "depende de" tem uma contraparte "desbloqueia" no item referenciado, ou é uma dependência externa explícita ao repositório).
- [x] **Todos os 7 épicos têm backlog suficiente para execução independente**: Segurança (8 itens), SEO (3), Design System (4), Consolidação (6), Engenharia (5), Acessibilidade (5), Governança (3) — nenhum épico depende de detalhamento adicional para que um time comece a trabalhar.

Itens adicionados nesta etapa que não constavam do roadmap original (`15-architecture-roadmap.md`) nem do catálogo de dívida técnica numerado: `ARQ-107` (desdobrado do rótulo genérico "LGPD"), `ARQ-108`, `ARQ-203`, `ARQ-405`, `ARQ-406`, `ARQ-503`, `ARQ-505`. Todos rastreados explicitamente no campo "Origem" de cada item.

Item adicionado posteriormente, durante a execução do backlog (Sprint 8): `ARQ-605`, achado da auditoria de `ARQ-602`, rastreado no campo "Origem" do próprio item.

Item adicionado posteriormente, durante a execução do backlog (Sprint 10): `ARQ-606`, achado da auditoria de `ARQ-604` (subtítulo de hero das páginas legais sem contraste suficiente), rastreado no campo "Origem" do próprio item.
