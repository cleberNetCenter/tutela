const planService = require('../../services/planService');

function handleError(error, res) {
  const statusCode = error.statusCode || 400;
  return res.status(statusCode).json({ message: error.message });
}

async function createPlan(req, res) {
  try {
    const result = await planService.create(req.body);
    return res.status(201).json(result);
  } catch (error) {
    return handleError(error, res);
  }
}

async function listPlans(_, res) {
  try {
    const result = await planService.list();
    return res.status(200).json(result);
  } catch (error) {
    return handleError(error, res);
  }
}

async function updatePlan(req, res) {
  try {
    const result = await planService.update(Number(req.params.id), req.body);
    return res.status(200).json(result);
  } catch (error) {
    return handleError(error, res);
  }
}

async function deletePlan(req, res) {
  try {
    const result = await planService.remove(Number(req.params.id));
    return res.status(200).json(result);
  } catch (error) {
    return handleError(error, res);
  }
}

module.exports = {
  createPlan,
  listPlans,
  updatePlan,
  deletePlan,
};
