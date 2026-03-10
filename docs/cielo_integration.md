# Integracao Checkout Cielo

## Credenciais
Variaveis esperadas:

- `CIELO_CHECKOUT_CLIENT_ID`
- `CIELO_CHECKOUT_CLIENT_SECRET`
- `CIELO_CHECKOUT_ACCESS_TOKEN` (opcional, somente override manual)
- `CIELO_CHECKOUT_RETURN_URL`
- `CIELO_CHECKOUT_NOTIFICATION_URL`
- `CIELO_CHECKOUT_STATUS_UPDATE_URL`

As credenciais `CIELO_MERCHANT_ID` e `CIELO_MERCHANT_KEY` permanecem reservadas para a futura migracao ao modelo de API E-commerce com checkout proprio.

## Endpoints Principais
### Gerar token de acesso
- `POST https://cieloecommerce.cielo.com.br/api/public/v2/token`

### Criar pagina de pagamento
- `POST https://cieloecommerce.cielo.com.br/api/public/v1/orders/`

## Estrategia de Implementacao Atual
1. O backend gera um token OAuth2 do Checkout Cielo usando `ClientId` e `ClientSecret`.
2. O endpoint interno `POST /api/checkout` cria uma pagina hospedada da Cielo e devolve `checkoutUrl`.
3. O endpoint `POST /api/subscriptions` cria uma pagina hospedada recorrente e devolve `checkoutUrl`.
4. O comprador e redirecionado para a pagina segura da Cielo para preencher os dados do pagamento.
5. O backend recebe notificacoes e atualizacoes de status em `POST /api/webhook/cielo`.

## Observacoes Importantes
- Checkout Cielo e Link de Pagamento nao possuem sandbox separado para criacao da pagina; a API usa o ambiente de producao com o Modo de Teste habilitado na loja Cielo.
- A pagina do Checkout exige dados de pedido, carrinho, frete e comprador.
- As URLs de retorno, notificacao e mudanca de status devem ser configuradas antes do go-live.
- A resposta da API de Checkout inclui a URL hospedada da Cielo. No codigo atual, esse valor e exposto como `checkoutUrl`.

## Contrato Recomendado do Backend
- `POST /api/checkout`: aceita `amount`, dados do comprador e opcionalmente `checkoutPayload` com o payload oficial completo da Cielo.
- `POST /api/subscriptions`: aceita `amount`, `userId`, `planId` e opcionalmente `checkoutPayload` com os campos oficiais de recorrencia programada.
- Quando `checkoutPayload` for enviado, o backend o repassa diretamente para a API oficial, reduzindo acoplamento a um modelo interno provisiorio.

## Checklist de Go-Live
- Gerar `ClientId` e `ClientSecret` no portal da Cielo.
- Habilitar Modo de Teste no Checkout Cielo antes da homologacao.
- Configurar URL de retorno e notificacoes com HTTPS publico.
- Validar redirecionamento, notificacao, mudanca de status e conciliacao de pedidos.
