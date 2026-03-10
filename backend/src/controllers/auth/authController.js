const authService = require('../../services/authService');

function handleError(error, res) {
  const statusCode = error.statusCode || 400;
  return res.status(statusCode).json({ message: error.message });
}

async function register(req, res) {
  try {
    const result = await authService.register(req.body);
    return res.status(201).json(result);
  } catch (error) {
    return handleError(error, res);
  }
}

async function login(req, res) {
  try {
    const result = await authService.login(req.body);
    return res.status(200).json(result);
  } catch (error) {
    return handleError(error, res);
  }
}

module.exports = {
  register,
  login,
};
