const bcrypt = require('bcrypt');

async function main() {
  const password = process.argv[2];
  const rounds = Number(process.argv[3] || 10);

  if (!password) {
    console.error('Uso: npm run hash-password -- "SUA_SENHA" [saltRounds]');
    process.exit(1);
  }

  if (!Number.isInteger(rounds) || rounds < 4 || rounds > 15) {
    console.error('saltRounds invalido. Use um inteiro entre 4 e 15.');
    process.exit(1);
  }

  const hash = await bcrypt.hash(password, rounds);
  console.log(hash);
}

main().catch((error) => {
  console.error('Erro ao gerar hash bcrypt:', error.message);
  process.exit(1);
});
