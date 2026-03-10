const fs = require('fs');
const path = require('path');
const db = require('../src/services/db');

async function ensureMigrationsTable() {
  await db.query(`
    CREATE TABLE IF NOT EXISTS schema_migrations (
      id SERIAL PRIMARY KEY,
      filename VARCHAR(255) UNIQUE NOT NULL,
      executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `);
}

async function getExecutedMigrations() {
  const { rows } = await db.query('SELECT filename FROM schema_migrations');
  return new Set(rows.map((row) => row.filename));
}

async function run() {
  const migrationsDir = process.env.MIGRATIONS_DIR
    ? path.resolve(process.env.MIGRATIONS_DIR)
    : path.resolve(__dirname, '../../database/migrations');
  const files = fs
    .readdirSync(migrationsDir)
    .filter((file) => file.endsWith('.sql'))
    .sort();

  await ensureMigrationsTable();
  const executed = await getExecutedMigrations();

  for (const filename of files) {
    if (executed.has(filename)) {
      continue;
    }

    const sql = fs.readFileSync(path.join(migrationsDir, filename), 'utf8');

    await db.query('BEGIN');
    try {
      await db.query(sql);
      await db.query('INSERT INTO schema_migrations (filename) VALUES ($1)', [filename]);
      await db.query('COMMIT');
      console.log(`Migration executada: ${filename}`);
    } catch (error) {
      await db.query('ROLLBACK');
      throw error;
    }
  }

  console.log('Migracoes finalizadas.');
}

run()
  .catch((error) => {
    console.error('Erro ao executar migracoes:', error.message);
    process.exitCode = 1;
  })
  .finally(async () => {
    await db.end();
  });
