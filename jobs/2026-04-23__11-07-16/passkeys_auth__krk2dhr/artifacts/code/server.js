'use strict';

const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

// Initialize Stytch B2C client
const stytchClient = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /webauthn/register/start
// Accepts: user_id, domain
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
    res.json(err);
  }
});

// POST /webauthn/register
// Accepts: user_id, public_key_credential
app.post('/webauthn/register', async (req, res) => {
  const { user_id, public_key_credential } = req.body;
  try {
    const response = await stytchClient.webauthn.register({
      user_id,
      public_key_credential,
    });
    res.json(response);
  } catch (err) {
    res.json(err);
  }
});

// POST /webauthn/authenticate/start
// Accepts: domain
app.post('/webauthn/authenticate/start', async (req, res) => {
  const { domain } = req.body;
  try {
    const response = await stytchClient.webauthn.authenticateStart({
      domain,
    });
    res.json(response);
  } catch (err) {
    res.json(err);
  }
});

// POST /webauthn/authenticate
// Accepts: public_key_credential
app.post('/webauthn/authenticate', async (req, res) => {
  const { public_key_credential } = req.body;
  try {
    const response = await stytchClient.webauthn.authenticate({
      public_key_credential,
    });
    res.json(response);
  } catch (err) {
    res.json(err);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
