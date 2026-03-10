const db = require('../services/db');

async function registerTransaction({ paymentId = null, provider, providerEvent, providerReference, rawPayload }) {
  const { rows } = await db.query(
    `INSERT INTO transactions (payment_id, provider, provider_event, provider_reference, raw_payload)
     VALUES ($1, $2, $3, $4, $5)
     RETURNING id, payment_id, provider, provider_event, provider_reference, created_at`,
    [paymentId, provider, providerEvent, providerReference, rawPayload]
  );

  return rows[0];
}

module.exports = {
  registerTransaction,
};
