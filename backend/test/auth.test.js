import test from 'node:test';
import assert from 'node:assert/strict';
import jwt from 'jsonwebtoken';

process.env.JWT_SECRET = 'test-secret';

const { authenticateRequest, requireRole, createRateLimiter } = await import('../src/auth.js');

function response() {
  return {
    statusCode: 200,
    body: null,
    status(code) { this.statusCode = code; return this; },
    json(value) { this.body = value; return this; }
  };
}

test('rejects missing credentials when auth is required', () => {
  const previous = process.env.REQUIRE_AUTH;
  process.env.REQUIRE_AUTH = 'true';
  const result = response();
  authenticateRequest({ headers: {} }, result, () => assert.fail('should reject'));
  assert.equal(result.statusCode, 401);
  process.env.REQUIRE_AUTH = previous;
});

test('accepts a signed token and enforces role', () => {
  const token = jwt.sign({ sub: 'user-1', role: 'finance' }, 'test-secret');
  const req = { headers: { authorization: `Bearer ${token}` } };
  const res = response();
  authenticateRequest(req, res, () => {});
  assert.equal(req.user.role, 'finance');

  requireRole('finance')(req, res, () => { res.authorized = true; });
  assert.equal(res.authorized, true);
});

test('limits requests within a window', () => {
  const limiter = createRateLimiter({ max: 1 });
  const req = { ip: '127.0.0.1' };
  const first = response();
  const second = response();
  limiter(req, first, () => {});
  limiter(req, second, () => {});
  assert.equal(second.statusCode, 429);
});
