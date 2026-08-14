# ADR-0004 — Adoção de TLS Pós-Quântico (PQC) na Infraestrutura Nginx

| Campo | Valor |
|---|---|
| Status | Implementado (Caminho B, homolog e produção) |
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

## Adendo — Decisão final e execução

Status atualizado: Implementado (Caminho B, homolog e produção)
Data da atualização: 14/08/2026

Após a investigação original identificar três caminhos possíveis para produção (A — upgrade de OpenSSL do host; B — `oqs-provider`; C — migração de topologia), cada um foi avaliado com dados reais antes de uma escolha:

### Caminho A — descartado

Ubuntu 24.04 LTS trava OpenSSL na série 3.0.x nos repositórios oficiais (`apt-cache madison` não retorna nenhuma versão 3.5+). Um upgrade exigiria sair do repositório suportado pela Canonical. Mais grave: `libssl3` do sistema é dependência compartilhada de `sshd` e `apt` no mesmo host — substituí-la arriscaria acesso remoto ao servidor. Descartado por risco desproporcional ao ganho.

### Caminho C — descartado

`ss -tlnp` confirmou que o Nginx do host escuta `0.0.0.0:443` como processo único, multiplexando três domínios (`tuteladigital.com.br`, `netcenter.br.com`, `veritio.com.br`) por SNI. O host tem um único IP público (`192.168.30.220`, atrás de NAT/port-forward do Fortigate — `ip -4 addr show` confirmou ausência de IPs adicionais). Migrar o Tutela para o Docker terminar TLS diretamente causaria conflito de bind de porta com os outros dois sites, que compartilham o mesmo processo Nginx. Resolver isso exigiria nova interface de rede e/ou reconfiguração do Fortigate para rotear por VIP/SNI — complexidade desproporcional, descartado por decisão do responsável pelo projeto.

### Caminho B — escolhido, implementado e validado em homologação e produção

Processo de build (idêntico nos dois ambientes, executado via container Docker temporário `ubuntu:24.04`, sem instalar toolchain de compilação nos hosts):

```bash
git clone --depth 1 https://github.com/open-quantum-safe/liboqs.git
git clone --depth 1 https://github.com/open-quantum-safe/oqs-provider.git
cmake -S liboqs -B liboqs/build -DCMAKE_INSTALL_PREFIX=/tmp/liboqs-install -DOQS_USE_OPENSSL=OFF -DBUILD_SHARED_LIBS=ON -GNinja
cmake --build liboqs/build --parallel && cmake --install liboqs/build
cmake -S oqs-provider -B oqs-provider/build -DCMAKE_INSTALL_PREFIX=/tmp/oqsprov-install -Dliboqs_DIR=/tmp/liboqs-install/lib/cmake/liboqs -GNinja
cmake --build oqs-provider/build --parallel
```

Artefatos gerados: `oqsprovider.so` (~1.1MB) e `liboqs.so.9` (~26MB) + symlinks.

Instalação (fora de gerenciamento por pacote — `.so`s copiados manualmente):

- `liboqs.so*` → `/usr/lib/x86_64-linux-gnu/` (+ `ldconfig`)
- `oqsprovider.so` → `/usr/lib/x86_64-linux-gnu/ossl-modules/`
- `openssl.cnf` editado: novo `oqsprovider = oqsprovider_sect` em `[provider_sect]`, nova seção `[oqsprovider_sect]` com `activate = 1`, e `default_sect` com `activate = 1` explícito (mantendo o provider padrão ativo — requisito de segurança, evita quebrar aplicações/SSH que dependem do OpenSSL do sistema).

Diretiva Nginx aplicada — no nível `http{}` de `/etc/nginx/nginx.conf` (não em cada `server{}` individualmente — ver "Causa raiz descoberta" abaixo):

```nginx
ssl_ecdh_curve X25519MLKEM768:X25519:secp256r1;
```

