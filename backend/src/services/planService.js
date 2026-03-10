const HttpError = require('../utils/httpError');
const planRepository = require('../repositories/planRepository');

async function create(input) {
  if (!input.name || !input.amountCents || !input.interval) {
    throw new HttpError(400, 'name, amountCents e interval sao obrigatorios.');
  }

  return planRepository.createPlan(input);
}

async function list() {
  return planRepository.listPlans();
}

async function update(id, input) {
  if (!input.name || !input.amountCents || !input.interval) {
    throw new HttpError(400, 'name, amountCents e interval sao obrigatorios.');
  }

  const updated = await planRepository.updatePlan(id, input);
  if (!updated) {
    throw new HttpError(404, 'Plano nao encontrado.');
  }

  return updated;
}

async function remove(id) {
  const deleted = await planRepository.deletePlan(id);
  if (!deleted) {
    throw new HttpError(404, 'Plano nao encontrado.');
  }

  return { deleted: true };
}

module.exports = {
  create,
  list,
  update,
  remove,
};
