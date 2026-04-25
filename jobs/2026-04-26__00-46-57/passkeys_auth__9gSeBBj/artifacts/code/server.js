const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID || '',
  secret: process.env.STYTCH_SECRET || '',
  env: process.env.STYTCH_PROJECT_ID && process.env.STYTCH_PROJECT_ID.startsWith('project-live-') ? stytch.envs.live : stytch.envs.test,
});

app.post('/webauthn/register/start', async (req, res) => {
  try {
    const { user_id, domain } = req.body;
    const response = await client.webauthn.registerStart({
      user_id,
      domain,
      use_base64_url_encoding: true,
    });
    res.json(response);
  } catch (err) {
    res.status(err.status_code || 500).json(err);
  }
});

app.post('/webauthn/register', async (req, res) => {
  try {
    const { user_id, public_key_credential } = req.body;
    const response = await client.webauthn.register({
      user_id,
      public_key_credential,
    });
    res.json(response);
  } catch (err) {
    res.status(err.status_code || 500).json(err);
  }
});

app.post('/webauthn/authenticate/start', async (req, res) => {
  try {
    const { domain } = req.body;
    const response = await client.webauthn.authenticateStart({
      domain,
    });
    res.json(response);
  } catch (err) {
    res.status(err.status_code || 500).json(err);
  }
});

app.post('/webauthn/authenticate', async (req, res) => {
  try {
    const { public_key_credential } = req.body;
    const response = await client.webauthn.authenticate({
      public_key_credential,
    });
    res.json(response);
  } catch (err) {
    res.status(err.status_code || 500).json(err);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
