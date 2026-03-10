const db = require('../services/db');

async function createUser({ name, email, passwordHash, role = 'customer' }) {
  const { rows } = await db.query(
    `INSERT INTO users (name, email, password_hash, role)
     VALUES ($1, $2, $3, $4)
     RETURNING id, name, email, role, created_at`,
    [name, email, passwordHash, role]
  );

  return rows[0];
}

async function findByEmail(email) {
  const { rows } = await db.query(
    `SELECT id, name, email, role, password_hash, created_at
     FROM users
     WHERE email = $1
     LIMIT 1`,
    [email]
  );

  return rows[0] || null;
}

async function listUsers() {
  const { rows } = await db.query(
    `SELECT id, name, email, role, created_at
     FROM users
     ORDER BY id DESC`
  );

  return rows;
}

module.exports = {
  createUser,
  findByEmail,
  listUsers,
};
