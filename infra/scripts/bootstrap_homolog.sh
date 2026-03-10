#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="$ROOT_DIR/docker-compose.yml"
ENV_FILE="$ROOT_DIR/.env"

if [[ ! -f "$COMPOSE_FILE" ]]; then
  echo "docker-compose.yml nao encontrado em $ROOT_DIR" >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo ".env nao encontrado em $ROOT_DIR" >&2
  echo "Crie o arquivo com base em .env.example antes de executar este script." >&2
  exit 1
fi

compose() {
  docker compose -f "$COMPOSE_FILE" "$@"
}

wait_for_postgres() {
  local retries=30

  echo "Aguardando PostgreSQL ficar pronto..."
  until compose exec -T postgres pg_isready -U tutela -d tutela >/dev/null 2>&1; do
    retries=$((retries - 1))
    if [[ $retries -le 0 ]]; then
      echo "PostgreSQL nao ficou pronto dentro do tempo esperado." >&2
      exit 1
    fi
    sleep 2
  done
}

seed_default_plan() {
  echo "Garantindo plano inicial de homologacao..."
  compose exec -T postgres psql -U tutela -d tutela <<'SQL'
INSERT INTO plans (name, amount_cents, interval)
SELECT 'Plano Homologacao Mensal', 4990, 'Monthly'
WHERE NOT EXISTS (
  SELECT 1
  FROM plans
  WHERE name = 'Plano Homologacao Mensal'
);
SQL
}

create_admin_user() {
  local admin_email="${HOMOLOG_ADMIN_EMAIL:-}"
  local admin_name="${HOMOLOG_ADMIN_NAME:-Admin Homologacao}"
  local admin_password_hash="${HOMOLOG_ADMIN_PASSWORD_HASH:-}"

  if [[ -z "$admin_email" || -z "$admin_password_hash" ]]; then
    echo "HOMOLOG_ADMIN_EMAIL ou HOMOLOG_ADMIN_PASSWORD_HASH nao configurados. Pulando seed de usuario admin."
    return
  fi

  echo "Garantindo usuario admin de homologacao..."
  compose exec -T postgres psql -U tutela -d tutela <<SQL
INSERT INTO users (name, email, password_hash, role)
SELECT '${admin_name}', '${admin_email}', '${admin_password_hash}', 'admin'
WHERE NOT EXISTS (
  SELECT 1
  FROM users
  WHERE email = '${admin_email}'
);
SQL
}

echo "Subindo stack de homologacao..."
compose up --build -d postgres redis backend nginx

wait_for_postgres

echo "Executando migrations..."
compose exec -T backend npm run migrate

seed_default_plan
create_admin_user

echo "Estado final dos containers:"
compose ps

echo "Bootstrap de homologacao concluido."
