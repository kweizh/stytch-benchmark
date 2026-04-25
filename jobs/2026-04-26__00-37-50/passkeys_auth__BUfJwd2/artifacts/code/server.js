const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const stytchClient = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /webauthn/register/start
app.post('/webauthn/register/start', async (req, res) => {
  const { user_id, domain } = req.body;
  try {
    const response = await stytchClient.webauthn.registerStart({
      user_id,
      domain,
      use_base64_url_encoding: true,
    });
    res.json(response);
  } catch (err) {
    res.status(400).json(err);
  }
});

// POST /webauthn/register
app.post('/webauthn/register', async (req, res) => {
  const { user_id, public_key_credential } = req.body;
  try {
    const response = await stytchClient.webauthn.register({
      user_id,
      public_key_credential,
    });
    res.json(response);
  } catch (err) {
    res.status(400).json(err);
  }
});

// POST /webauthn/authenticate/start
app.post('/webauthn/authenticate/start', async (req, res) => {
  const { domain } = req.body;
  try {
    const response = await stytchClient.webauthn.authenticateStart({
      domain,
    });
    res.json(response);
  } catch (err) {
    res.status(400).json(err);
  }
});

// POST /webauthn/authenticate
app.post('/webauthn/authenticate', async (req, res) => {
  const { public_key_credential } = req.body;
  try {
    const response = await stytchClient.webauthn.authenticate({
      public_key_credential,
    });
    res.json(response);
  } catch (err) {
    res.status(400).json(err);
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
