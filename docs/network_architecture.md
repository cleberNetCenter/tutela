# Topologia de Rede - Atual e Futura

## Topologia Atual
```text
Internet
   |
Firewall Fortinet
   |
VMWare Host
   |
Ubuntu Server
   |
Nginx
   |
Site estatico
```

## Topologia Futura
```text
Internet
   |
Fortinet
   |
Reverse Proxy Nginx
   |
+-----------------------------+
| Backend API (Node.js)       |
| PostgreSQL                  |
| Redis                       |
| Worker                      |
+-----------------------------+
```

## Regras de Exposicao
### Portas externas (publicas)
- `80/tcp`
- `443/tcp`

### Portas internas (privadas)
- `3000/tcp` - Backend API
- `5432/tcp` - PostgreSQL
- `6379/tcp` - Redis

## Diretrizes
- Somente Nginx deve receber trafego externo.
- API, banco e cache devem permanecer em rede privada.
- Fortinet deve restringir origem/rota para portas internas.
- TLS termina no reverse proxy com renovacao de certificados controlada.
