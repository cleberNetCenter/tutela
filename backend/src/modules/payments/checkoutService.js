const cieloClient = require('./cieloClient');
const paymentRepository = require('../../repositories/paymentRepository');

async function create(input) {
  await paymentRepository.savePaymentDraft(input);

  const salePayload = {
    MerchantOrderId: input.orderId || `order_${Date.now()}`,
    Customer: {
      Name: input.customerName || 'Cliente Tutela',
    },
    Payment: {
      Type: 'CreditCard',
      Amount: input.amount,
      Installments: input.installments || 1,
      SoftDescriptor: 'Tutela',
      Recurrent: false,
      CreditCard: input.creditCard || {},
    },
  };

  const cieloResponse = await cieloClient.createSale(salePayload);

  return {
    checkoutStatus: 'CREATED',
    gateway: 'cielo',
    cieloResponse,
  };
}

module.exports = { create };
