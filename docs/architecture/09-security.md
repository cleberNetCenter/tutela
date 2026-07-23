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

Este é um site estático de conteúdo institucional/jurídico, sem autenticação própria e sem backend versionado neste repositório. A superfície de ataque diretamente controlada pelo código deste repositório é pequena: HTML/CSS/JS estáticos, um formulário (`/diagnostico/`) que envia dados para um endpoint externo ao repositório, e integrações com serviços de terceiros (Google Analytics, Google reCAPTCHA, Google Fonts). A maior parte da postura de segurança (headers HTTP, TLS, proxy) depende da configuração do Nginx no servidor, que **não é versionada neste repositório** — necessita validação direta no servidor para qualquer afirmação definitiva.

## Headers HTTP e CSP

Uma busca em todo o repositório (arquivos HTML, JS e JSON) por `Content-Security-Policy`, `X-Frame-Options`, `Strict-Transport-Security`, `Permissions-Policy` e `X-Content-Type-Options` não retornou nenhuma ocorrência. **Não identificado no projeto.**

Isso não significa necessariamente que esses headers estejam ausentes em produção — segundo `docs/ambientes-e-deploy.md:116-118`, a configuração ativa do Nginx *"não é mais versionada no repositório: ela é gerenciada diretamente nos servidores"*. Portanto, a existência (ou não) de CSP, HSTS, `X-Frame-Options` etc. **necessita validação** direta via `nginx -T` no servidor, ou via `curl -I` contra a produção, conforme o próprio runbook recomenda (`docs/ambientes-e-deploy.md:160-176`). O que é um fato verificável a partir do repositório é que **nenhum desses headers é definido pela aplicação em si** (não há middleware, não há `<meta http-equiv="Content-Security-Policy">` em nenhuma página).

`public/vercel.json` — que poderia ser o lugar natural para declarar headers caso a Vercel estivesse em uso — contém apenas `redirects`, nenhuma seção `headers`.

## Autenticação e autorização

Não identificado no projeto. Este repositório não implementa login, sessão, JWT, OAuth ou qualquer mecanismo de autenticação/autorização. O único ponto de contato com um sistema autenticado é um link de saída para uma aplicação externa: `https://app.tuteladigital.com.br/` (`public/partials/header.html:137`, aberto em nova aba com `rel="noopener noreferrer"` — uso correto para evitar *tabnabbing*). A autenticação real acontece nessa aplicação externa, fora do escopo deste repositório.

## Formulários e dados de usuário

O único formulário do site é o de `/diagnostico/` (`public/diagnostico.html`, lógica em `public/assets/js/diagnostico.js`). Campos coletados: nome, e-mail, respostas do questionário (score numérico) e consentimento (checkbox obrigatório, `#consentimento`). Fluxo de envio (`diagnostico.js:276-301`):

```js
fetch('/api/diagnostico', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ nome, email, score, token })
})
```

**Achado relevante**: `/api/diagnostico` não tem nenhuma implementação visível neste repositório (não é uma página estática, não há função serverless, não há proxy documentado). Isso significa que, do ponto de vista deste código-fonte, é impossível auditar como os dados pessoais (nome, e-mail) são processados, armazenados ou protegidos no destino — necessita validação com a equipe responsável pela infraestrutura do endpoint. Esse ponto é especialmente relevante dado que o site é de uma empresa de custódia jurídica que promete conformidade com a LGPD (citada em `public/index.html:211` e ao longo do conteúdo institucional) — a coleta de dados pessoais pelo próprio formulário do site deveria, no mínimo, ter seu tratamento documentado e auditável.

O botão de envio só é habilitado quando nome (≥3 caracteres), e-mail (validação simplista: contém `@` e `.`, sem regex robusta — `diagnostico.js:87-89`), consentimento marcado e reCAPTCHA resolvido, todos verdadeiros simultaneamente (`diagnostico.js:91-98`). Essa é uma validação **apenas no cliente**; não há como confirmar validação equivalente no servidor a partir deste repositório — necessita validação.

## CAPTCHA

