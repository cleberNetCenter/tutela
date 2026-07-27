# Ambientes, deploy e Nginx — Tutela

Este runbook descreve o que está confirmado no repositório `cleberNetCenter/tutela` e identifica explicitamente o que deve ser conferido no servidor. Não registre neste arquivo senhas, chaves SSH, tokens ou chaves privadas TLS.

## Arquitetura

```text
desenvolvedor
  ├─ push em homolog ─► GitHub Actions / runner [self-hosted, homolog]
  │                       ├─ /opt/tutela ← origin/homolog
  │                       └─ docker compose em /opt/tutela-v2 ─► :8080 ─► Nginx homolog
  └─ push em main ────► GitHub Actions / runner [self-hosted, production]
                          ├─ /var/www/tutela ← origin/main
                          └─ docker compose em /opt/tutela-v2 ─► :8080 ─► Nginx produção
                                                                            │
                                                                            ▼
                                               https://www.tuteladigital.com.br
```

O projeto é um site estático servido de `public/`. O repositório não contém `docker-compose.yml`: a definição efetiva do container é mantida em `/opt/tutela-v2` no servidor. Nginx faz TLS, redirecionamentos e proxy reverso para o serviço local.

## Ambientes

| Ambiente | Branch/fonte | Checkout no servidor | Gatilho | Uso |
| --- | --- | --- | --- | --- |
| Local | árvore de trabalho | servidor HTTP local | manual | desenvolvimento |
| Homologação | `homolog` | `/opt/tutela` | push em `homolog` | validação |
| Produção | `main` | `/var/www/tutela` | push em `main` | site público |

