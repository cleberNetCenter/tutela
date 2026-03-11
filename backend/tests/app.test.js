const request = require('supertest');

jest.mock('../src/services/db', () => ({
  query: jest.fn(),
}));

const db = require('../src/services/db');
const checkoutService = require('../src/modules/payments/checkoutService');
const subscriptionService = require('../src/modules/payments/subscriptionService');
const webhookService = require('../src/modules/payments/webhookService');
const app = require('../src/app');

describe('Tutela API', () => {
  beforeEach(() => {
    db.query.mockReset();
    jest.restoreAllMocks();
  });

  it('GET /health should return ok', async () => {
    const response = await request(app).get('/health');

    expect(response.status).toBe(200);
    expect(response.body.status).toBe('ok');
  });

  it('GET /api/health should return api-ok', async () => {
    const response = await request(app).get('/api/health');

    expect(response.status).toBe(200);
    expect(response.body.status).toBe('api-ok');
  });

  it('POST /api/auth/register should create user', async () => {
    db.query
      .mockResolvedValueOnce({ rows: [] })
      .mockResolvedValueOnce({
        rows: [
          {
            id: 1,
            name: 'Admin Tutela',
            email: 'admin@tutela.test',
            role: 'admin',
            created_at: '2026-01-01T00:00:00.000Z',
          },
        ],
      });

    const response = await request(app).post('/api/auth/register').send({
      name: 'Admin Tutela',
      email: 'admin@tutela.test',
      password: '123456',
      role: 'admin',
    });

    expect(response.status).toBe(201);
    expect(response.body.user.email).toBe('admin@tutela.test');
    expect(response.body.token).toBeDefined();
  });

  it('POST /api/checkout should create checkout', async () => {
    jest.spyOn(checkoutService, 'create').mockResolvedValue({
      checkoutStatus: 'CHECKOUT_CREATED',
      gateway: 'cielo-checkout',
      payment: {
        id: 10,
        status: 'CHECKOUT_CREATED',
      },
      checkoutUrl: 'https://cielo.test/checkout/order_123',
    });

    const response = await request(app).post('/api/checkout').send({
      userId: 1,
      amount: 1990,
      customerName: 'Cliente Teste',
    });

    expect(response.status).toBe(201);
    expect(response.body.checkoutStatus).toBe('CHECKOUT_CREATED');
    expect(response.body.gateway).toBe('cielo-checkout');
    expect(response.body.checkoutUrl).toBe('https://cielo.test/checkout/order_123');
  });

  it('POST /api/checkout should return provider details on failure', async () => {
    const error = new Error('Checkout Cielo request failed');
    error.details = {
      status: 400,
      data: {
        message: 'Invalid request payload',
      },
    };

    jest.spyOn(console, 'error').mockImplementation(() => {});
    jest.spyOn(checkoutService, 'create').mockRejectedValue(error);

    const response = await request(app).post('/api/checkout').send({
      amount: 1990,
    });

    expect(response.status).toBe(400);
    expect(response.body.message).toBe('Falha ao criar checkout');
    expect(response.body.details.status).toBe(400);
    expect(response.body.details.data.message).toBe('Invalid request payload');
  });

  it('POST /api/subscriptions should create subscription', async () => {
    jest.spyOn(subscriptionService, 'create').mockResolvedValue({
      subscriptionStatus: 'CHECKOUT_CREATED',
      gateway: 'cielo-checkout',
      subscription: {
        id: 5,
        gateway_subscription_id: null,
        status: 'PENDING_CHECKOUT',
      },
      checkoutUrl: 'https://cielo.test/checkout/sub_123',
    });

    const response = await request(app).post('/api/subscriptions').send({
      userId: 1,
      planId: 2,
      amount: 4990,
      interval: 'Monthly',
    });

    expect(response.status).toBe(201);
    expect(response.body.subscriptionStatus).toBe('CHECKOUT_CREATED');
    expect(response.body.subscription.status).toBe('PENDING_CHECKOUT');
    expect(response.body.checkoutUrl).toBe('https://cielo.test/checkout/sub_123');
  });

  it('POST /api/webhook/cielo should process webhook payload', async () => {
    jest.spyOn(webhookService, 'process').mockResolvedValue({
      processed: true,
      paymentId: 'pay_123',
      paymentStatus: 'PAID',
      changeType: 'PaymentCaptured',
    });

    const response = await request(app).post('/api/webhook/cielo').send({
      PaymentId: 'pay_123',
      ChangeType: 'PaymentCaptured',
    });

    expect(response.status).toBe(200);
    expect(response.body.processed).toBe(true);
    expect(response.body.paymentStatus).toBe('PAID');
  });
});
