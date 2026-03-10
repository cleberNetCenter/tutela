const { Router } = require('express');
const { handleCieloWebhook } = require('../controllers/webhookController');

const router = Router();

router.post('/webhook/cielo', handleCieloWebhook);

module.exports = router;
