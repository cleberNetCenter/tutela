const checkoutService = require('../modules/payments/checkoutService');

async function createCheckout(req, res) {
  try {
    const result = await checkoutService.create(req.body);
    res.status(201).json(result);
  } catch (error) {
    res.status(400).json({
      message: 'Falha ao criar checkout',
      details: error.message,
    });
  }
}

module.exports = { createCheckout };
