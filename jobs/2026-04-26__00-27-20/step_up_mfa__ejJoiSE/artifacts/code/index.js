const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID || 'project-test-00000000-0000-0000-0000-000000000000',
  secret: process.env.STYTCH_SECRET || 'secret-test-11111111-1111-1111-1111-111111111111',
  env: process.env.STYTCH_ENV === 'live' ? stytch.envs.live : stytch.envs.test,
});

app.post('/transfer', async (req, res) => {
  const { session_token } = req.body;
  
  if (!session_token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const response = await client.sessions.authenticate({
      session_token: session_token
    });

    const session = response.session;
    if (session.authentication_factors.length < 2) {
      return res.status(403).json({ error: 'Step-up MFA required' });
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
