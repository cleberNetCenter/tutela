const db = require('../services/db');

async function createSubscription({ userId, planId, gatewaySubscriptionId, status }) {
  const { rows } = await db.query(
    `INSERT INTO subscriptions (user_id, plan_id, gateway_subscription_id, status, started_at)
     VALUES ($1, $2, $3, $4, NOW())
     RETURNING id, user_id, plan_id, gateway_subscription_id, status, started_at, created_at`,
    [userId, planId || null, gatewaySubscriptionId || null, status || 'PENDING']
  );

  return rows[0];
}

async function updateSubscriptionStatus(gatewaySubscriptionId, status) {
  const { rows } = await db.query(
    `UPDATE subscriptions
     SET status = $2
     WHERE gateway_subscription_id = $1
     RETURNING id, user_id, plan_id, gateway_subscription_id, status, started_at, created_at`,
    [gatewaySubscriptionId, status]
  );

  return rows[0] || null;
}

async function listSubscriptions() {
  const { rows } = await db.query(
    `SELECT id, user_id, plan_id, gateway_subscription_id, status, started_at, created_at
     FROM subscriptions
     ORDER BY id DESC`
  );

  return rows;
}

module.exports = {
  createSubscription,
  updateSubscriptionStatus,
  listSubscriptions,
};
