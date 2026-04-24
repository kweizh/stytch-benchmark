const express = require('express');
const stytch = require('stytch');
require('dotenv').config();

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const PROJECT_ID = process.env.STYTCH_B2B_PROJECT_ID;
const SECRET = process.env.STYTCH_B2B_SECRET;

if (!PROJECT_ID || !SECRET) {
  console.error('Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables');
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: PROJECT_ID,
  secret: SECRET,
});

app.post('/validate', async (req, res) => {
  const { session_jwt } = req.body;

  if (!session_jwt) {
    return res.status(400).json({ error: 'session_jwt is required' });
  }

  try {
    // authenticateJwtLocal performs local validation using JWKS
    const session = await client.sessions.authenticateJwtLocal({
      session_jwt,
    });

    return res.status(200).json({
      member_id: session.member_id,
    });
  } catch (error) {
    console.error('JWT Validation Error:', error);
    return res.status(401).json({ error: 'Unauthorized' });
  }
});

app.listen(PORT, () => {
  console.log(`Stytch B2B Local JWT Validator listening on port ${PORT}`);
});
