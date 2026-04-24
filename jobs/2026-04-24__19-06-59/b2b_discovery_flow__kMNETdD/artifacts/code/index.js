require('dotenv').config();
const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

// 1. POST /api/discovery/send
app.post('/api/discovery/send', async (req, res) => {
  const { email } = req.body;
  try {
    const response = await client.magicLinks.discovery.send({
      email_address: email,
    });
    res.status(200).json(response);
  } catch (error) {
    res.status(400).json(error);
  }
});

// 2. POST /api/discovery/authenticate
app.post('/api/discovery/authenticate', async (req, res) => {
  const { discovery_magic_links_token } = req.body;
  try {
    const response = await client.magicLinks.discovery.authenticate({
      discovery_magic_links_token,
    });
    res.status(200).json({
      intermediate_session_token: response.intermediate_session_token,
      discovered_organizations: response.discovered_organizations,
    });
  } catch (error) {
    res.status(400).json(error);
  }
});

// 3. POST /api/discovery/exchange
app.post('/api/discovery/exchange', async (req, res) => {
  const { intermediate_session_token, organization_id } = req.body;
  try {
    const response = await client.discovery.intermediateSessions.exchange({
      intermediate_session_token,
      organization_id,
    });
    res.status(200).json({
      member_session: response.member_session,
    });
  } catch (error) {
    res.status(400).json(error);
  }
});

// 4. POST /api/discovery/create
app.post('/api/discovery/create', async (req, res) => {
  const { intermediate_session_token, organization_name } = req.body;
  try {
    const response = await client.discovery.organizations.create({
      intermediate_session_token,
      organization_name,
    });
    res.status(200).json({
      organization: response.organization,
      member_session: response.member_session,
    });
  } catch (error) {
    res.status(400).json(error);
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
