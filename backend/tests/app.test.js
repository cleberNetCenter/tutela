const request = require('supertest');

jest.mock('../src/services/db', () => ({
  query: jest.fn(),
}));

const db = require('../src/services/db');
const app = require('../src/app');

describe('Tutela API', () => {
  beforeEach(() => {
    db.query.mockReset();
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
});
