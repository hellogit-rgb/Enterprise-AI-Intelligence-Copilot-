import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET || 'development-only-secret';

export function authenticateRequest(req, res, next) {
  const header = req.headers.authorization || '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : null;

  if (!token) {
    if (process.env.REQUIRE_AUTH === 'true') {
      return res.status(401).json({ error: 'Authentication required.' });
    }
    req.user = { sub: 'local-development', role: 'admin' };
    return next();
  }

  try {
    req.user = jwt.verify(token, JWT_SECRET);
    return next();
  } catch (error) {
    return res.status(401).json({ error: 'Invalid or expired token.' });
  }
}

export function requireRole(...roles) {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Insufficient permissions.' });
    }
    return next();
  };
}

export function createRateLimiter({ windowMs = 60_000, max = 60 } = {}) {
  const requests = new Map();
  return (req, res, next) => {
    const key = req.ip || req.socket.remoteAddress || 'unknown';
    const now = Date.now();
    const entry = requests.get(key);
    const current = !entry || now - entry.startedAt >= windowMs
      ? { startedAt: now, count: 0 }
      : entry;

    current.count += 1;
    requests.set(key, current);
    if (current.count > max) {
      return res.status(429).json({ error: 'Rate limit exceeded.' });
    }
    return next();
  };
}