### Causa raiz descoberta durante a aplicação em produção — lição operacional crítica

A primeira tentativa de aplicar a diretiva (só no `server{}` do Tutela, depois em todos os `server{}` do domínio, depois no nível `http{}` global) falhou consistentemente com `SSL alert number 40` (`handshake_failure`) quando um cliente oferecia o grupo híbrido. Diagnóstico completo, por eliminação:

- Não era posição da diretiva no arquivo — mesmo movida para `http{}` global (herdada por todos os `server{}`, incluindo Netcenter e Veritio), a falha persistiu.
- Não era `ssl_ciphers` incompatível — testado isoladamente, sem efeito na negociação de grupo.
- Não eram processos Nginx concorrentes na porta 443 — confirmado via `ss -tlnp` que só um processo (`nginx.service`) está de fato vinculado a `0.0.0.0:443`; os outros processos "nginx" visíveis em `ps` são workers dentro dos containers Docker, isolados em redes internas.
- Causa real: `openssl list -providers`/CLI `openssl` enxergavam o `oqsprovider` corretamente (novo processo, lê `openssl.cnf` do zero), mas o processo master do Nginx, rodando desde 30/07 (duas semanas antes desta mudança), nunca recarregou sua inicialização do OpenSSL. `systemctl reload nginx` recarrega a configuração do Nginx, mas não reinicializa o OpenSSL nem seus providers — isso só acontece na criação de um novo processo master. Confirmado via `/proc/<pid>/maps`: o provider `liboqs.so` estava ausente do mapa de memória dos workers antes do restart, presente depois.

Correção: `systemctl restart nginx` (não `reload`) após qualquer mudança em `openssl.cnf`. Causou interrupção breve (segundos) — aceitável, comunicado e executado deliberadamente, não incidental.

### Validação final (14/08/2026, pós-restart)

```
Netcenter:  Negotiated TLS1.3 group: X25519MLKEM768
Veritio:    Negotiated TLS1.3 group: X25519MLKEM768
Tutela:     Negotiated TLS1.3 group: X25519MLKEM768 (via hostname público, através do Fortigate)
Smoke test (sem forçar grupo): HTTP/2 200 nos três sites
```

Netcenter e Veritio ganharam suporte a PQC como benefício colateral não planejado — a diretiva no nível `http{}` global os beneficia automaticamente, sem trabalho adicional, já que compartilham o mesmo processo Nginx do host.

### Consequências (atualizado)

- Todos os três sites servidos por este host (Tutela, Netcenter, Veritio) têm key exchange híbrido PQC ativo, mitigando "harvest now, decrypt later" para os três de uma vez.
- `liboqs`/`oqs-provider` não são gerenciados por pacote do sistema (`apt`) — instalação manual, não sobrevive a uma reinstalação do SO, e uma atualização futura de `libssl3` via `apt upgrade` pode alterar ABI o suficiente para quebrar compatibilidade binária com o provider compilado hoje. Sem processo de atualização automatizado — risco de dívida técnica silenciosa.
- Qualquer mudança futura em `openssl.cnf` do host exige `systemctl restart nginx`, não `reload` — documentado no runbook para evitar repetição do diagnóstico desta sprint.
- Ambiente de homologação (`tutela-dev`) tem dois caminhos PQC funcionando simultaneamente: o original via imagem `nginx:alpine`/Docker (não removido) e agora também via `oqs-provider` no host (mesmo padrão de produção) — redundância não intencional, sem necessidade de unificar, mas vale nota para não confundir futuros diagnósticos.

### Não decidido — fica como trabalho futuro, fora desta sprint

Empacotamento apropriado de `liboqs`/`oqs-provider` (ex. `.deb` próprio ou script de instalação versionado) para tornar a instalação reproduzível e resiliente a atualizações do sistema. Monitoramento contínuo da taxa de negociação PQC real vs. fallback clássico em produção (não implementado nesta sprint).
