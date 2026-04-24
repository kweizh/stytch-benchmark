const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

// Initialize Stytch client using environment variables
const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /login - Send a magic link to the provided email
app.post('/login', async (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ error: 'Email is required' });
  }

  try {
    await client.magicLinks.email.loginOrCreate({
      email,
      login_magic_link_url: 'http://localhost:3000/authenticate',
      signup_magic_link_url: 'http://localhost:3000/authenticate',
    });

    return res.json({ success: true, message: 'Magic link sent to ' + email });
  } catch (err) {
    console.error('Error sending magic link:', err);
    return res.status(500).json({ error: 'Failed to send magic link', details: err.message });
  }
});

// GET /authenticate - Verify the magic link token
app.get('/authenticate', async (req, res) => {
  const { token } = req.query;

  if (!token) {
    return res.status(400).json({ error: 'Token is required' });
  }

  try {
    const response = await client.magicLinks.authenticate({ token });

    return res.json({ success: true, user_id: response.user_id });
  } catch (err) {
    console.error('Error authenticating token:', err);
    return res.status(401).json({ error: 'Authentication failed', details: err.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
