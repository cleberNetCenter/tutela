const auditService = require('../../services/auditService');
const subscriptionRepository = require('../../repositories/subscriptionRepository');
const transactionRepository = require('../../repositories/transactionRepository');

async function process(payload) {
  const paymentId = payload.PaymentId || null;
  const changeType = payload.ChangeType || null;
  const recurrentPaymentId = payload.RecurrentPaymentId || null;

  if (recurrentPaymentId && changeType) {
    await subscriptionRepository.updateSubscriptionStatus(recurrentPaymentId, changeType);
  }

  const transaction = await transactionRepository.registerTransaction({
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
    changeType,
    transaction,
    audit,
  };
}

module.exports = { process };
