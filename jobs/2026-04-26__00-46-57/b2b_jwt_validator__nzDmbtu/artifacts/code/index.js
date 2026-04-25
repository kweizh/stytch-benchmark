require('dotenv').config();
const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;
const STYTCH_B2B_PROJECT_ID = process.env.STYTCH_B2B_PROJECT_ID;
const STYTCH_B2B_SECRET = process.env.STYTCH_B2B_SECRET;

if (!STYTCH_B2B_PROJECT_ID || !STYTCH_B2B_SECRET) {
  console.error('Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables.');
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: STYTCH_B2B_PROJECT_ID,
  secret: STYTCH_B2B_SECRET,
});

app.post('/validate', async (req, res) => {
  const { session_jwt } = req.body;

  if (!session_jwt) {
    return res.status(400).json({ error: 'Missing session_jwt in request body' });
  }

  try {
    // authenticateJwtLocal validates the JWT using the JWKS cached by the SDK
    const session = await client.sessions.authenticateJwtLocal({
      session_jwt,
    });

    return res.status(200).json({
      member_id: session.member_id,
    });
  } catch (err) {
    console.error('JWT Validation Error:', err);
    return res.status(401).json({ error: 'Unauthorized' });
  }
});

app.listen(PORT, () => {
  console.log(`Stytch B2B Local JWT Validator listening on port ${PORT}`);
});
