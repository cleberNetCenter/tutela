const { Router } = require('express');
const { createSubscription } = require('../controllers/subscriptionController');

const router = Router();

router.post('/subscriptions', createSubscription);

module.exports = router;
