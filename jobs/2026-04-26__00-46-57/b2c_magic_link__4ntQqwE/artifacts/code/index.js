const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: process.env.STYTCH_PROJECT_ID && process.env.STYTCH_PROJECT_ID.startsWith('project-live') 
    ? stytch.envs.live 
    : stytch.envs.test,
});

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
    res.status(200).json({ message: 'Magic link sent' });
  } catch (error) {
    console.error('Login error:', error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/authenticate', async (req, res) => {
  const { token } = req.query;
  if (!token) {
    return res.status(400).json({ error: 'Token is required' });
  }

  try {
    const response = await client.magicLinks.authenticate({ token });
    res.json({
      success: true,
      user_id: response.user_id,
    });
  } catch (error) {
    console.error('Authentication error:', error);
    res.status(401).json({ success: false });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
