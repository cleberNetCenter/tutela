const { Router } = require('express');
const authRoutes = require('./authRoutes');
const checkoutRoutes = require('./checkoutRoutes');
const subscriptionRoutes = require('./subscriptionRoutes');
const webhookRoutes = require('./webhookRoutes');
const adminRoutes = require('./adminRoutes');
const planRoutes = require('./planRoutes');

const router = Router();

router.use(authRoutes);
router.use(planRoutes);
router.use(checkoutRoutes);
router.use(subscriptionRoutes);
router.use(webhookRoutes);
router.use(adminRoutes);

router.get('/health', (_, res) => {
  res.status(200).json({ status: 'api-ok' });
});

module.exports = router;
