const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID || '',
  secret: process.env.STYTCH_SECRET || '',
  env: stytch.envs.test,
});

app.post('/transfer', async (req, res) => {
  const { session_token } = req.body;

  if (!session_token) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  try {
    const response = await client.sessions.authenticate({
      session_token: session_token,
    });

    const factors = response.session.authentication_factors || [];
    if (factors.length < 2) {
      return res.status(403).json({ error: 'Step-up MFA required' });
    }

    return res.status(200).json({ success: true });
  } catch (err) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
