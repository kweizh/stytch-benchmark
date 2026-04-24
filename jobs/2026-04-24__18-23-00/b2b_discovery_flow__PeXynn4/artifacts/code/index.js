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
  try {
    const { email } = req.body;
    const response = await client.magicLinks.email.discovery.send({
      email_address: email,
    });
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message || error });
  }
});

// 2. POST /api/discovery/authenticate
app.post('/api/discovery/authenticate', async (req, res) => {
  try {
    const { discovery_magic_links_token } = req.body;
    const response = await client.magicLinks.discovery.authenticate({
      discovery_magic_links_token,
    });
    res.json({
      intermediate_session_token: response.intermediate_session_token,
      discovered_organizations: response.discovered_organizations,
    });
  } catch (error) {
    res.status(500).json({ error: error.message || error });
  }
});

// 3. POST /api/discovery/exchange
app.post('/api/discovery/exchange', async (req, res) => {
  try {
    const { intermediate_session_token, organization_id } = req.body;
    const response = await client.discovery.intermediateSessions.exchange({
      intermediate_session_token,
      organization_id,
    });
    res.json({ member_session: response.member_session });
  } catch (error) {
    res.status(500).json({ error: error.message || error });
  }
});

// 4. POST /api/discovery/create
app.post('/api/discovery/create', async (req, res) => {
  try {
    const { intermediate_session_token, organization_name } = req.body;
    const response = await client.discovery.organizations.create({
      intermediate_session_token,
      organization_name,
    });
    res.json({
      organization: response.organization,
      member_session: response.member_session,
    });
  } catch (error) {
    res.status(500).json({ error: error.message || error });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
