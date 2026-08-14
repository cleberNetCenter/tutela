# ADR-0004 — Adoção de TLS Pós-Quântico (PQC) na Infraestrutura Nginx

| Campo | Valor |
|---|---|
| Status | Proposto (parcialmente implementado — ver Decisão) |
| Data | 2026-08-14 |
| Sprint / ARQ | 14/08/2026, `ARQ-704` |
| Relacionado | `ARQ-704` (a abrir formalmente), `ARQ-108` (auditoria de infraestrutura que originou este trabalho) |
| Decisores | Cleber (infraestrutura), com investigação técnica assistida por Claude |

## Contexto

O modelo de ameaça "harvest now, decrypt later" (HNDL) — onde tráfego TLS interceptado hoje pode ser descriptografado no futuro por um computador quântico suficientemente capaz — afeta primariamente o key exchange de uma sessão TLS, não a assinatura de certificados. Key exchange clássico (X25519, ECDHE) usa problemas matemáticos (log discreto em curvas elípticas) que algoritmos quânticos (Shor) resolvem eficientemente; assinatura de certificados tem urgência menor porque a janela de exposição é o tempo de validade do certificado (meses), não o tempo de retenção de tráfego interceptado (potencialmente anos/décadas).

Isso motivou investigar viabilidade de PQC na camada de key exchange TLS da infraestrutura do Tutela Digital, através do item `ARQ-704` (proposto, não formalmente aberto no backlog até este ADR).

### Estado da infraestrutura (confirmado por auditoria direta, 14/08/2026)

| Ambiente | Quem termina TLS | Nginx | OpenSSL |
|---|---|---|---|
| Produção (`tutela-web`) | Nginx do host (`systemd`) | 1.24.0 | 3.0.13 |
| Homologação (`tutela-dev`) | Nginx dentro do container Docker (`nginx:alpine`) | 1.29.7 | 3.5.5 (atualizado para 3.5.7 via `apk upgrade` durante o teste) |

OpenSSL 3.0.13 (produção) não implementa ML-KEM (FIPS 203) nativamente — suporte experimental chegou na série 3.2, tornou-se estável na 3.5 (abril de 2025). OpenSSL 3.5.5/3.5.7 (homolog, via imagem `nginx:alpine` já em uso) tem suporte nativo completo.

## Decisão

### Homologação — implementado nesta sprint

Adicionada a diretiva `ssl_ecdh_curve X25519MLKEM768:X25519:secp256r1;` ao `server{}` de `homolog.tuteladigital.com.br` em `/opt/tutela-v2/nginx/default.conf`, aplicada via `docker compose up -d --force-recreate nginx` (necessário por causa do bind mount de arquivo único — ver nota operacional em `docs/ambientes-e-deploy.md`).

Validado ao vivo contra o hostname público real:

```
$ openssl s_client -connect homolog.tuteladigital.com.br:443 -groups X25519MLKEM768 -tls1_3
Negotiated TLS1.3 group: X25519MLKEM768
Verify return code: 0 (ok)
```

A lista de grupos coloca o híbrido PQC primeiro, com fallback para X25519 e secp256r1 clássicos — mudança aditiva, sem quebra de compatibilidade: clientes que não suportam o grupo híbrido continuam negociando normalmente com os grupos clássicos.

### Produção — não implementado, decisão em aberto

A mesma diretiva não pode ser aplicada da mesma forma em produção, porque o Nginx que termina TLS ali é o do host (OpenSSL 3.0.13, sem suporte nativo), não o container Docker. Três caminhos foram identificados, nenhum aplicado:

| Caminho | Descrição | Prós | Contras |
|---|---|---|---|
| A — Upgrade do OpenSSL do host | Atualizar OpenSSL do sistema operacional para 3.5+ (via backport/PPA/compilação) e recompilar/religar o Nginx do host contra ele | Resolve na raiz; mesma infra que hoje | Maior superfície de mudança no SO de produção; pode afetar outros serviços que dependem do OpenSSL do sistema (ex. netcenter, veritio, que também rodam nesse host) |
| B — `oqs-provider` | Instalar o provider Open Quantum Safe como plugin do OpenSSL 3.0.13 atual, sem trocar a versão base | Não exige upgrade do OpenSSL do SO; mais cirúrgico | Componente adicional a manter/atualizar; ecosystem menos maduro que suporte nativo |
| C — Migrar topologia de produção para o padrão de homolog | Docker passa a terminar TLS diretamente (como já acontece em homolog), Nginx do host deixa de ter esse papel | Reaproveita exatamente o que já foi validado em homolog; unifica as duas topologias (resolvendo também a divergência de normalização de URL registrada em `ARQ-408`) | Mudança arquitetural de maior porte; precisa replicar toda a lógica hoje só no Nginx do host (SSI, headers, cache, redirects) para dentro do container; risco mais alto |

Nenhum destes caminhos foi avaliado além do nível de descrição acima — cada um exigiria sua própria investigação técnica antes de uma escolha informada.

## Consequências

- Homologação está pronta para validar continuamente comportamento de clientes/monitoramento com PQC ativo, funcionando como ambiente de prova antes de qualquer decisão de produção.
- Produção segue com key exchange 100% clássico — exposta ao modelo de ameaça HNDL até uma decisão ser tomada e executada.
- A escolha entre os Caminhos A/B/C depende de fatores fora do escopo desta investigação técnica (apetite de risco, prazo desejado, se outros sites no mesmo host de produção precisam do mesmo tratamento) — decisão de negócio/infraestrutura, não só técnica.
- `openssl` instalado no container de homolog para o teste desta sprint é efêmero (não sobrevive a um `--force-recreate`) — se for necessário monitorar a negociação PQC de forma recorrente, será preciso um Dockerfile próprio em vez da imagem `nginx:alpine` pura (fora do escopo desta decisão).

## Não decidido nesta sprint

Qual dos três caminhos seguir para produção, e quando. Fica registrado como trabalho futuro sob `ARQ-704`.
