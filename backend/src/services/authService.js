const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const HttpError = require('../utils/httpError');
const userRepository = require('../repositories/userRepository');

function generateToken(user) {
  return jwt.sign(
    {
      sub: user.id,
      email: user.email,
      role: user.role,
    },
    process.env.JWT_SECRET || 'dev-secret',
    { expiresIn: '8h' }
  );
}

async function register({ name, email, password, role }) {
  if (!name || !email || !password) {
    throw new HttpError(400, 'Nome, email e senha sao obrigatorios.');
  }

  const existingUser = await userRepository.findByEmail(email);
  if (existingUser) {
    throw new HttpError(409, 'Email ja cadastrado.');
  }

  const passwordHash = await bcrypt.hash(password, 10);
  const createdUser = await userRepository.createUser({
    name,
    email,
    passwordHash,
    role: role || 'customer',
  });

  return {
    user: createdUser,
    token: generateToken(createdUser),
  };
}

async function login({ email, password }) {
  if (!email || !password) {
    throw new HttpError(400, 'Email e senha sao obrigatorios.');
  }

  const user = await userRepository.findByEmail(email);
  if (!user) {
    throw new HttpError(401, 'Credenciais invalidas.');
  }

  const isValidPassword = await bcrypt.compare(password, user.password_hash);
  if (!isValidPassword) {
    throw new HttpError(401, 'Credenciais invalidas.');
  }

  return {
    user: {
      id: user.id,
      name: user.name,
      email: user.email,
      role: user.role,
      created_at: user.created_at,
    },
    token: generateToken(user),
  };
}

module.exports = {
  register,
  login,
};
