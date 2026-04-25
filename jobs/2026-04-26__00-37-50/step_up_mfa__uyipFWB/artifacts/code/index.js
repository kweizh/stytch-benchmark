const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

// Initialize Stytch B2C client using environment variables
const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

// POST /transfer — Step-Up MFA protected endpoint
app.post('/transfer', async (req, res) => {
  const { session_token } = req.body;

  try {
    // Authenticate the session with Stytch
    const response = await client.sessions.authenticate({ session_token });
    const session = response.session;

    // Check the number of authentication factors
    if (session.authentication_factors.length >= 2) {
      return res.status(200).json({ success: true });
    } else {
      return res.status(403).json({ error: 'Step-up MFA required' });
    }
  } catch (err) {
    // Any error from Stytch (invalid/expired token, etc.) → 401 Unauthorized
    return res.status(401).json({ error: 'Unauthorized' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
