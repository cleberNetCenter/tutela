# Infraestrutura Atual - Tutela Digital

## Visao Geral
A plataforma atual da Tutela Digital opera em uma infraestrutura tradicional com servidor unico:

- **Hypervisor:** VMware
- **Sistema operacional da VM:** Ubuntu Server
- **Servidor web:** Nginx
- **Aplicacao:** site estatico (HTML/CSS/JS)
- **Protecao de borda:** Firewall Fortinet

## Fluxo Atual
1. Requisicoes entram pela internet.
2. Firewall Fortinet aplica regras de seguranca e NAT.
3. Trafego permitido chega ao host VMware.
4. VM Ubuntu recebe a conexao.
5. Nginx entrega arquivos estaticos do site.

## Estrutura Provavel de Diretorios no Servidor
- `/var/www/site`: conteudo estatico publicado
- `/etc/nginx/`: configuracao principal do Nginx
- `/etc/nginx/sites-enabled`: virtual hosts ativos

## Caracteristicas e Limitacoes Atuais
- Nao ha backend dedicado para regras de negocio.
- Nao ha camada API para checkout, assinaturas ou integracoes externas.
- Nao ha separacao explicita de servicos (web, API, fila, cache, DB).
- Escalabilidade e evolucao funcional ficam acopladas a mesma VM.

## Risco Operacional
- Alteracoes no ambiente produtivo sem clone/esteira aumentam risco de indisponibilidade.
- Ausencia de observabilidade e isolamento de componentes dificulta diagnostico rapido.
