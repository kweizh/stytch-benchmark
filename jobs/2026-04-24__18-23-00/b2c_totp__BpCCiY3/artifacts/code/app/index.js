const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const env = process.env.STYTCH_PROJECT_ID && process.env.STYTCH_PROJECT_ID.startsWith('project-live-') 
  ? stytch.envs.live 
  : stytch.envs.test;

const stytchClient = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID || '',
  secret: process.env.STYTCH_SECRET || '',
  env: env,
});

app.post('/users', async (req, res) => {
  try {
    const { email } = req.body;
    const response = await stytchClient.users.create({ email });
    res.json({ user_id: response.user_id });
  } catch (error) {
    res.status(error.status_code || 500).json({ error: error.error_message || error.message });
  }
});

app.post('/totp/enroll', async (req, res) => {
  try {
    const { user_id } = req.body;
    const response = await stytchClient.totps.create({ user_id });
    res.json({ 
      totp_id: response.totp_id, 
      secret: response.secret 
    });
  } catch (error) {
    res.status(error.status_code || 500).json({ error: error.error_message || error.message });
  }
});

app.post('/totp/verify', async (req, res) => {
  try {
    const { user_id, totp_code } = req.body;
    const response = await stytchClient.totps.authenticate({ 
      user_id,
      totp_code,
      session_duration_minutes: 60
    });
    res.json({ session_token: response.session_token });
  } catch (error) {
    res.status(error.status_code || 500).json({ error: error.error_message || error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
