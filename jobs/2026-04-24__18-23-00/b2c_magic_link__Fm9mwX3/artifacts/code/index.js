const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

// Initialize Stytch client using environment variables
const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /login endpoint
app.post('/login', async (req, res) => {
  const { email } = req.body;
  
  if (!email) {
    return res.status(400).json({ error: 'Email is required in the request body' });
  }

  try {
    const response = await client.magicLinks.email.loginOrCreate({
      email,
      login_magic_link_url: 'http://localhost:3000/authenticate',
      signup_magic_link_url: 'http://localhost:3000/authenticate',
    });
    res.json(response);
  } catch (error) {
    console.error('Error sending magic link:', error);
    res.status(500).json({ error: error.message || 'Internal Server Error' });
  }
});

// GET /authenticate endpoint
app.get('/authenticate', async (req, res) => {
  const { token } = req.query;

  if (!token) {
    return res.status(400).json({ error: 'Token query parameter is required' });
  }

  try {
    const response = await client.magicLinks.authenticate({
      token,
    });
    
    // Respond with success and user_id as specified
    res.json({
      success: true,
      user_id: response.user_id,
    });
  } catch (error) {
    console.error('Error authenticating token:', error);
    // Respond with 401 status code if authentication fails
    res.status(401).json({ error: 'Authentication failed' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is listening on port ${PORT}`);
});
