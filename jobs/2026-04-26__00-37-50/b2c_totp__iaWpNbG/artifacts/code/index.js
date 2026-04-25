'use strict';

const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

// Initialize Stytch B2C client using environment variables.
// The SDK selects the env (test vs live) automatically based on the project_id prefix.
const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /users
// Body: { "email": "user@example.com" }
// Response: { "user_id": "..." }
app.post('/users', async (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ error: 'email is required' });
  }

  try {
    const response = await client.users.create({ email });
    return res.status(201).json({ user_id: response.user_id });
  } catch (err) {
    console.error('POST /users error:', err);
    return res.status(500).json({ error: err.message || 'Failed to create user' });
  }
});

// POST /totp/enroll
// Body: { "user_id": "..." }
// Response: { "totp_id": "...", "secret": "..." }
app.post('/totp/enroll', async (req, res) => {
  const { user_id } = req.body;

  if (!user_id) {
    return res.status(400).json({ error: 'user_id is required' });
  }

  try {
    const response = await client.totps.create({ user_id });
    return res.status(201).json({
      totp_id: response.totp_id,
      secret: response.secret,
    });
  } catch (err) {
    console.error('POST /totp/enroll error:', err);
    return res.status(500).json({ error: err.message || 'Failed to enroll TOTP' });
  }
});

// POST /totp/verify
// Body: { "user_id": "...", "totp_code": "..." }
// Response: { "session_token": "..." }
app.post('/totp/verify', async (req, res) => {
  const { user_id, totp_code } = req.body;

  if (!user_id || !totp_code) {
    return res.status(400).json({ error: 'user_id and totp_code are required' });
  }

  try {
    const response = await client.totps.authenticate({
      user_id,
      totp_code,
      session_duration_minutes: 60,
    });
    return res.status(200).json({ session_token: response.session_token });
  } catch (err) {
    console.error('POST /totp/verify error:', err);
    return res.status(500).json({ error: err.message || 'Failed to verify TOTP' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
