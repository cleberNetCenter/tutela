const db = require('../services/db');

async function createPlan({ name, amountCents, interval }) {
  const { rows } = await db.query(
    `INSERT INTO plans (name, amount_cents, interval)
     VALUES ($1, $2, $3)
     RETURNING id, name, amount_cents, interval, created_at`,
    [name, amountCents, interval]
  );

  return rows[0];
}

async function listPlans() {
  const { rows } = await db.query(
    `SELECT id, name, amount_cents, interval, created_at
     FROM plans
     ORDER BY id DESC`
  );

  return rows;
}

async function updatePlan(id, { name, amountCents, interval }) {
  const { rows } = await db.query(
    `UPDATE plans
     SET name = $2,
         amount_cents = $3,
         interval = $4
     WHERE id = $1
     RETURNING id, name, amount_cents, interval, created_at`,
    [id, name, amountCents, interval]
  );

  return rows[0] || null;
}

async function deletePlan(id) {
  const { rowCount } = await db.query('DELETE FROM plans WHERE id = $1', [id]);
  return rowCount > 0;
}

module.exports = {
  createPlan,
  listPlans,
  updatePlan,
  deletePlan,
};
