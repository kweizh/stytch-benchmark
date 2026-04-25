const express = require('express');
const stytch = require('stytch');

const app = express();
const port = 3000;

app.use(express.json());

const stytchClient = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: process.env.STYTCH_ENV === 'live' ? stytch.envs.live : stytch.envs.test,
});

app.post('/webauthn/register/start', async (req, res) => {
  try {
    const { user_id, domain } = req.body;
    const response = await stytchClient.webauthn.registerStart({
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
  try {
    const { user_id, public_key_credential } = req.body;
    const response = await stytchClient.webauthn.register({
      user_id,
      public_key_credential,
    });
    res.json(response);
  } catch (error) {
    res.status(error.status_code || 500).json(error);
  }
});

app.post('/webauthn/authenticate/start', async (req, res) => {
  try {
    const { domain } = req.body;
    const response = await stytchClient.webauthn.authenticateStart({
      domain,
    });
    res.json(response);
  } catch (error) {
    res.status(error.status_code || 500).json(error);
  }
});

app.post('/webauthn/authenticate', async (req, res) => {
  try {
    const { public_key_credential } = req.body;
    const response = await stytchClient.webauthn.authenticate({
      public_key_credential,
    });
    res.json(response);
  } catch (error) {
    res.status(error.status_code || 500).json(error);
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
