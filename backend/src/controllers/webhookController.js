const webhookService = require('../modules/payments/webhookService');

async function handleCieloWebhook(req, res) {
  try {
    const result = await webhookService.process(req.body);
    res.status(200).json(result);
  } catch (error) {
    res.status(400).json({
      message: 'Falha ao processar webhook Cielo',
      details: error.message,
    });
  }
}

module.exports = { handleCieloWebhook };
