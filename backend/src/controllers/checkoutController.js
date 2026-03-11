const checkoutService = require('../modules/payments/checkoutService');

async function createCheckout(req, res) {
  try {
    const result = await checkoutService.create(req.body);
    res.status(201).json(result);
  } catch (error) {
    const details = error.details || error.message;
    console.error('Falha ao criar checkout:', details);
    res.status(400).json({
      message: 'Falha ao criar checkout',
      details,
    });
  }
}

module.exports = { createCheckout };
