function calculate({ amount, recipients = [] }) {
  const totalPercent = recipients.reduce((acc, current) => acc + current.percent, 0);

  if (totalPercent > 100) {
    throw new Error('Percentual de split invalido: acima de 100%.');
  }

  return recipients.map((recipient) => ({
    ...recipient,
    amount: Math.round((amount * recipient.percent) / 100),
  }));
}

module.exports = { calculate };
