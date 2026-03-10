# Arquitetura de Pagamentos

## Objetivo
Introduzir pagamentos online, recorrencia e split com baixo acoplamento, rastreabilidade e capacidade de auditoria.

## Componentes
- **Checkout API**: cria a pagina hospedada da Cielo e devolve a URL de redirecionamento.
- **Gateway Adapter (Checkout Cielo)**: encapsula token OAuth2, criacao de pagina e chamadas de gestao.
- **Subscription Service**: cria paginas recorrentes e acompanha a ativacao apos webhook/status update.
- **Webhook Handler**: processa notificacoes assincronas.
- **Payment Split Service**: calcula e registra distribuicao por parceiro/comissao.
- **Banco PostgreSQL**: persistencia transacional.
- **Redis**: idempotencia, cache curto e desacoplamento operacional.

## Fluxo de Checkout
1. Cliente chama `POST /api/checkout`.
2. Backend valida dados e cria registro local pendente.
3. Modulo Cielo gera token OAuth2 e cria a pagina de pagamento hospedada.
4. Backend devolve `checkoutUrl` ao frontend.
5. Cliente e redirecionado para a pagina segura da Cielo.
6. Webhooks/consultas atualizam status local do pedido.

## Fluxo de Recorrencia
1. Cliente chama `POST /api/subscriptions`.
2. Backend monta o payload oficial do Checkout com recorrencia programada.
3. Checkout Cielo coleta o cartao e agenda as cobrancas futuras.
4. A assinatura local permanece `PENDING_CHECKOUT` ate a confirmacao assincrona.
5. Webhook atualiza status de assinatura e pagamentos.

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
- Manter o payload oficial do Checkout Cielo o mais proximo possivel do contrato do fornecedor para simplificar o go-live.
