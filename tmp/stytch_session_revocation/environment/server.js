const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

app.get('/protected', async (req, res) => {
  const authHeader = req.headers.authorization;
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid authorization header' });
  }

  const token = authHeader.split(' ')[1];

  try {
    // VULNERABLE TO REVOCATION DRIFT:
    // This only checks the local JWT signature and expiry.
    // If the session was revoked in Stytch, this will still succeed for up to 5 minutes.
    const { member_session } = await client.sessions.authenticateJwtLocal({
      session_jwt: token,
    });
    
    return res.json({ message: 'Success', member_id: member_session.member_id });
  } catch (err) {
    return res.status(401).json({ error: 'Unauthorized', details: err.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
