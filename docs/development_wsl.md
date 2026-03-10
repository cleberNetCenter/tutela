# Ambiente de Desenvolvimento (Windows + WSL)

## Atualizacao base
```bash
sudo apt update
sudo apt upgrade -y
```

## Instalacao de ferramentas
```bash
sudo apt install -y git docker.io docker-compose nodejs npm
```

## Permitir uso do Docker sem sudo
```bash
sudo usermod -aG docker $USER
newgrp docker
```

## Execucao local
Na raiz do projeto:

```bash
docker compose up --build
```

Acesso principal:
- `http://localhost:8080`
