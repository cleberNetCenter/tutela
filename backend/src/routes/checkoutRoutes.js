const { Router } = require('express');
const { createCheckout } = require('../controllers/checkoutController');

const router = Router();

router.post('/checkout', createCheckout);

module.exports = router;
