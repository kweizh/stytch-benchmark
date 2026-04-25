const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const projectId = process.env.STYTCH_PROJECT_ID || '';
const secret = process.env.STYTCH_SECRET || '';

const client = new stytch.Client({
  project_id: projectId,
  secret: secret,
  env: projectId.startsWith('project-live-') ? stytch.envs.live : stytch.envs.test,
});

app.post('/users', async (req, res) => {
  try {
    const { email } = req.body;
    const response = await client.users.create({
      email: email
    });
    res.json({ user_id: response.user_id });
  } catch (error) {
    console.error('Error creating user:', error);
    res.status(500).json({ error: error.message || 'Internal Server Error' });
  }
});

app.post('/totp/enroll', async (req, res) => {
  try {
    const { user_id } = req.body;
    const response = await client.totps.create({
      user_id: user_id
    });
    res.json({
      totp_id: response.totp_id,
      secret: response.secret
    });
  } catch (error) {
    console.error('Error enrolling TOTP:', error);
    res.status(500).json({ error: error.message || 'Internal Server Error' });
  }
});

app.post('/totp/verify', async (req, res) => {
  try {
    const { user_id, totp_code } = req.body;
    const response = await client.totps.authenticate({
      user_id: user_id,
      totp_code: totp_code,
      session_duration_minutes: 60
    });
    res.json({ session_token: response.session_token });
  } catch (error) {
    console.error('Error verifying TOTP:', error);
    res.status(500).json({ error: error.message || 'Internal Server Error' });
  }
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
