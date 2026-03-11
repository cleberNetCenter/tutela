const cieloClient = require('./cieloClient');
const subscriptionRepository = require('../../repositories/subscriptionRepository');

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
    Name: input.itemName || input.planName || 'Assinatura Tutela Digital',
    Description: input.itemDescription || 'Assinatura programada Tutela Digital',
    UnitPrice: input.amount,
    Quantity: 1,
    Type: input.itemType || 'Asset',
  };
}

function buildSubscriptionCheckoutPayload(input) {
  if (input.checkoutPayload && typeof input.checkoutPayload === 'object') {
    return input.checkoutPayload;
  }

  return compactNested({
    OrderNumber: input.orderId || `sub_${Date.now()}`,
    SoftDescriptor: input.softDescriptor || 'TUTELA',
    ReturnUrl: input.returnUrl || process.env.CIELO_CHECKOUT_RETURN_URL,
    NotificationUrl: input.notificationUrl || process.env.CIELO_CHECKOUT_NOTIFICATION_URL,
    PaymentStatusUrl: input.statusUpdateUrl || process.env.CIELO_CHECKOUT_STATUS_UPDATE_URL,
    Shipping: {
      Type: input.shippingType || 'WithoutShipping',
      Price: input.shippingPrice || 0,
    },
    Customer: removeUndefined({
      FullName: input.customerName || 'Assinante Tutela',
      Email: input.customerEmail,
      Identity: input.customerIdentity,
      IdentityType: input.customerIdentityType,
      Phone: input.customerPhone,
    }),
    Cart: {
      Items: Array.isArray(input.items) && input.items.length > 0 ? input.items : [buildDefaultItem(input)],
    },
    Recurrent: removeUndefined({
      Interval: input.interval || 'Monthly',
      EndDate: input.endDate,
    }),
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
