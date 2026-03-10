const subscriptionService = require('../modules/payments/subscriptionService');

async function createSubscription(req, res) {
  try {
    const result = await subscriptionService.create(req.body);
    res.status(201).json(result);
  } catch (error) {
    res.status(400).json({
      message: 'Falha ao criar assinatura',
      details: error.message,
    });
  }
}

module.exports = { createSubscription };
