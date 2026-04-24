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

  try {
    const { member_session } = await stytchClient.sessions.authenticate({
      session_token: sessionToken,
    });

    const factors = member_session.authentication_factors || [];
    const hasTwoFactors = factors.length >= 2;
    const hasOtpOrTotp = factors.some(
      (factor) => factor.type === 'otp' || factor.type === 'totp'
    );

    if (hasTwoFactors || hasOtpOrTotp) {
      return res.status(200).json({ success: true });
    } else {
      return res.status(403).json({ error: 'MFA required' });
    }
  } catch (error) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
