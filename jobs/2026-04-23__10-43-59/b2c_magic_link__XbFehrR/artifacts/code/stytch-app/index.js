const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: process.env.STYTCH_PROJECT_ID?.startsWith('project-live-') ? stytch.envs.live : stytch.envs.test
});

app.post('/login', async (req, res) => {
  const { email } = req.body;
  
  try {
    const params = {
      email: email,
      login_magic_link_url: 'http://localhost:3000/authenticate',
      signup_magic_link_url: 'http://localhost:3000/authenticate'
    };
    const response = await client.magicLinks.email.loginOrCreate(params);
    res.status(200).json(response);
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.get('/authenticate', async (req, res) => {
  const { token } = req.query;
  
  try {
    const response = await client.magicLinks.authenticate({ token });
    res.status(200).json({ success: true, user_id: response.user_id });
  } catch (error) {
    console.error(error);
    res.status(401).json({ error: 'Unauthorized' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
