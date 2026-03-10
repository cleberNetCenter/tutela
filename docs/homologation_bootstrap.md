# Bootstrap da Homologacao

## Objetivo
Subir o ambiente publico de homologacao com os mesmos componentes basicos do desenvolvimento atual:

- `nginx`
- `backend`
- `postgres`
- `redis`

## Arquivos Envolvidos
- [docker-compose.yml](/home/cleber/tutela/docker-compose.yml)
- [bootstrap_homolog.sh](/home/cleber/tutela/infra/scripts/bootstrap_homolog.sh)
- [001_init.sql](/home/cleber/tutela/database/migrations/001_init.sql)
- [002_users_role_and_indexes.sql](/home/cleber/tutela/database/migrations/002_users_role_and_indexes.sql)

## Componentes que Devem Ser Replicados na Homologacao
- VM Ubuntu separada da producao
- Docker e Docker Compose
- Codigo da branch `homolog`
- Arquivo `.env` proprio da homologacao
- Banco PostgreSQL
- Redis
- Nginx
- DNS publico com HTTPS

## Procedimento
1. Clonar a branch `homolog`.
2. Criar `.env` a partir de `.env.example`.
3. Executar:

```bash
cd /opt/tutela
bash infra/scripts/bootstrap_homolog.sh
```

## O que o Script Faz
1. Valida a existencia de `docker-compose.yml` e `.env`.
2. Sobe `postgres`, `redis`, `backend` e `nginx`.
3. Aguarda o PostgreSQL ficar pronto.
4. Executa as migrations do backend.
5. Garante um plano inicial de homologacao na tabela `plans`.
6. Opcionalmente cria um usuario admin se as variaveis abaixo existirem no shell:

```bash
export HOMOLOG_ADMIN_EMAIL=admin@seudominio
export HOMOLOG_ADMIN_PASSWORD_HASH='$2b$10$...hash bcrypt...'
export HOMOLOG_ADMIN_NAME='Administrador Homologacao'
```

## Banco Criado na Homologacao
As migrations atuais criam:

- `users`
- `plans`
- `subscriptions`
- `payments`
- `transactions`
- `audit_logs`
- `schema_migrations`

## Validacoes Pos-Bootstrap
```bash
docker compose ps
curl http://localhost:8080/api/health
docker compose exec -T postgres psql -U tutela -d tutela -c "select id, name, amount_cents, interval from plans;"
```

## Observacoes
- O script e idempotente para migrations e seed do plano inicial.
- O usuario admin opcional exige hash bcrypt pronto; o script nao gera senha em claro.
- As URLs da Cielo configuradas no `.env` devem apontar para o dominio publico da homologacao.
