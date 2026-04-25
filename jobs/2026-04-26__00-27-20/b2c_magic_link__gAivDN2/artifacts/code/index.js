const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

// Initialize the Stytch client
const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /login
app.post('/login', async (req, res) => {
  const { email } = req.body;

  try {
    const response = await client.magicLinks.email.loginOrCreate({
      email: email,
      login_magic_link_url: 'http://localhost:3000/authenticate',
      signup_magic_link_url: 'http://localhost:3000/authenticate',
    });
    
    res.json(response);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// GET /authenticate
app.get('/authenticate', async (req, res) => {
  const { token } = req.query;

  try {
    const response = await client.magicLinks.authenticate({
      token: token,
    });
    
    res.json({
      success: true,
      user_id: response.user_id,
    });
  } catch (error) {
    res.status(401).json({ error: error.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
