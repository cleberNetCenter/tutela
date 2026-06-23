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

O hostname de produção confirmado no conteúdo e sitemap é `www.tuteladigital.com.br`. A URL de homologação não está versionada: obtenha-a da configuração Nginx/DNS e registre-a no cofre operacional.

## Desenvolvimento local

Pré-requisitos: Git, Python 3 e navegador. Não use `file://`; execute o site por HTTP:

```bash
python3 -m http.server 8080 --directory public
```

Acesse `http://localhost:8080/`. Não há build, gerenciador de pacotes nem testes automatizados versionados; HTML, CSS, JavaScript, partials, idiomas e assets são entregues diretamente.

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

| Item | Homologação | Produção |
| --- | --- | --- |
| Hostname | confirmar | `www.tuteladigital.com.br` |
| Servidor/IP | confirmar | confirmar |
| Arquivo Nginx ativo | confirmar | confirmar |
| Certificado e renovação | confirmar | confirmar |
| Compose | `/opt/tutela-v2/docker-compose.yml` | `/opt/tutela-v2/docker-compose.yml` |
| Checkout Git | `/opt/tutela` | `/var/www/tutela` |
| Upstream | confirmar | `127.0.0.1:8080` a confirmar |

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

Espere redirecionamentos para HTTPS/`www` quando aplicável e `200` para o site, robots e sitemap. Os redirecionamentos legados também aparecem em `public/_redirects` e `public/vercel.json`; confirme que a camada realmente usada em produção os atende.

## Incidentes e rollback

Para falha após deploy:

1. Guarde URL, horário, SHA e logs de Actions/Nginx/Compose.
2. Verifique `docker compose ps`, `docker compose logs --tail=100` e `sudo nginx -t`.
3. Faça rollback com um novo commit que reverta o commit ruim na branch do ambiente. É o caminho auditável e persistente.
4. Valide antes de promover a correção.

Não deixe o checkout do servidor preso em SHA antigo: o workflow o substituirá por `origin/main` ou `origin/homolog`. Em incidente de Nginx, restaure o backup anterior do arquivo, valide com `nginx -t` e recarregue; não use configuração histórica do Git como restauração automática.

## Segurança e pendências de operação

- Controle escrita nas branches `main` e `homolog`; use revisão para produção.
- Restrinja administração dos runners, Docker, Nginx, DNS e certificados.
- Mantenha segredos em GitHub Secrets ou cofre operacional, nunca em commits.
- Confirme e registre em cofre: URL/DNS de homologação, IPs, responsáveis, arquivo Nginx ativo, upstream, renovação TLS, paridade do Compose, backup e retenção de logs.
- Defina se o merge automático **main → homolog** do sitemap é intencional para o processo de release.

Depois de preencher esses dados operacionais, este documento é o runbook de onboarding, publicação e resposta inicial a incidentes.

