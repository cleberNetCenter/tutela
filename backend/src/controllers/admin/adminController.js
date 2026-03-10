const adminService = require('../../services/adminService');

async function dashboard(_, res) {
  try {
    const result = await adminService.getDashboard();
    return res.status(200).json(result);
  } catch (error) {
    return res.status(400).json({ message: error.message });
  }
}

async function listUsers(_, res) {
  try {
    const result = await adminService.listUsers();
    return res.status(200).json(result);
  } catch (error) {
    return res.status(400).json({ message: error.message });
  }
}

async function listSubscriptions(_, res) {
  try {
    const result = await adminService.listSubscriptions();
    return res.status(200).json(result);
  } catch (error) {
    return res.status(400).json({ message: error.message });
  }
}

module.exports = {
  dashboard,
  listUsers,
  listSubscriptions,
};
