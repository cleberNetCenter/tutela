const cieloClient = require('./cieloClient');
const paymentRepository = require('../../repositories/paymentRepository');

function removeUndefined(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([, value]) => value !== undefined));
}

function compactNested(value) {
  if (Array.isArray(value)) {
    return value
      .map(compactNested)
      .filter((item) => item !== undefined);
  }

  if (!value || typeof value !== 'object') {
    return value;
  }

  const compacted = Object.fromEntries(
    Object.entries(value)
      .map(([key, nestedValue]) => [key, compactNested(nestedValue)])
      .filter(([, nestedValue]) => nestedValue !== undefined)
  );

  return Object.keys(compacted).length > 0 ? compacted : undefined;
}

function buildDefaultItem(input) {
  return {
    Name: input.itemName || input.planName || 'Servico Tutela Digital',
    Description: input.itemDescription || 'Pagamento Tutela Digital',
    UnitPrice: input.amount,
    Quantity: input.quantity || 1,
    Type: input.itemType || 'Asset',
  };
}

function buildCheckoutPayload(input) {
  if (input.checkoutPayload && typeof input.checkoutPayload === 'object') {
    return input.checkoutPayload;
  }

  return compactNested({
    OrderNumber: input.orderId || `order_${Date.now()}`,
    SoftDescriptor: input.softDescriptor || 'TUTELA',
    ReturnUrl: input.returnUrl || process.env.CIELO_CHECKOUT_RETURN_URL,
    NotificationUrl: input.notificationUrl || process.env.CIELO_CHECKOUT_NOTIFICATION_URL,
    PaymentStatusUrl: input.statusUpdateUrl || process.env.CIELO_CHECKOUT_STATUS_UPDATE_URL,
    Shipping: {
      Type: input.shippingType || 'WithoutShipping',
      Price: input.shippingPrice || 0,
    },
    Customer: removeUndefined({
      FullName: input.customerName || 'Cliente Tutela',
      Email: input.customerEmail,
      Identity: input.customerIdentity,
      IdentityType: input.customerIdentityType,
      Phone: input.customerPhone,
    }),
    Cart: {
      Items: Array.isArray(input.items) && input.items.length > 0 ? input.items : [buildDefaultItem(input)],
    },
  });
}

async function create(input) {
  if (!Number.isInteger(input.amount) || input.amount <= 0) {
    throw new Error('amount must be a positive integer in cents');
  }

  const draftPayment = await paymentRepository.savePaymentDraft(input);
  const checkoutPayload = buildCheckoutPayload(input);
  const cieloResponse = await cieloClient.createCheckoutPage(checkoutPayload);
  const checkoutUrl = cieloResponse.CheckoutUrl || cieloResponse.checkout_url || null;

  return {
    checkoutStatus: 'CHECKOUT_CREATED',
    gateway: 'cielo-checkout',
    payment: {
      ...draftPayment,
      status: 'CHECKOUT_CREATED',
    },
    checkoutUrl,
    checkoutPayload,
    cieloResponse,
  };
}

module.exports = { create };
