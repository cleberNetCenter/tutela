# 09 — Segurança

## Índice
- [Resumo](#resumo)
- [Headers HTTP e CSP](#headers-http-e-csp)
- [Autenticação e autorização](#autenticação-e-autorização)
- [Formulários e dados de usuário](#formulários-e-dados-de-usuário)
- [CAPTCHA](#captcha)
- [Cookies e armazenamento local](#cookies-e-armazenamento-local)
- [CORS](#cors)
- [Variáveis sensíveis e segredos](#variáveis-sensíveis-e-segredos)
- [Sanitização e XSS](#sanitização-e-xss)
- [Dependências e superfície de ataque](#dependências-e-superfície-de-ataque)

## Resumo

Este é um site estático de conteúdo institucional/jurídico, sem autenticação própria e sem backend versionado neste repositório. A superfície de ataque diretamente controlada pelo código deste repositório é pequena: HTML/CSS/JS estáticos, um formulário (`/diagnostico/`) que envia dados para um endpoint externo ao repositório, e integrações com serviços de terceiros (Google Analytics, Google reCAPTCHA). A maior parte da postura de segurança (headers HTTP, TLS, proxy) depende da configuração do Nginx no servidor, que **não é versionada neste repositório** — necessita validação direta no servidor para qualquer afirmação definitiva. **Atualização (ARQ-604)**: Google Fonts deixou de ser uma integração de terceiro — as fontes (Inter, Cormorant Garamond, Playfair Display, Source Serif 4, DM Mono) foram vendorizadas em `public/assets/fonts/` e são servidas pela própria origem, sem chamada de rede à CDN do Google.

Desde a Sprint 25 (`ARQ-101`), o backend de `/api/diagnostico` é auditável: versionado em `github.com/cleberNetCenter/tutela-api` (privado, ver `docs/ambientes-e-deploy.md:34`). Fatos e lacunas levantados por evidência de código estão na seção [Formulários e dados de usuário](#formulários-e-dados-de-usuário). Esta auditoria é técnica — não constitui determinação de conformidade LGPD, que exige avaliação jurídica dos fatos aqui documentados.

## Headers HTTP e CSP

Uma busca em todo o repositório (arquivos HTML, JS e JSON) por `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security`, `Permissions-Policy` e `X-Content-Type-Options` não retorna nenhuma ocorrência — **nenhum desses headers é definido pela aplicação em si** (não há middleware, não há `<meta http-equiv="Content-Security-Policy">` em nenhuma página). A configuração ativa do Nginx não é versionada neste repositório — é gerenciada diretamente nos servidores, e o `nginx -T`/`curl -I` executado neles é a fonte de verdade.

Essa configuração-fonte foi auditada diretamente nos dois servidores (`tutela-web`/produção, `tutela-dev`/homologação) via `nginx -T`/`curl -I`, inicialmente em 2026-07-24 (ARQ-108) e reconfirmada/atualizada em 14/08/2026. Estado confirmado por esses headers:

| Header | Produção | Homologação |
| --- | --- | --- |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains; preload` | ausente |
| `X-Frame-Options` | `SAMEORIGIN` | `SAMEORIGIN` |
| `X-Content-Type-Options` | `nosniff` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `camera=(), microphone=(), geolocation=()` | `camera=(), microphone=(), geolocation=()` |
| `Content-Security-Policy-Report-Only` | substituído pelo header de enforcement (ver linha abaixo) | ativo (política completa em `docs/ambientes-e-deploy.md`, seção "CSP Report-Only (ARQ-102)") |
| `Content-Security-Policy` (modo bloqueante) | **ativo desde 17/08/2026** — mesma política do Report-Only, sem sufixo (ver `docs/ambientes-e-deploy.md`, seção "CSP promovido para modo bloqueante em produção (ARQ-102)") | ausente (segue em Report-Only) |

Detalhamento item a item, incluindo a evidência de config-fonte e o histórico de cada auditoria, está em `16-architecture-backlog.md` (ARQ-102 a ARQ-106, ARQ-108) e em `docs/ambientes-e-deploy.md` (seção "Nginx"). CSP em modo bloqueante está `CONCLUÍDO` em produção (ARQ-102, 17/08/2026, após período de observação sem violações); homologação segue em Report-Only.

`public/vercel.json` — que poderia ter sido o lugar natural para declarar headers caso a Vercel estivesse em uso — continha apenas `redirects`, nenhuma seção `headers`; removido na Sprint 6 (ARQ-403) por estar comprovadamente inerte (ver [12-technical-debt.md](12-technical-debt.md)).

## Autenticação e autorização

Não identificado no projeto. Este repositório não implementa login, sessão, JWT, OAuth ou qualquer mecanismo de autenticação/autorização. O único ponto de contato com um sistema autenticado é um link de saída para uma aplicação externa: `https://app.tuteladigital.com.br/` (`public/partials/header.html:137`, aberto em nova aba com `rel="noopener noreferrer"` — uso correto para evitar *tabnabbing*). A autenticação real acontece nessa aplicação externa, fora do escopo deste repositório.

## Formulários e dados de usuário

O único formulário do site é o de `/diagnostico/` (`public/diagnostico.html`, lógica em `public/assets/js/diagnostico.js`). Campos coletados no cliente: nome, e-mail, respostas do questionário (score numérico) e consentimento (checkbox obrigatório, `#consentimento`, com modal de leitura da política de privacidade — `diagnostico.html:266-281,326-348`). Fluxo de envio (`diagnostico.js:276-301`):

```js
fetch('/api/diagnostico', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ nome, email, score, token })
})
```

**Nota**: o campo `nivel` (nível de risco) é calculado e exibido só no cliente (`diagnostico.js:223-228`) e nunca é enviado no payload — o servidor o espera (`server.js:41`) mas sempre o recebe como `undefined`, refletindo no assunto do e-mail enviado (ex. "Novo diagnóstico - undefined", `server.js:81`). Bug de qualidade de dado, não de privacidade; fora do escopo de correção desta sprint (registrar como item de backlog separado se for corrigido).

**Achado relevante — resposta `fetch` não verifica status HTTP**: `diagnostico.js:299` chama `.then(() => renderResultado(score))` incondicionalmente após qualquer resposta HTTP resolvida (2xx **ou** 4xx/5xx) — `fetch()` só rejeita em falha de rede. Ou seja, se o backend rejeitar a submissão (ex. `403` de CAPTCHA inválido, `400` de validação, `500` de falha de SMTP), o usuário ainda vê a tela de "resultado" como se o envio tivesse sido bem-sucedido. Bug de UX/confiabilidade que também mascara falhas de entrega de dado; não corrigido nesta sessão por disciplina de escopo (LGPD, não funcionalidade), registrado aqui como fato observado.

### Backend `/api/diagnostico` (repositório `tutela-api`, auditado na Sprint 25 — `ARQ-101`)

Desde a Sprint 24 (`ARQ-507`), o backend está versionado em `github.com/cleberNetCenter/tutela-api` (privado; branches `main`= produção, `homolog`= homologação — ambas no mesmo commit `23f0cb9` no momento desta auditoria). Fatos levantados com evidência de arquivo/linha desse repositório (`server.js`, commit `23f0cb9`, salvo onde indicado):

- **Coleta**: `nome`, `email`, `score`, `nivel` (sempre vazio, ver acima) e `token` (reCAPTCHA) recebidos via `req.body` (`server.js:41`). O IP é capturado explicitamente por código próprio (`req.ip`, `server.js:72`), não só via log de acesso do Nginx — mas o app **não** declara `app.set('trust proxy', ...)` em nenhum lugar do arquivo; como a API roda atrás do Nginx (`proxy_pass http://api:3000`, ver `docs/ambientes-e-deploy.md`), `req.ip` tende a refletir o IP interno do container Nginx na rede Docker, não o IP público real do visitante — não confirmado empiricamente (sem acesso ao servidor para inspecionar `logs/leads.jsonl` real), mas é o comportamento padrão documentado do Express nessa topologia. Ver também o efeito colateral em rate limiting, abaixo.
- **Validação servidor**: CAPTCHA validado contra a API do Google antes de qualquer outro processamento (`validarCaptcha()`, `server.js:44,101-118`); presença de `nome`/`email` checada (`server.js:51-53`); e-mail validado apenas por `.includes("@")` (`server.js:55-57`, mesma fragilidade do cliente); corpo da requisição limitado a 10kb (`express.json({ limit: "10kb" })`, `server.js:13`); nenhuma sanitização/normalização de `nome`/`email` além disso; nenhuma validação de tamanho/tipo para `score`/`nivel`. `helmet()` ativo (`server.js:12`, headers de segurança HTTP padrão do framework). Rate limit de 50 requisições/15min por IP em todo `/api/` (`server.js:16-20`) — sujeito à mesma imprecisão de IP citada acima (se `req.ip` for sempre o IP interno do Nginx, o limite passa a ser efetivamente compartilhado entre todos os visitantes, não por pessoa).
- **Armazenamento**: `logs/leads.jsonl`, caminho relativo ao `WORKDIR /app` do container (`Dockerfile:3,10`) — portanto `/app/logs/leads.jsonl` dentro do container. Formato: uma linha JSON por registro (`data`, `nome`, `email`, `score`, `nivel`, `ip`), texto plano, sem criptografia em repouso (`server.js:59-75`). Sem rotação ou limite de tamanho no código da aplicação. `Dockerfile` não declara `USER` — o processo Node roda como `root` dentro do container, então o arquivo é criado com o dono/permissão padrão de `root` (não confirmado o valor exato de `umask`/modo do arquivo — necessita acesso ao servidor). Permissões reais em disco, se `logs/` está montado como volume persistente do host, e rotação/backup a nível de SO: **não verificável a partir do código — necessita acesso SSH ao servidor**, que não estava disponível nesta sessão.
- **Transmissão (SMTP)**: `nodemailer` para `SMTP_HOST`/`SMTP_PORT` (Zoho, porta 587) com credenciais via variável de ambiente (`server.js:23-31`) — confirmado que não há credencial hardcoded. **Correção aplicada nesta sessão** (ver abaixo): `secure:false` sem `requireTLS` permitia fallback silencioso para conexão em texto plano caso o STARTTLS fosse bloqueado/removido por um MITM; `requireTLS: true` adicionado para que a conexão falhe em vez de degradar. Conexão do navegador ao próprio site (onde o formulário roda) depende do TLS do Nginx, já coberto por HSTS confirmado em produção (`ARQ-505`/`ARQ-108`) — não re-verificado nesta sessão.
- **Retenção**: nenhuma rotina de expurgo, TTL ou expiração de `logs/leads.jsonl` encontrada no código (`tutela-api`, 4 arquivos no total, revisados integralmente). **Lacuna**: dados de lead ficam retidos indefinidamente, salvo processo manual não documentado em nenhum repositório.
- **Acesso**: dentro do container, apenas o processo do `api` lê/escreve `logs/leads.jsonl` e `.env` — nenhum outro serviço do `docker-compose.yml` (apenas `nginx`+`api`, por `ARQ-505`) monta ou acessa esse caminho, pelo que a topologia documentada mostra. Acesso a nível de host (backup, outros processos, quem tem SSH aos servidores) **não verificável a partir do código**.
- **Consentimento**: ao contrário do que uma leitura só do backend sugeriria, o frontend **tem** checkbox de opt-in obrigatório com link para a política de privacidade completa (`diagnostico.html:266-281`, `diagnostico.js:92,97,145-192`) — o botão de envio fica desabilitado sem o consentimento marcado. **Porém**: (1) o consentimento é reforçado **só no cliente** — o payload enviado ao servidor (`diagnostico.js:297`) não inclui nenhum campo de consentimento, e o servidor não o valida (`server.js:41,51-57`); uma chamada direta a `/api/diagnostico` (curl/script), sem passar pela UI, é processada normalmente sem qualquer registro de consentimento. (2) O texto da política de privacidade vinculado (`public/legal/politica-de-privacidade.html`) descreve o tratamento de dados no contexto do produto de **custódia de ativos digitais** (seções 1–3, 5) — não menciona em nenhum ponto o formulário de diagnóstico, os campos coletados por ele (nome/e-mail/score/IP), o envio por e-mail via SMTP, ou o reCAPTCHA/Analytics como destinatários de dados. É um fato verificável por leitura direta do documento, não uma inferência.
- **Direito de exclusão/portabilidade**: `tutela-api` expõe só `/api/health` e `/api/diagnostico` (`server.js:34,39`) — nenhum endpoint técnico de exclusão/portabilidade. A política de privacidade (seção 7, "Direitos do Titular") descreve um canal de contato genérico (`contato@tuteladigital.com.br`, seção 11) como processo manual para exercício de direitos LGPD, mas escrito no contexto do produto de custódia, sem menção explícita aos dados do formulário de diagnóstico. **Lacuna**: nenhum mecanismo técnico ou processo documentado especificamente para excluir um registro de `logs/leads.jsonl`.
- **Terceiros**: (1) Google reCAPTCHA — token verificado contra `https://www.google.com/recaptcha/api.js` (cliente) e `https://www.google.com/recaptcha/api/siteverify` (servidor, `server.js:103`); segredo via `RECAPTCHA_SECRET` env var. (2) Zoho — provedor SMTP (`smtp.zoho.com`, confirmado em `ARQ-507`), recebe nome/e-mail/score/IP como corpo do e-mail em cada submissão. Nenhum outro serviço (analytics, CRM, webhook) identificado no código do `api` — confirmado por leitura integral dos 4 arquivos do repositório (`server.js`, `package.json`, `Dockerfile`, `.gitignore`); nenhuma outra chamada de rede além de `siteverify` e SMTP.
- **Homologação — dados reais vs. fictícios**: até a Sprint 24, o proxy `/api/` não existia no Nginx de homologação (`ARQ-507`, corrigido) — hoje o proxy está ativo. Porém, o `.env` de homologação tem `RECAPTCHA_SECRET` **vazio** (gap pré-existente, não corrigido — `ARQ-507`, Observações): qualquer submissão real em homologação falha na validação de CAPTCHA (`server.js:44-48`) **antes** de chegar ao log ou ao e-mail — ou seja, hoje, submissões em homologação não persistem em `logs/leads.jsonl` nem dão origem a e-mail, mesmo que um usuário real preencha nome/e-mail reais no formulário. Ressalva: o corpo da requisição (incluindo nome/e-mail reais, se digitados) ainda trafega por HTTPS até o processo do `api` em homologação antes de ser descartado em memória — não fica persistido, mas passa pela rede e pelo processo do servidor. Combinado com o bug de `fetch` sem checagem de status (acima), o usuário em homologação vê a tela de "sucesso" mesmo com o envio rejeitado — o formulário nunca funcionou de ponta a ponta em homologação, mas aparenta funcionar.

**Correção técnica de baixo risco aplicada nesta sessão**: `requireTLS: true` adicionado ao transporte SMTP (`tutela-api/server.js`, branch `homolog`, commit local não publicado — aguardando decisão de push). Nenhuma outra mudança de código foi aplicada: itens de retenção, texto de consentimento e mecanismo de exclusão são decisões de política de privacidade, não corrigidas nesta sessão por instrução explícita do escopo desta sprint.

O botão de envio só é habilitado no cliente quando nome (≥3 caracteres), e-mail (validação simplista: contém `@` e `.`, sem regex robusta — `diagnostico.js:87-89`), consentimento marcado e reCAPTCHA resolvido, todos verdadeiros simultaneamente (`diagnostico.js:91-98`). Essa validação é **só no cliente**; o servidor, auditado nesta sprint, replica a mesma fragilidade de validação de e-mail e não valida consentimento (ver acima).

## CAPTCHA

Google reCAPTCHA v2 (checkbox), com site key exposta diretamente no HTML: `public/diagnostico.html:289` (`data-sitekey="6Lcp7pcsAAAAAJFgWGRYjp6t_2QlcFbgJUlZrUNx"`). Isso é esperado e seguro — a "site key" do reCAPTCHA é pública por design (a chave secreta correspondente, usada na verificação server-side, não está e não deveria estar neste repositório; sua ausência aqui é o comportamento correto). O idioma do widget é recarregado dinamicamente conforme o idioma ativo do i18n (`diagnostico.js:196-219`).

## Cookies e armazenamento local

- `localStorage.setItem('tutela_lang', lang)` — único uso de armazenamento client-side persistente identificado, guardando a preferência de idioma (`i18n.js:183`, lido em `i18n.js:49` e `search.js:108`). Não é um dado sensível.
- Não foi identificado nenhum uso de `document.cookie` no código-fonte deste repositório. Não identificado no projeto.
- Não há banner de consentimento de cookies (cookie banner/CMP) no HTML analisado — apesar de o Google Analytics (que tipicamente usa cookies próprios, `_ga`) estar presente em todas as páginas (`public/index.html:46-54`). Isso é uma lacuna potencial de conformidade LGPD/GDPR — necessita validação jurídica, fora do escopo técnico desta análise, mas registrada como fato observável em [12-technical-debt.md](12-technical-debt.md).

## CORS

Não identificado no projeto. Não há configuração de CORS neste repositório (nem headers `Access-Control-Allow-Origin`, nem `fetch` com `mode: 'cors'` explícito além do padrão do navegador). Os `fetch` existentes (`i18n.js`, `search.js`) são todos para o mesmo domínio (`/assets/...`), o que não exige CORS. `/api/diagnostico` usa path relativo, resolvido pelo mesmo host via proxy reverso do Nginx (`proxy_pass http://api:3000`, confirmado em `docs/ambientes-e-deploy.md` e `ARQ-507`) — mesma origem, não é uma chamada cross-origin real. `tutela-api/server.js` (auditado na Sprint 25, `ARQ-101`) também não declara nenhum middleware de CORS (`cors`, `Access-Control-Allow-Origin`) — consistente com a topologia de mesma origem via proxy.

## Variáveis sensíveis e segredos

Nenhum arquivo `.env`, chave de API privada, token ou credencial foi encontrado no repositório (buscas por padrões comuns de chave — ex. `AIza...`, `sk_live`, `AKIA...` — não retornaram resultados). Segredos de deploy (`GITHUB_TOKEN` usado em `.github/workflows/sitemap.yml` para disparar o redeploy de homolog) são gerenciados via GitHub Secrets nativo do Actions, não versionados em texto plano — prática correta.

## Sanitização e XSS

- `search.js` usa uma função `escapeHtml` própria (via `div.textContent`/`div.innerHTML`) antes de injetar trechos de resultado de busca no DOM (`search.js:111-127`), o que mitiga XSS refletido a partir de conteúdo do próprio índice de busca (que é gerado por CI a partir do HTML do site, não de input de usuário).
- O rótulo do rodapé com `data-i18n-html="true"` (`public/partials/footer.html:60`, texto de patente pendente) é o único ponto em que `i18n.js` usa `el.innerHTML = translation` em vez de `textContent` (`i18n.js:92`). Como a fonte desse HTML são os arquivos `lang/*.json` versionados no próprio repositório (não input de usuário em runtime), o risco prático de XSS aqui é baixo, mas é um padrão a vigiar caso `data-i18n-html` seja reutilizado no futuro para conteúdo menos controlado.
- O formulário de diagnóstico não faz sanitização perceptível de `nome`/`email` no cliente além da checagem trivial de formato. Auditado na Sprint 25 (`ARQ-101`): o servidor (`tutela-api/server.js`) também não sanitiza `nome`/`email` além de checagem de presença e `.includes("@")` — sem escape/normalização, sem limite de tamanho por campo (só limite de 10kb no corpo inteiro). `nome`/`email`/`score` são inseridos apenas no corpo de texto plano do e-mail (`server.js:82-89`) e como valores de campo JSON no log (`server.js:66-73`), não em contexto HTML/SQL/shell — risco de XSS/SQLi não se aplica diretamente a este fluxo, mas a ausência de validação de formato/tamanho permanece uma lacuna de robustez de entrada.

## Dependências e superfície de ataque

Como não há dependências de runtime (nenhuma biblioteca JS de terceiros é importada nas páginas, apenas scripts de terceiros carregados via `<script src>` direto de CDNs do Google), a superfície de ataque via *supply chain* de pacotes npm é mínima — o único artefato de tooling (`@playwright/test`) é uma dependência de desenvolvimento não utilizada em nenhum teste versionado (ver [12-technical-debt.md](12-technical-debt.md)) e não afeta o site em produção.

## Documentos relacionados
- [11-build-deploy.md](11-build-deploy.md) — TLS, Nginx e segredos de CI/CD.
- [12-technical-debt.md](12-technical-debt.md) — priorização dos achados de segurança.
