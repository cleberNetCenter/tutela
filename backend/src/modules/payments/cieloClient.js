const axios = require('axios');
const { URLSearchParams } = require('url');

const sandboxBaseUrl = 'https://apisandbox.cieloecommerce.cielo.com.br';
const productionBaseUrl = 'https://api.cieloecommerce.cielo.com.br';
const checkoutBaseUrl = 'https://cieloecommerce.cielo.com.br';

let cachedCheckoutToken = null;
let cachedCheckoutTokenExpiresAt = 0;

function getBaseUrl() {
  return process.env.CIELO_SANDBOX === 'true' ? sandboxBaseUrl : productionBaseUrl;
}

function getCheckoutBaseUrl() {
  return process.env.CIELO_CHECKOUT_BASE_URL || checkoutBaseUrl;
}

function getHeaders() {
  return {
    MerchantId: process.env.CIELO_MERCHANT_ID,
    MerchantKey: process.env.CIELO_MERCHANT_KEY,
    'Content-Type': 'application/json',
  };
}

function getCheckoutCredentials() {
  const clientId = process.env.CIELO_CHECKOUT_CLIENT_ID;
  const clientSecret = process.env.CIELO_CHECKOUT_CLIENT_SECRET;

  if (!clientId || !clientSecret) {
    throw new Error(
      'Missing Checkout Cielo credentials. Configure CIELO_CHECKOUT_CLIENT_ID and CIELO_CHECKOUT_CLIENT_SECRET.'
    );
  }

  return { clientId, clientSecret };
}

function buildCheckoutAuthHeader() {
  const { clientId, clientSecret } = getCheckoutCredentials();
  const encoded = Buffer.from(`${clientId}:${clientSecret}`).toString('base64');

  return `Basic ${encoded}`;
}

async function getCheckoutAccessToken() {
  if (process.env.CIELO_CHECKOUT_ACCESS_TOKEN) {
    return process.env.CIELO_CHECKOUT_ACCESS_TOKEN;
  }

  const now = Date.now();
  if (cachedCheckoutToken && now < cachedCheckoutTokenExpiresAt) {
    return cachedCheckoutToken;
  }

  const body = new URLSearchParams({ grant_type: 'client_credentials' }).toString();
  const response = await axios.post(`${getCheckoutBaseUrl()}/api/public/v2/token`, body, {
    headers: {
      Authorization: buildCheckoutAuthHeader(),
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    timeout: 10000,
  });

  const accessToken = response.data && response.data.access_token
    ? response.data.access_token
    : response.data;

  if (!accessToken) {
    throw new Error('Checkout Cielo token response did not include an access token');
  }

  const expiresInSeconds = Number(response.data && response.data.expires_in) || 600;
  cachedCheckoutToken = accessToken;
  cachedCheckoutTokenExpiresAt = now + Math.max(expiresInSeconds - 30, 60) * 1000;

  return cachedCheckoutToken;
}

async function createCheckoutPage(payload) {
  const accessToken = await getCheckoutAccessToken();
  const response = await axios.post(`${getCheckoutBaseUrl()}/api/public/v1/orders/`, payload, {
    headers: {
      Authorization: `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    timeout: 10000,
  });

  return response.data;
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
  createCheckoutPage,
  createSale,
  captureSale,
  getCheckoutAccessToken,
};
