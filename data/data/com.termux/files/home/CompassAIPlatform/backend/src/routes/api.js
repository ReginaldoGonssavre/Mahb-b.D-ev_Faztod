const express = require('express');
const jwt = require('jsonwebtoken');
const router = express.Router();

const SECRET_KEY = process.env.JWT_SECRET || 'supersecretjwtkey'; // Use environment variable in production

// Middleware to verify JWT
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (token == null) return res.sendStatus(401); // No token

  jwt.verify(token, SECRET_KEY, (err, user) => {
    if (err) return res.sendStatus(403); // Invalid token
    req.user = user;
    next();
  });
};

// Protected API route
router.get('/protected', authenticateToken, (req, res) => {
  res.json({ message: `Welcome, ${req.user.username}! This is protected data.`, user: req.user });
});

module.exports = router;