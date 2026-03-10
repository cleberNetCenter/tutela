const cieloClient = require('./cieloClient');
const subscriptionRepository = require('../../repositories/subscriptionRepository');

async function create(input) {
  const payload = {
    MerchantOrderId: input.orderId || `sub_${Date.now()}`,
    Customer: {
      Name: input.customerName || 'Assinante Tutela',
    },
    Payment: {
      Type: 'CreditCard',
      Amount: input.amount,
      Installments: 1,
      Recurrent: true,
      RecurrentPayment: {
        AuthorizeNow: true,
        Interval: input.interval || 'Monthly',
      },
      CreditCard: input.creditCard || {},
    },
  };

  const cieloResponse = await cieloClient.createSale(payload);
  const recurrentId = cieloResponse.Payment && cieloResponse.Payment.RecurrentPayment
    ? cieloResponse.Payment.RecurrentPayment.RecurrentPaymentId
    : null;

  const subscription = await subscriptionRepository.createSubscription({
    userId: input.userId,
    planId: input.planId,
    gatewaySubscriptionId: recurrentId,
    status: 'CREATED',
  });

  return {
    subscriptionStatus: 'CREATED',
    gateway: 'cielo',
    subscription,
    cieloResponse,
  };
}

module.exports = { create };
