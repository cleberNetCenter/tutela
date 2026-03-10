const cieloClient = require('./cieloClient');
const subscriptionRepository = require('../../repositories/subscriptionRepository');

function removeUndefined(obj) {
  return Object.fromEntries(Object.entries(obj).filter(([, value]) => value !== undefined));
}

function buildDefaultItem(input) {
  return {
    type: input.itemType || 'Service',
    name: input.itemName || input.planName || 'Assinatura Tutela Digital',
    unit_price: input.amount,
    quantity: 1,
  };
}

function buildSubscriptionCheckoutPayload(input) {
  if (input.checkoutPayload && typeof input.checkoutPayload === 'object') {
    return input.checkoutPayload;
  }

  return removeUndefined({
    order_number: input.orderId || `sub_${Date.now()}`,
    soft_descriptor: input.softDescriptor || 'TUTELA',
    shipping_type: input.shippingType || 'WithoutShipping',
    shipping_price: input.shippingPrice || 0,
    customer_name: input.customerName || 'Assinante Tutela',
    customer_email: input.customerEmail,
    customer_identity: input.customerIdentity,
    customer_identity_type: input.customerIdentityType,
    return_url: input.returnUrl || process.env.CIELO_CHECKOUT_RETURN_URL,
    notification_url: input.notificationUrl || process.env.CIELO_CHECKOUT_NOTIFICATION_URL,
    payment_status_url: input.statusUpdateUrl || process.env.CIELO_CHECKOUT_STATUS_UPDATE_URL,
    recurrent: true,
    recurrent_interval: input.interval || 'Monthly',
    recurrent_end_date: input.endDate,
    items: Array.isArray(input.items) && input.items.length > 0 ? input.items : [buildDefaultItem(input)],
  });
}

async function create(input) {
  if (!Number.isInteger(input.amount) || input.amount <= 0) {
    throw new Error('amount must be a positive integer in cents');
  }

  const payload = buildSubscriptionCheckoutPayload(input);
  const cieloResponse = await cieloClient.createCheckoutPage(payload);
  const checkoutUrl = cieloResponse.CheckoutUrl || cieloResponse.checkout_url || null;

  const subscription = await subscriptionRepository.createSubscription({
    userId: input.userId,
    planId: input.planId,
    gatewaySubscriptionId: null,
    status: 'PENDING_CHECKOUT',
  });

  return {
    subscriptionStatus: 'CHECKOUT_CREATED',
    gateway: 'cielo-checkout',
    subscription,
    checkoutUrl,
    checkoutPayload: payload,
    cieloResponse,
  };
}

module.exports = { create };
