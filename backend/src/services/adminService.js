const userRepository = require('../repositories/userRepository');
const subscriptionRepository = require('../repositories/subscriptionRepository');

async function getDashboard() {
  const [users, subscriptions] = await Promise.all([
    userRepository.listUsers(),
    subscriptionRepository.listSubscriptions(),
  ]);

  return {
    usersCount: users.length,
    subscriptionsCount: subscriptions.length,
  };
}

async function listUsers() {
  return userRepository.listUsers();
}

async function listSubscriptions() {
  return subscriptionRepository.listSubscriptions();
}

module.exports = {
  getDashboard,
  listUsers,
  listSubscriptions,
};
