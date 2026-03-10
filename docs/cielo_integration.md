# Integracao Cielo E-commerce API

## Credenciais
Variaveis esperadas:

- `CIELO_MERCHANT_ID`
- `CIELO_MERCHANT_KEY`
- `CIELO_SANDBOX=true|false`

## Endpoints Principais
### Criar pagamento
- `POST https://apisandbox.cieloecommerce.cielo.com.br/1/sales/`

### Capturar pagamento
- `PUT /1/sales/{PaymentId}/capture`

### Criar checkout
- `POST https://cieloecommerce.cielo.com.br/api/public/v1/orders/`

### Criar recorrencia
- `POST /1/sales/` com objeto `RecurrentPayment`

## Estrategia de Implementacao
1. Centralizar chamadas HTTP em `cieloClient.js`.
2. Usar headers obrigatorios:
   - `MerchantId`
   - `MerchantKey`
   - `Content-Type: application/json`
3. Tratar erros de rede, timeout e codigos 4xx/5xx.
4. Persistir request/response normalizados para auditoria (sem dados sensiveis).

## Ambientes
- Sandbox: homologacao e testes automatizados.
- Producao: habilitar apenas apos validacao de fluxo completo (checkout, webhook, recorrencia, split).

## Checklist de Go-Live
- Chaves de producao validadas.
- Endpoint webhook publico com TLS.
- Monitoramento de falhas de autorizacao/captura.
- Rotina de reconciliacao financeira diaria.
