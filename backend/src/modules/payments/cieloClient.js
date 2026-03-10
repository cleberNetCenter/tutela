const axios = require('axios');

const sandboxBaseUrl = 'https://apisandbox.cieloecommerce.cielo.com.br';
const productionBaseUrl = 'https://api.cieloecommerce.cielo.com.br';

function getBaseUrl() {
  return process.env.CIELO_SANDBOX === 'true' ? sandboxBaseUrl : productionBaseUrl;
}

function getHeaders() {
  return {
    MerchantId: process.env.CIELO_MERCHANT_ID,
    MerchantKey: process.env.CIELO_MERCHANT_KEY,
    'Content-Type': 'application/json',
  };
}

async function createSale(payload) {
  const response = await axios.post(`${getBaseUrl()}/1/sales/`, payload, {
    headers: getHeaders(),
    timeout: 10000,
  });

  return response.data;
}

async function captureSale(paymentId, amount) {
  const suffix = typeof amount === 'number' ? `?amount=${amount}` : '';
  const response = await axios.put(`${getBaseUrl()}/1/sales/${paymentId}/capture${suffix}`, {}, {
    headers: getHeaders(),
    timeout: 10000,
  });

  return response.data;
}

module.exports = {
  createSale,
  captureSale,
};
