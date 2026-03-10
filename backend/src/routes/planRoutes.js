const { Router } = require('express');
const planController = require('../controllers/plans/planController');
const { requireAuth, requireAdmin } = require('../middlewares/authMiddleware');

const router = Router();

router.get('/plans', planController.listPlans);
router.post('/plans', requireAuth, requireAdmin, planController.createPlan);
router.put('/plans/:id', requireAuth, requireAdmin, planController.updatePlan);
router.delete('/plans/:id', requireAuth, requireAdmin, planController.deletePlan);

module.exports = router;