O hostname de produção confirmado no conteúdo e sitemap é `www.tuteladigital.com.br`. O hostname de homologação é **`homolog.tuteladigital.com.br`** — confirmado em 2026-07-24 via `curl -I https://homolog.tuteladigital.com.br/` (resposta `200`, `x-robots-tag: noindex, nofollow, noarchive`, ver [Auditoria externa (ARQ-108)](#auditoria-externa-arq-108-2026-07-24) abaixo).

## Desenvolvimento local

Pré-requisitos: Git, Node.js e navegador. Não use `file://`; execute o site por HTTP com o servidor de desenvolvimento do repositório (resolve os includes SSI de header/footer/scripts, assim como o Nginx faz em homologação/produção):

```bash
npm install
npm run dev
```

Acesse `http://localhost:8081/`. HTML, CSS, JavaScript, partials, idiomas e assets são entregues diretamente, sem build.

**Não use `python3 -m http.server` para verificar cabeçalho, navegação, rodapé ou qualquer página com partials.** Esse servidor não resolve `<!--#include virtual="..." -->` (SSI) — a página apareceria sem header/footer, com o comentário de include cru no lugar. Serve apenas para o caso raro de abrir um arquivo isolado sem includes.

Antes de publicar:

- Teste as URLs afetadas em desktop e mobile.
- Confira links e redirecionamentos.
- Se mudar chaves de idioma, valide `public/assets/lang/pt.json`, `en.json` e `es.json`.
- Execute `git diff --check` e confira `git status`.

## GitHub e deploy

### Fluxo recomendado

1. Trabalhe em uma branch de feature/fix e valide localmente.
2. Integre em `homolog`. O workflow **Deploy Homolog** publica o ambiente de validação.
3. Valide a URL de homologação, incluindo navegação, responsividade, console, HTTPS, páginas legais, sitemap e CTAs.
4. Promova o commit validado para `main`. O workflow **Deploy Produção** publica o site público.
5. Valide a produção assim que a execução terminar.

Nunca use alterações manuais no checkout do site como publicação: o deploy executa `git reset --hard` e as remove.

### Deploy Homolog

Arquivo: [deploy-homolog.yml](../.github/workflows/deploy-homolog.yml)

O push em `homolog` usa o runner `[self-hosted, homolog]` e executa:

```bash
cd /opt/tutela
git fetch origin
git reset --hard origin/homolog

cd /opt/tutela-v2
docker compose up -d --build
```

### Deploy Produção

Arquivo: [deploy-prod.yml](../.github/workflows/deploy-prod.yml)

O push em `main` usa o runner `[self-hosted, production]` e executa:

```bash
cd /var/www/tutela
git fetch origin
git reset --hard origin/main

cd /opt/tutela-v2
docker compose up -d --build
```

O Compose é reconstruído a cada publicação. Como ele não pertence a este repositório, mudanças nele devem ser feitas pela operação de infraestrutura e mantidas equivalentes entre os servidores quando isso for necessário.

### Sitemap e sincronização

Arquivo: [sitemap.yml](../.github/workflows/sitemap.yml)

O workflow roda em pushes de `main`, `homolog` e `feature/legal-structure`, ou manualmente. Ele gera `public/sitemap.xml` a partir dos HTML rastreados pelo Git, ignora `public/partials/` e cria o commit `chore: auto update sitemap` se houver alteração.

Após um push em `main`, esse workflow também faz merge de `origin/main` em `homolog`. Portanto a sincronização automática é **main → homolog**, e não o inverso. Essa regra deve ser revisada pela equipe, pois o fluxo usual de validação é homologação antes de produção.

### Verificar publicação

Acompanhe a execução em **Actions** no GitHub. No servidor correto, valide:

```bash
cd /opt/tutela-v2
docker compose ps
docker compose logs --tail=100

git -C /opt/tutela rev-parse --short HEAD       # homologação
git -C /var/www/tutela rev-parse --short HEAD   # produção
```

Os comandos de `git -C` devem retornar o SHA esperado para o ambiente em que forem executados.

## Nginx

A configuração Nginx não é mais versionada no repositório: ela é gerenciada diretamente nos servidores. Assim, o resultado de `nginx -T` é a fonte de verdade. Existiu uma configuração histórica no Git, mas ela não deve ser reaplicada automaticamente.

Nginx deve, no mínimo:

- atender HTTP/HTTPS e permitir `/.well-known/acme-challenge/` se usar Let's Encrypt;
- redirecionar HTTP para HTTPS;
- manter `www.tuteladigital.com.br` como canônico na produção;
- fazer proxy para `http://127.0.0.1:8080` (confirmar a porta ativa);
- encaminhar `Host`, `X-Real-IP` e `X-Forwarded-For`;
- manter logs de acesso/erro, certificados válidos e renovação TLS;
- aplicar a política atual de URLs canônicas e redirecionamentos.

**Achado estrutural importante (2026-07-24): homologação e produção têm arquiteturas de Nginx diferentes, não apenas hosts diferentes.** Em produção, o Nginx que termina TLS, aplica os security headers e faz a normalização de URL roda **no host** (`/etc/nginx`, fora do Docker) e repassa para o container `tutela_v2_nginx` só o conteúdo, via `proxy_pass http://localhost:8080`. Em homologação, não existe Nginx de host fazendo esse papel — o container `tutela_v2_nginx` (imagem `nginx:alpine`) está publicado **diretamente** nas portas 80/443 do host (`docker run -p 80:80 -p 443:443` ou equivalente no compose) e ele mesmo faz TLS, headers e normalização de URL. O `/etc/nginx` do host de homologação existe mas **não está vinculado a nenhuma porta pública** — é config morta, não uma segunda fonte de verdade. Consequência prática: para alterar headers/redirects/SSI em produção, edita-se o Nginx do host; para o mesmo em homologação, edita-se a config dentro do container (`/opt/tutela-v2`, montada ou construída na imagem).

| Item | Homologação (host `tutela-dev`) | Produção (host `tutela-web`) |
| --- | --- | --- |
| Hostname | `homolog.tuteladigital.com.br` (CNAME para `dev.tuteladigital.com.br`) | `www.tuteladigital.com.br` |
| Servidor/IP | `tutela-dev`; resolve internamente para IP privado (RFC1918) — registrar em cofre, não neste documento | `tutela-web`, host compartilhado com outros projetos (fora do escopo deste repositório); IP ainda não registrado |
| Onde o Nginx público realmente roda | **Dentro do container** `tutela_v2_nginx` (`nginx:alpine`), publicado direto nas portas 80/443 do host — confirmado via `docker ps` + `ss -ltnp` (portas 80/443 pertencem a `docker-proxy`, não ao processo `nginx` do host) | **No host**, processo `nginx` nativo (fora do Docker) — confirmado via `ss -ltnp` (portas 80/443 pertencem a processos `nginx`, não a `docker-proxy`) |
| Arquivo Nginx ativo | `/etc/nginx/conf.d/default.conf` **dentro do container** `tutela_v2_nginx`, obtido via `docker exec tutela_v2_nginx nginx -T` | `/etc/nginx/sites-enabled/tutela.conf` no host, obtido via `sudo nginx -T` |
| `/etc/nginx` do host (fora do Docker) | Existe (`sites-available/tutela.conf`), mas **não está em uso** — não vinculado a nenhuma porta pública; parece cópia desatualizada do vhost de produção (mesmo `server_name www.tuteladigital.com.br`, mesmo cert) | É o Nginx real e ativo |
| Versão Nginx | `nginx/1.29.7` (header `Server` — a imagem `nginx:alpine` não desativa `server_tokens`) | não divulgada no header (`server_tokens off;` no `nginx.conf` do host) |
| Certificado e renovação | Let's Encrypt, `/etc/letsencrypt/live/homolog.tuteladigital.com.br/` (confirmado via `nginx -T` do container) | Let's Encrypt, `/etc/letsencrypt/live/www.tuteladigital.com.br/` (confirmado via `nginx -T`); renovação automática (certbot timer/cron) **não confirmada** em nenhum dos dois ambientes |
| Containers `tutela_v2_*` ativos | Só `tutela_v2_nginx` (confirmado via `docker ps`) | `tutela_v2_nginx` **e** `tutela_v2_api` (porta 3000, interna) — confirmado via `docker ps` |
| Compose (`/opt/tutela-v2/docker-compose.yml`) | **Paridade com produção confirmada como AUSENTE** — produção roda um container (`tutela_v2_api`) que não aparece rodando em homologação | Ver coluna ao lado — mesma conclusão |
| Checkout Git | `/opt/tutela` | `/var/www/tutela` |
| Upstream | Nginx do container serve os arquivos direto (`root /usr/share/nginx/html;`), sem proxy adicional | `proxy_pass http://localhost:8080;` no host → `tutela_v2_nginx` no container, confirmado via `nginx -T` + `docker ps` |
| SSI (Server Side Includes) | `ssi on; ssi_types text/html;` confirmado dentro do container | `ssi on;` confirmado no vhost do host — resolve a pendência que `11-build-deploy.md` registrava como não-documentada |
| Redirect `.html` → URL limpa | `location ~ ^/(?!partials/)(.*)\.html$ { return 301 https://$host/$1; }` — mesma regra genérica de produção (sem barra final), mesmo bug: as 5 URLs legadas também quebram aqui | `location ~ ^/(?!partials/)(.*)\.html$ { return 301 .../$1/; }` (com barra final) |

**Achado incidental, fora do escopo desta auditoria**: `docker ps` em produção mostra um container `tutela_v2_api` (porta 3000, interna, sem publicação externa direta) que não estava catalogado em nenhum documento de arquitetura. Pode ser a implementação de `/api/diagnostico` (item #2 de `12-technical-debt.md` / ARQ-101) — **não investigado agora**, por disciplina de escopo desta sprint (ARQ-108 é sobre Nginx, não sobre o backend do formulário). Fica como pista concreta para quando ARQ-101 for priorizado.

### Auditoria externa (ARQ-108) — 2026-07-24

Auditoria em duas fases. Fase 1 (abaixo): `curl` a partir do ambiente de execução do Claude Code, que tinha acesso de rede de saída (confirmado antes de prosseguir) mas **nenhum acesso SSH ou a arquivo de configuração** — evidência puramente externa, reproduzível por qualquer pessoa com os mesmos comandos. Fase 2 ("Confirmação via `nginx -T` na fonte", mais abaixo): o usuário rodou os comandos de auditoria diretamente nos servidores e compartilhou o resultado, confirmando (e em um caso, corrigindo) o que a Fase 1 já indicava.

**Headers HTTP confirmados — duplamente, via `curl` externo e via `nginx -T` na fonte (host de produção e container de homologação); nível de confiança: confirmado diretamente nos dois métodos, valores idênticos:**

| Header | Homologação (`https://homolog.tuteladigital.com.br/`) | Produção (`https://www.tuteladigital.com.br/`) |
| --- | --- | --- |
| `Strict-Transport-Security` | **ausente** | `max-age=31536000; includeSubDomains; preload` |
| `X-Frame-Options` | `SAMEORIGIN` | `SAMEORIGIN` |
| `X-Content-Type-Options` | `nosniff` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` | `strict-origin-when-cross-origin` |
| `Content-Security-Policy` | ausente | ausente |
| `Permissions-Policy` | ausente | ausente |
| `X-Robots-Tag` | `noindex, nofollow, noarchive` | ausente (esperado — só faz sentido em homologação) |

```bash
curl -sS -D - -o /dev/null https://homolog.tuteladigital.com.br/
curl -sS -D - -o /dev/null https://www.tuteladigital.com.br/
```

**`og-image.jpg`**: confirmado `404` tanto em produção (`https://www.tuteladigital.com.br/assets/images/og-image.jpg`) quanto em homologação. Resolve em definitivo a incerteza do item #1/`12-technical-debt.md`: o arquivo **não existe em nenhum ambiente**, não é um caso de "existe só em produção fora do Git".

**Redirects legados (`_redirects`/`vercel.json`) — confirmado que NÃO são a fonte ativa, e que os 5 estão quebrados em produção:**

Uma regra genérica do Nginx (remove `.html`, redireciona para o path sem extensão + barra final) intercepta as 5 URLs legadas antes de qualquer regra específica de `_redirects`/`vercel.json`, e o destino gerado não existe:

```bash
curl -sS -D - -o /dev/null https://www.tuteladigital.com.br/institucional.html
# → 301 para /institucional/
curl -sS -o /dev/null -w '%{http_code}\n' https://www.tuteladigital.com.br/institucional/
# → 404
```

O mesmo padrão (`301` para path sem extensão, depois `404`) foi confirmado para `fundamento-juridico.html`, `termos-de-custodia.html`, `preservacao-probatoria-digital.html` e `politica-de-privacidade.html`. Controle: o mesmo comportamento de "strip `.html`" ocorre em `/diagnostico.html` (página sem nenhuma regra de redirect legado), confirmando que é uma regra genérica do Nginx, não a lógica de `_redirects`/`vercel.json`. As páginas de destino reais existem e respondem `200` em `/legal/institucional/` etc. — só não são alcançadas pelas 5 URLs legadas.

**Conclusão factual para ARQ-403**: o Nginx não replica os redirects de `_redirects`/`vercel.json` em nenhum dos dois ambientes — e, hoje, as 5 URLs legadas resultam em `404` tanto em produção quanto em homologação. Correção está fora do escopo desta auditoria (ARQ-108 é só levantamento), mas o fato é confirmado e acionável a qualquer momento.

### Confirmação via `nginx -T` na fonte — produção e homologação, 2026-07-24

**Produção**: `sudo nginx -T` rodado pelo usuário no host `tutela-web` (que hospeda o vhost de `tuteladigital.com.br` junto com outros domínios não relacionados a este projeto, fora do escopo destes docs). Confirma, na fonte, tudo que a auditoria externa por `curl` já havia indicado:

- **Causa raiz do redirect quebrado (ARQ-403), confirmada no arquivo de configuração** (`/etc/nginx/sites-enabled/tutela.conf`):
  ```nginx
  # .html → URL limpa com trailing slash
  location ~ ^/(?!partials/)(.*)\.html$ {
      return 301 https://www.tuteladigital.com.br/$1/;
  }
  ```
  Não existe nenhum `location` específico para as 5 URLs legadas — essa regra genérica de normalização captura qualquer `.html` primeiro. `_redirects` e `vercel.json` nunca são lidos por este Nginx — confirmação de que esses dois arquivos são **inertes há muito tempo** nesta infraestrutura.
- CSP e `Permissions-Policy` **confirmados ausentes na configuração-fonte**.
- `ssi on;`, `proxy_pass http://localhost:8080;` e certificado Let's Encrypt (`/etc/letsencrypt/live/www.tuteladigital.com.br/`) confirmados.
- `server_tokens off;` está no bloco `http {}` global do host (`/etc/nginx/nginx.conf`) — por isso produção não divulga a versão do Nginx no header `Server`.

**Homologação**: inicialmente rodamos `sudo nginx -T` no host `tutela-dev` e o resultado **não batia** com o que o `curl` mostrava (vhost para `www.tuteladigital.com.br`, não `homolog.tuteladigital.com.br`; HSTS presente na config mas ausente ao vivo). Investigação (`docker ps` + `ss -ltnp`) revelou a causa: nesse host, as portas 80/443 são publicadas **diretamente pelo container** `tutela_v2_nginx` (`docker-proxy`, não o processo `nginx` do host) — o `/etc/nginx` do host existe mas está morto, sem porta pública associada, provavelmente uma cópia desatualizada da config de produção nunca ativada. A config real veio de `docker exec tutela_v2_nginx nginx -T`, e essa sim bate exatamente com o `curl`: `server_name homolog.tuteladigital.com.br`, sem HSTS, `X-Robots-Tag: noindex, nofollow, noarchive`, e a mesma regra genérica de redirect quebrado (`location ~ ^/(?!partials/)(.*)\.html$ { return 301 https://$host/$1; }`) — o bug do ARQ-403 existe nos dois ambientes, não só em produção.

**Achado confirmado — a anomalia da porta 80/`:445` não vem de nenhum dos dois Nginx**: o vhost de porta 80 de produção (`server { listen 80; server_name tuteladigital.com.br www.tuteladigital.com.br; ... return 301 https://www.tuteladigital.com.br$request_uri; }`) é um redirect limpo, sem os headers extras (`Content-Security-Policy: frame-ancestors 'self'`, `X-XSS-Protection`) e sem porta `:445` observados via `curl` externo. O usuário esclareceu que o acesso externo passa por um **firewall Fortinet**, e explicou a causa provável (**informado pelo usuário — não verificado diretamente nesta auditoria**): como o Fortinet atende vários sites na porta 443, a porta de administração web do próprio equipamento foi remapeada de 443 (padrão de fábrica) para 445, para não conflitar com o tráfego HTTPS real dos sites. A hipótese mais provável é que a regra de redirect HTTP→HTTPS configurada no Fortinet para `tuteladigital.com.br` está referenciando essa porta de administração (445) em vez da porta real do site (443) — um erro de configuração conhecido em FortiGate, onde o redirecionamento automático herda a variável de porta administrativa (`admin-sport`) em vez da porta do VIP/serviço. Correção está fora do escopo desta auditoria e deste repositório (requer acesso ao Fortinet), mas a causa provável já está documentada para quem for corrigir. Homologação **não tem esse problema** — seu redirect de porta 80 (dentro do próprio container) é limpo, sem anomalia.

```bash
curl -sS -D - -o /dev/null http://tuteladigital.com.br/
docker exec tutela_v2_nginx nginx -T   # rodado no host de homologação
```

**Pendências residuais** (nenhuma bloqueia mais os 3 pontos originais do ARQ-108 — headers, hostname, redirects —, todos confirmados; o que resta é para itens relacionados/futuros):

```bash
# Renovação de certificado, em cada servidor:
sudo certbot certificates 2>/dev/null || true    # ou equivalente

# No Fortinet (fora deste repositório) — corrigir a regra de redirect HTTP→HTTPS de
# tuteladigital.com.br para apontar à porta 443 do site, não à porta de administração
# (445) do próprio equipamento.

# Registrar em cofre operacional (não neste documento): IP dos hosts tutela-web e
# tutela-dev, e o IP privado para o qual homolog.tuteladigital.com.br resolve.
```

Isso fecha: renovação de certificado e a correção da regra de redirect no Fortinet (causa provável já identificada, ver acima — não verificada/corrigida nesta auditoria).

### Auditoria externa (ARQ-505) — 2026-07-26

Ponto de partida: o achado incidental do ARQ-108/Sprint 5 (`docker ps` mostrando `tutela_v2_api` rodando só em produção — ver tabela comparativa acima) sugeria ausência de paridade, mas não era, por si só, a auditoria formal pedida por `12-technical-debt.md`. Esta sprint fecha o que é auditável **sem acesso a servidor** e prepara o que exige.

**Confirmado por `curl` externo — comportamental, reproduzível por qualquer pessoa com os mesmos comandos, sem SSH:**

Em vez de repetir só a observação de processo do ARQ-108, esta auditoria testou se o próprio serviço (não o processo) responde de forma diferente nos dois ambientes:

```bash
curl -sS -D - -o /dev/null https://www.tuteladigital.com.br/api/diagnostico/
curl -sS -D - -o /dev/null https://homolog.tuteladigital.com.br/api/diagnostico/
```

- **Produção**: `404`, mas com um conjunto de headers que **não aparece em nenhuma página estática do site** — `content-security-policy: default-src 'none'`, `cross-origin-opener-policy`, `cross-origin-resource-policy`, `origin-agent-cluster`, `x-dns-prefetch-control`, `x-download-options`, `x-permitted-cross-domain-policies`, `x-xss-protection: 0`, e `x-ratelimit-limit`/`x-ratelimit-remaining`/`x-ratelimit-reset`. Esse padrão (CSP restritivo + headers de segurança tipo Helmet + rate limiting) é característico de uma aplicação Node/Express respondendo diretamente — não de um Nginx servindo arquivo estático inexistente.
- **Homologação**: `404` também, mas com o mesmo conjunto plano de headers de qualquer 404 estático do ambiente (sem CSP, sem rate-limit) — comportamento indistinguível de um path totalmente inexistente.

**Controles para descartar falso positivo** (confirmam que a diferença é específica de `/api/diagnostico`, não um efeito genérico do Nginx):

```bash
# Path garantidamente inexistente, para calibrar o comportamento "padrão" de cada ambiente:
curl -sS -D - -o /dev/null https://www.tuteladigital.com.br/totally-nonexistent-path-xyz123
curl -sS -D - -o /dev/null https://homolog.tuteladigital.com.br/totally-nonexistent-path-xyz123
```

- Produção redireciona (`301`) **qualquer** path sem extensão para a versão com barra final — inclusive paths inexistentes (`/totally-nonexistent-path-xyz123` → `301` → `/totally-nonexistent-path-xyz123/` → `404` sem headers de app) — confirmando que o `301` isolado de `/api/diagnostico` não é sinal de nada por si só; o sinal real está nos headers do `404` final em `/api/diagnostico/`, que só aparecem nesse path específico.
- Testado também `/api/health`, `/api/status`, `/api/ping` nos dois ambientes: todos retornam o padrão genérico (produção `301`→`404` plano; homologação `404` plano) — ou seja, a aplicação por trás de produção só responde de forma diferenciada exatamente em `/api/diagnostico`, não em qualquer path sob `/api/`.
- Porta `3000` (onde `tutela_v2_api` escuta, por `docker ps` do ARQ-108) não é alcançável externamente em nenhum dos dois ambientes (timeout de conexão) — confirma que o container, se existir, não está publicado direto, só acessível via proxy interno do Nginx.

**Conclusão do Bloco A (sem acesso a servidor)**: há evidência comportamental externa, nova e independente do `docker ps` da Sprint 5, de que produção tem um backend de aplicação vivo e proxiado atrás de `/api/diagnostico`, enquanto homologação não tem nada respondendo nesse path (trata-o como qualquer 404 estático). Isso reforça a suspeita de ausência de paridade, mas **não é o diff de `docker-compose.yml`** pedido pelo critério de aceite de `ARQ-505` — não confirma sozinho todas as divergências (variáveis de ambiente, volumes, redes, versões de imagem), só a presença/ausência de um serviço proxiado.

**O que não é auditável a partir deste ambiente**: o conteúdo completo de `docker-compose.yml` (serviços declarados, variáveis de ambiente, volumes, redes, versões de imagem) em nenhum dos dois servidores — esse arquivo não é versionado neste repositório e não há acesso SSH neste ambiente de execução.

**Bloco B — comandos para rodar nos servidores** (mesmo padrão do ARQ-108: usuário roda e cola o resultado de volta):

```bash
# Em cada servidor (tutela-dev = homologação, tutela-web = produção), dentro de /opt/tutela-v2:
cat docker-compose.yml
docker compose config    # config resolvida, com variáveis de ambiente expandidas
docker compose ps
docker ps --format '{{.Names}}\t{{.Image}}\t{{.Ports}}'
```

Com esse output dos dois servidores, é possível fechar `ARQ-505` com o diff formal serviço a serviço. Até lá, o item permanece **BACKLOG, com investigação preparada** — a suspeita de ausência de paridade tem agora duas evidências independentes (processo, via ARQ-108, e comportamento do serviço, via esta auditoria), mas nenhuma delas substitui o diff real do arquivo.

### Diff formal — `docker-compose.yml` produção vs. homologação (2026-07-27)

O usuário rodou os 4 comandos do Bloco B nos dois servidores. **A hipótese de "paridade ausente" da Sprint 5 (baseada em `docker ps` observando o container `api` parado num dado momento) não se confirma como divergência de arquivo**: os dois `docker-compose.yml` declaram exatamente os mesmos dois serviços (`nginx`, `api`), com a mesma imagem/build.

| Item | Homologação (`tutela-dev`) | Produção (`tutela-web`) | Divergência? |
| --- | --- | --- | --- |
| Serviço `api` declarado | `build: ./api`, `container_name: tutela_v2_api`, volume `./api/logs:/app/logs` | Idêntico | Não |
| Serviço `nginx` — imagem | `nginx:alpine` | `nginx:alpine` | Não |
| Porta publicada do `nginx` | `80:80`, `443:443` (direto) | `8080:80` | Sim — **esperada**: já documentada no ARQ-108 (produção usa Nginx do host fazendo proxy para `localhost:8080`; homologação publica o container direto nas portas públicas) |
| Volume do site estático | `/opt/tutela/public` | `/var/www/tutela/public` | Sim — **esperada**: reflete o checkout de cada ambiente (`11-build-deploy.md`), não uma falha de config |
| `/etc/letsencrypt` montado | Sim | Sim | Não |
| `/var/www/html` montado | Sim (extra, sem uso confirmado) | Não presente | Sim — **não investigada** (baixo risco, não bloqueia paridade funcional; candidato a limpeza futura, não corrigido nesta auditoria) |
| Política de restart dos serviços | Nenhuma declarada (`restart:` ausente em ambos) | Nenhuma declarada | Não (idêntico — ver achado operacional abaixo) |
| `depends_on` | `api` (nginx depende de api) | `api` (idêntico) | Não |

**Nenhuma divergência estrutural não justificada** — as duas diferenças de porta/volume já eram esperadas e documentadas pelo ARQ-108 (topologias de proxy diferentes por design). O montante de `/var/www/html` extra em homologação é a única divergência sem explicação registrada; fica anotado, não corrigido (fora do escopo de auditoria).

**Achado operacional durante a coleta do Bloco B (não é sobre paridade, é um incidente real encontrado no processo)**: no momento da coleta, `docker compose ps` em produção mostrava `tutela_v2_nginx` em `Restarting (1)` e `tutela_v2_api` ausente — produção estava retornando `502` em todas as rotas, confirmado via `curl` externo. Causa raiz, pelos logs (`docker compose logs nginx`): `nginx: [emerg] host not found in upstream "api"` — após um reboot do servidor (atualização do Linux, informado pelo usuário), o container `api` não subiu automaticamente porque **nenhum dos dois serviços declara política de `restart`** no compose; sem o `api` no ar, o DNS interno do Docker não resolve o hostname `api`, e o `nginx` entra em loop de falha na inicialização (não tenta re-resolver sozinho). Corrigido ao vivo com `docker compose up -d --build`, que recriou os dois containers; produção confirmada saudável em seguida (`200` em home, `/legal/institucional/`, `/diagnostico/`, `sitemap.xml`; `/api/diagnostico/` respondendo com headers de app novamente). Isso não é uma divergência de paridade (a ausência de `restart:` é idêntica nos dois ambientes) — é uma lacuna de resiliência operacional comum aos dois, fora do escopo de `ARQ-505`; registrado como `ARQ-506` (Épico 5, Alta prioridade por impacto confirmado — ver `16-architecture-backlog.md`) para a Sprint 24, não corrigido no arquivo nesta auditoria.

**Veredito final de `ARQ-505`**: paridade de `docker-compose.yml` **CONFIRMADA** entre produção e homologação — mesmos serviços, mesma imagem/build; as únicas diferenças (porta, path de volume) são de topologia esperada, já documentadas no ARQ-108, não falhas de configuração. Critério de aceite (diff documentado; divergências justificadas) satisfeito.

### Auditoria e mudança segura

No servidor do ambiente:

```bash
sudo nginx -t
sudo nginx -T
sudo systemctl status nginx --no-pager
sudo ss -ltnp | rg ':80|:443|:8080'
sudo docker compose -f /opt/tutela-v2/docker-compose.yml ps
```

Antes de editar Nginx, faça backup datado em local restrito. Depois da edição, sempre execute:

```bash
sudo nginx -t && sudo systemctl reload nginx
```

Não recarregue se o teste falhar. Prefira `reload` a `restart`, pois uma configuração válida pode ser recarregada sem interrupção desnecessária.

### Verificação externa

```bash
curl -I http://SEU_HOST/
curl -I https://SEU_HOST/
curl -sS -o /dev/null -w '%{http_code}\n' https://SEU_HOST/
```

Em produção:

```bash
curl -I http://tuteladigital.com.br/
curl -I https://tuteladigital.com.br/
curl -I https://www.tuteladigital.com.br/
curl -I https://www.tuteladigital.com.br/robots.txt
curl -I https://www.tuteladigital.com.br/sitemap.xml
```

Espere redirecionamentos para HTTPS/`www` quando aplicável e `200` para o site, robots e sitemap. `public/_redirects` e `public/vercel.json` foram removidos do repositório na Sprint 6 (ARQ-403) — comprovadamente inertes, confirmado via `nginx -T` na fonte (ver seção "Nginx" acima). Os redirecionamentos legados reais dependem apenas da regra genérica do Nginx, hoje quebrada para as 5 URLs legadas (ver achados de ARQ-108 acima).

## Incidentes e rollback

Para falha após deploy:

1. Guarde URL, horário, SHA e logs de Actions/Nginx/Compose.
2. Verifique `docker compose ps`, `docker compose logs --tail=100` e `sudo nginx -t`.
3. Faça rollback com um novo commit que reverta o commit ruim na branch do ambiente. É o caminho auditável e persistente.
4. Valide antes de promover a correção.

Não deixe o checkout do servidor preso em SHA antigo: o workflow o substituirá por `origin/main` ou `origin/homolog`. Em incidente de Nginx, restaure o backup anterior do arquivo, valide com `nginx -t` e recarregue; não use configuração histórica do Git como restauração automática.

### Incidente: certificado TLS expirado em produção (2026-07-27)

Durante a validação de `ARQ-506` (Sprint 24), um health check de rotina (`curl https://www.tuteladigital.com.br/`) encontrou `SSL certificate problem: certificate has expired`. Confirmado via `sudo certbot certificates`: o certificado de `www.tuteladigital.com.br` havia expirado às 2026-07-27 01:54:03 UTC, poucos minutos antes da checagem — outage real e ativo para qualquer visitante retornante (produção tem HSTS ativo, confirmado em ARQ-108; navegador força HTTPS e bloqueia sem opção de prosseguir). `http://` (porta 80) continuava respondendo `301` normalmente, já que o redirect não depende do certificado.

**Causa raiz**: regra de firewall bloqueando a renovação automática — corrigida pelo usuário durante o incidente (detalhe da regra fora do escopo deste documento, registrar em cofre/infra se relevante).

**Achado que agrava o incidente**: `certbot.timer` está ativo e rodando duas vezes ao dia há meses (desde 2026-04-30), e um certificado diferente no mesmo host compartilhado (`www.veritio.com.br`, projeto fora deste repositório) renovou normalmente (2 dias de validade no momento da checagem) — ou seja, a automação em si não estava quebrada de forma geral, a falha era específica ao bloqueio de firewall para este domínio, e **falhou silenciosamente por tempo suficiente para o certificado chegar a expirar de fato**, sem nenhum alerta chegar a alguém. Um certificado de `netcenter.br.com` (mesmo host, outro projeto) expirou no mesmo instante (01:53:47 UTC) — mesma causa raiz provável, sinalizar para quem for responsável por esse projeto.

**Correção aplicada**: `sudo certbot renew --cert-name www.tuteladigital.com.br` — sucesso, `nginx` recarregado automaticamente pelo hook de renovação do certbot. Novo certificado válido até 2026-08-26. `curl https://www.tuteladigital.com.br/` confirmado `200` após a correção.

**Lacuna sistêmica exposta, não corrigida nesta sessão**: não existe alerta/monitoramento de expiração de certificado — a falha de renovação só foi percebida porque um health check manual, feito por outro motivo, aconteceu de bater na janela entre a expiração real e a próxima tentativa agendada. Candidato a item novo de backlog (Épico 5, ex. "monitoramento de expiração de certificado TLS/alerta de falha de renovação silenciosa"), não criado nesta sessão por disciplina de escopo — fica registrado aqui como achado para decisão em sprint futura.

## Segurança e pendências de operação

- Controle escrita nas branches `main` e `homolog`; use revisão para produção.
- Restrinja administração dos runners, Docker, Nginx, DNS e certificados.
- Mantenha segredos em GitHub Secrets ou cofre operacional, nunca em commits.
- Confirme e registre em cofre: IPs, responsáveis, arquivo Nginx ativo, upstream, renovação TLS, paridade do Compose, backup e retenção de logs. (URL/DNS de homologação já confirmada em 2026-07-24, ver [Auditoria externa (ARQ-108)](#auditoria-externa-arq-108-2026-07-24).)
- Defina se o merge automático **main → homolog** do sitemap é intencional para o processo de release.

Depois de preencher esses dados operacionais, este documento é o runbook de onboarding, publicação e resposta inicial a incidentes.

