const { Router } = require('express');
const adminController = require('../controllers/admin/adminController');
const { requireAuth, requireAdmin } = require('../middlewares/authMiddleware');

const router = Router();

router.get('/admin/health', requireAuth, requireAdmin, (_, res) => {
  res.status(200).json({ status: 'admin-ok' });
});

router.get('/admin/dashboard', requireAuth, requireAdmin, adminController.dashboard);
router.get('/admin/users', requireAuth, requireAdmin, adminController.listUsers);
router.get('/admin/subscriptions', requireAuth, requireAdmin, adminController.listSubscriptions);

module.exports = router;
