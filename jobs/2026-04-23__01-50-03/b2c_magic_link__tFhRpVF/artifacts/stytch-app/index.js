const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: process.env.STYTCH_PROJECT_ID && process.env.STYTCH_PROJECT_ID.startsWith('project-test-') 
    ? stytch.envs.test 
    : stytch.envs.live,
});

app.post('/login', async (req, res) => {
  const { email } = req.body;
  try {
    await client.magicLinks.email.loginOrCreate({
      email,
      login_magic_link_url: 'http://localhost:3000/authenticate',
      signup_magic_link_url: 'http://localhost:3000/authenticate',
    });
    res.status(200).json({ message: 'Magic link sent' });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: error.message });
  }
});

app.get('/authenticate', async (req, res) => {
  const { token } = req.query;
  try {
    const response = await client.magicLinks.authenticate({
      token,
    });
    res.status(200).json({
      success: true,
      user_id: response.user_id,
    });
  } catch (error) {
    console.error(error);
    res.status(401).json({ success: false, error: 'Authentication failed' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
