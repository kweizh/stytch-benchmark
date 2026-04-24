const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /users: Accepts JSON { "email": "user@example.com" }. 
// Creates a Stytch B2C user and returns { "user_id": "..." }.
app.post('/users', async (req, res) => {
  try {
    const { email } = req.body;
    const response = await client.users.create({
      email,
    });
    res.status(201).json({ user_id: response.user_id });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

// POST /totp/enroll: Accepts JSON { "user_id": "..." }. 
// Creates a TOTP instance for the user using Stytch, 
// and returns { "totp_id": "...", "secret": "..." }.
app.post('/totp/enroll', async (req, res) => {
  try {
    const { user_id } = req.body;
    const response = await client.totps.create({
      user_id,
    });
    res.status(200).json({
      totp_id: response.totp_id,
      secret: response.secret,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

// POST /totp/verify: Accepts JSON { "user_id": "...", "totp_code": "..." }. 
// Authenticates the TOTP code using Stytch, creating a session. 
// Returns { "session_token": "..." }.
app.post('/totp/verify', async (req, res) => {
  try {
    const { user_id, totp_code } = req.body;
    const response = await client.totps.authenticate({
      user_id,
      totp_code,
      session_duration_minutes: 60, // Create a session
    });
    res.status(200).json({ session_token: response.session_token });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