Google reCAPTCHA v2 (checkbox), com site key exposta diretamente no HTML: `public/diagnostico.html:289` (`data-sitekey="6Lcp7pcsAAAAAJFgWGRYjp6t_2QlcFbgJUlZrUNx"`). Isso é esperado e seguro — a "site key" do reCAPTCHA é pública por design (a chave secreta correspondente, usada na verificação server-side, não está e não deveria estar neste repositório; sua ausência aqui é o comportamento correto). O idioma do widget é recarregado dinamicamente conforme o idioma ativo do i18n (`diagnostico.js:196-219`).

## Cookies e armazenamento local

- `localStorage.setItem('tutela_lang', lang)` — único uso de armazenamento client-side persistente identificado, guardando a preferência de idioma (`i18n.js:183`, lido em `i18n.js:49` e `search.js:108`). Não é um dado sensível.
- Não foi identificado nenhum uso de `document.cookie` no código-fonte deste repositório. Não identificado no projeto.
- Não há banner de consentimento de cookies (cookie banner/CMP) no HTML analisado — apesar de o Google Analytics (que tipicamente usa cookies próprios, `_ga`) estar presente em todas as páginas (`public/index.html:46-54`). Isso é uma lacuna potencial de conformidade LGPD/GDPR — necessita validação jurídica, fora do escopo técnico desta análise, mas registrada como fato observável em [12-technical-debt.md](12-technical-debt.md).

## CORS

Não identificado no projeto. Não há configuração de CORS no repositório (nem headers `Access-Control-Allow-Origin`, nem `fetch` com `mode: 'cors'` explícito além do padrão do navegador). Os `fetch` existentes (`i18n.js`, `search.js`) são todos para o mesmo domínio (`/assets/...`), o que não exige CORS. O único `fetch` cross-origin conceitual é `/api/diagnostico`, mas como o path é relativo (`/api/diagnostico`, não uma URL absoluta de outro domínio), presume-se que seja resolvido pelo mesmo host via proxy reverso do Nginx — necessita validação, pois a implementação real do endpoint está fora do repositório.

## Variáveis sensíveis e segredos

Nenhum arquivo `.env`, chave de API privada, token ou credencial foi encontrado no repositório (buscas por padrões comuns de chave — ex. `AIza...`, `sk_live`, `AKIA...` — não retornaram resultados). Segredos de deploy (`GITHUB_TOKEN` usado em `.github/workflows/sitemap.yml` para disparar o redeploy de homolog) são gerenciados via GitHub Secrets nativo do Actions, não versionados em texto plano — prática correta.

## Sanitização e XSS

- `search.js` usa uma função `escapeHtml` própria (via `div.textContent`/`div.innerHTML`) antes de injetar trechos de resultado de busca no DOM (`search.js:111-127`), o que mitiga XSS refletido a partir de conteúdo do próprio índice de busca (que é gerado por CI a partir do HTML do site, não de input de usuário).
- O rótulo do rodapé com `data-i18n-html="true"` (`public/partials/footer.html:60`, texto de patente pendente) é o único ponto em que `i18n.js` usa `el.innerHTML = translation` em vez de `textContent` (`i18n.js:92`). Como a fonte desse HTML são os arquivos `lang/*.json` versionados no próprio repositório (não input de usuário em runtime), o risco prático de XSS aqui é baixo, mas é um padrão a vigiar caso `data-i18n-html` seja reutilizado no futuro para conteúdo menos controlado.
- O formulário de diagnóstico não faz sanitização perceptível de `nome`/`email` no cliente além da checagem trivial de formato — a responsabilidade de sanitização do lado servidor recai sobre o endpoint `/api/diagnostico`, não auditável a partir deste repositório.

## Dependências e superfície de ataque

Como não há dependências de runtime (nenhuma biblioteca JS de terceiros é importada nas páginas, apenas scripts de terceiros carregados via `<script src>` direto de CDNs do Google), a superfície de ataque via *supply chain* de pacotes npm é mínima — o único artefato de tooling (`@playwright/test`) é uma dependência de desenvolvimento não utilizada em nenhum teste versionado (ver [12-technical-debt.md](12-technical-debt.md)) e não afeta o site em produção.

## Documentos relacionados
- [11-build-deploy.md](11-build-deploy.md) — TLS, Nginx e segredos de CI/CD.
- [12-technical-debt.md](12-technical-debt.md) — priorização dos achados de segurança.
