async function savePaymentDraft(input) {
  return {
    id: `draft_${Date.now()}`,
    status: 'PENDING',
    input,
  };
}

module.exports = { savePaymentDraft };
