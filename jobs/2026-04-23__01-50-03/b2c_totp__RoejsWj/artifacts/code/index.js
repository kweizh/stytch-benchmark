const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: process.env.STYTCH_PROJECT_ID && process.env.STYTCH_PROJECT_ID.startsWith('project-test-') 
    ? stytch.envs.test 
    : stytch.envs.live,
});

// POST /users: Creates a Stytch B2C user
app.post('/users', async (req, res) => {
  const { email } = req.body;
  try {
    const response = await client.users.create({ email });
    res.status(201).json({ user_id: response.user_id });
  } catch (error) {
    console.error(error);
    res.status(400).json({ error: error.error_message || 'Failed to create user' });
  }
});

// POST /totp/enroll: Creates a TOTP instance for the user
app.post('/totp/enroll', async (req, res) => {
  const { user_id } = req.body;
  try {
    const response = await client.totps.create({ user_id });
    res.status(200).json({ 
      totp_id: response.totp_id, 
      secret: response.secret 
    });
  } catch (error) {
    console.error(error);
    res.status(400).json({ error: error.error_message || 'Failed to enroll TOTP' });
  }
});

// POST /totp/verify: Authenticates the TOTP code
app.post('/totp/verify', async (req, res) => {
  const { user_id, totp_code } = req.body;
  try {
    const response = await client.totps.authenticate({
      user_id,
      totp_code,
      session_duration_minutes: 60,
    });
    res.status(200).json({ session_token: response.session_token });
  } catch (error) {
    console.error(error);
    res.status(400).json({ error: error.error_message || 'Failed to verify TOTP' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
