const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: stytch.envs.test, // Defaulting to test environment
});

app.post('/webauthn/register/start', async (req, res) => {
  const { user_id, domain } = req.body;
  try {
    const response = await client.webauthn.registerStart({
      user_id,
      domain,
      use_base64_url_encoding: true,
    });
    res.json(response);
  } catch (error) {
    res.status(error.status_code || 500).json(error);
  }
});

app.post('/webauthn/register', async (req, res) => {
  const { user_id, public_key_credential } = req.body;
  try {
    const response = await client.webauthn.register({
      user_id,
      public_key_credential,
    });
    res.json(response);
  } catch (error) {
    res.status(error.status_code || 500).json(error);
  }
});

app.post('/webauthn/authenticate/start', async (req, res) => {
  const { domain } = req.body;
  try {
    const response = await client.webauthn.authenticateStart({
      domain,
    });
    res.json(response);
  } catch (error) {
    res.status(error.status_code || 500).json(error);
  }
});

app.post('/webauthn/authenticate', async (req, res) => {
  const { public_key_credential } = req.body;
  try {
    const response = await client.webauthn.authenticate({
      public_key_credential,
    });
    res.json(response);
  } catch (error) {
    res.status(error.status_code || 500).json(error);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
