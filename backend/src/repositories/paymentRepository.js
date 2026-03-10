const db = require('../services/db');

async function savePaymentDraft(input) {
  const { rows } = await db.query(
    `INSERT INTO payments (user_id, subscription_id, gateway_payment_id, amount_cents, status, payment_method)
     VALUES ($1, $2, $3, $4, $5, $6)
     RETURNING id, user_id, subscription_id, gateway_payment_id, amount_cents, status, payment_method, created_at`,
    [
      input.userId || null,
      input.subscriptionId || null,
      null,
      input.amount,
      'DRAFT',
      input.paymentMethod || 'CreditCard',
    ]
  );

  return rows[0];
}

async function updatePaymentGatewayData(paymentId, gatewayPaymentId, status) {
  const { rows } = await db.query(
    `UPDATE payments
     SET gateway_payment_id = $1,
         status = $2
     WHERE id = $3
     RETURNING id, user_id, subscription_id, gateway_payment_id, amount_cents, status, payment_method, created_at`,
    [gatewayPaymentId, status, paymentId]
  );

  return rows[0] || null;
}

async function updatePaymentStatusByGatewayId(gatewayPaymentId, status) {
  const { rows } = await db.query(
    `UPDATE payments
     SET status = $2
     WHERE gateway_payment_id = $1
     RETURNING id, user_id, subscription_id, gateway_payment_id, amount_cents, status, payment_method, created_at`,
    [gatewayPaymentId, status]
  );

  return rows[0] || null;
}

module.exports = {
  savePaymentDraft,
  updatePaymentGatewayData,
  updatePaymentStatusByGatewayId,
};
