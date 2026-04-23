const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

app.post('/transfer', async (req, res) => {
  const { session_token } = req.body;

  try {
    const response = await client.sessions.authenticate({ session_token });
    const session = response.session;
    const factorCount = session.authentication_factors.length;

    if (factorCount >= 2) {
      return res.status(200).json({ success: true });
    } else {
      return res.status(403).json({ error: 'Step-up MFA required' });
    }
  } catch (err) {
    return res.status(401).send('Unauthorized');
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
