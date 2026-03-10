function register(event, payload = {}) {
  return {
    event,
    timestamp: new Date().toISOString(),
    payload,
  };
}

module.exports = { register };
