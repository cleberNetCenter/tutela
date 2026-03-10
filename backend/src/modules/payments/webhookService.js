const auditService = require('../../services/auditService');
const paymentRepository = require('../../repositories/paymentRepository');
const subscriptionRepository = require('../../repositories/subscriptionRepository');
const transactionRepository = require('../../repositories/transactionRepository');

function mapWebhookStatus(changeType) {
  const normalized = String(changeType || '').toLowerCase();

  if (normalized.includes('authorize')) {
    return 'AUTHORIZED';
  }

  if (normalized.includes('capture') || normalized.includes('paid')) {
    return 'PAID';
  }

  if (normalized.includes('cancel')) {
    return 'CANCELED';
  }

  return 'RECEIVED';
}

async function process(payload) {
  const paymentId = payload.PaymentId || null;
  const changeType = payload.ChangeType || null;
  const recurrentPaymentId = payload.RecurrentPaymentId || null;
  const paymentStatus = mapWebhookStatus(changeType);
  const payment = paymentId
    ? await paymentRepository.updatePaymentStatusByGatewayId(paymentId, paymentStatus)
    : null;

  if (recurrentPaymentId && changeType) {
    await subscriptionRepository.updateSubscriptionStatus(recurrentPaymentId, changeType);
  }

  const transaction = await transactionRepository.registerTransaction({
    paymentId: payment ? payment.id : null,
    provider: 'cielo',
    providerEvent: changeType,
    providerReference: paymentId,
    rawPayload: payload,
  });

  const audit = auditService.register('cielo.webhook.received', {
    paymentId,
    event: changeType,
    recurrentPaymentId,
  });

  return {
    processed: true,
    paymentId,
    paymentStatus,
    payment,
    changeType,
    transaction,
    audit,
  };
}

module.exports = { process };
