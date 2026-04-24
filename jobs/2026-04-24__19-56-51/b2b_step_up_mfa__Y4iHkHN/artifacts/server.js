const express = require('express');
const cookieParser = require('cookie-parser');
const stytch = require('stytch');

const app = express();
app.use(express.json());
app.use(cookieParser());

const stytchClient = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

// Implement POST /sensitive-action here
app.post('/sensitive-action', async (req, res) => {
  const sessionToken = req.cookies.stytch_session;

  if (!sessionToken) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  let memberSession;
  try {
    const response = await stytchClient.sessions.authenticate({
      session_token: sessionToken,
    });
    memberSession = response.member_session;
  } catch (err) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  const factors = memberSession.authentication_factors || [];
  const mfaComplete =
    factors.length >= 2 ||
    factors.some((f) => f.type === 'otp' || f.type === 'totp');

  if (!mfaComplete) {
    return res.status(403).json({ error: 'MFA required' });
  }

  return res.status(200).json({ success: true });
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
