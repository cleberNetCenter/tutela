# Arquitetura de Pagamentos

## Objetivo
Introduzir pagamentos online, recorrencia e split com baixo acoplamento, rastreabilidade e capacidade de auditoria.

## Componentes
- **Checkout API**: cria pedidos e inicia pagamento.
- **Gateway Adapter (Cielo)**: encapsula chamadas REST da Cielo.
- **Subscription Service**: cria e acompanha recorrencias.
- **Webhook Handler**: processa notificacoes assincronas.
- **Payment Split Service**: calcula e registra distribuicao por parceiro/comissao.
- **Banco PostgreSQL**: persistencia transacional.
- **Redis**: idempotencia, cache curto e desacoplamento operacional.

## Fluxo de Checkout
1. Cliente chama `POST /api/checkout`.
2. Backend valida dados e cria registro local pendente.
3. Modulo Cielo cria transacao.
4. Backend grava `PaymentId`, status e auditoria.
5. Cliente recebe resposta de pagamento.

## Fluxo de Recorrencia
1. Cliente chama `POST /api/subscriptions`.
2. Backend monta payload com `RecurrentPayment`.
3. Cielo agenda cobrancas futuras.
4. Webhook atualiza status de assinatura e pagamentos.

## Webhooks e Confiabilidade
- Endpoint: `POST /api/webhook/cielo`.
- Validar autenticidade da notificacao (cabecalhos/chave compartilhada).
- Aplicar idempotencia por `PaymentId` + evento.
- Registrar eventos em `transactions` e `audit_logs`.

## Boas Praticas
- Timeout e retry com backoff nas chamadas ao gateway.
- Segredos em variaveis de ambiente.
- Nao armazenar dados sensiveis de cartao.
- Logs estruturados com correlacao por request-id.
