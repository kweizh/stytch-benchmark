const express = require('express');
const cookieParser = require('cookie-parser');
const stytch = require('stytch');

const app = express();
app.use(cookieParser());
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const revokedSessions = new Set();

app.post('/register', async (req, res) => {
  const { email, password } = req.body;
  try {
    const resp = await client.passwords.create({
      email,
      password,
      session_duration_minutes: 60
    });
    res.cookie('stytch_session', resp.session_token);
    res.cookie('stytch_session_jwt', resp.session_jwt);
    res.json({ success: true });
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

app.post('/logout', async (req, res) => {
  const token = req.cookies.stytch_session;
  if (!token) return res.status(400).json({ error: 'No session token' });
  try {
    // Extract session_id from JWT and add to revokedSessions
    const jwt = req.cookies.stytch_session_jwt;
    if (jwt) {
      try {
        const { session } = await client.sessions.authenticateJwtLocal({ session_jwt: jwt });
        revokedSessions.add(session.session_id);
      } catch (_) {
        // If JWT decode fails, proceed with revocation anyway
      }
    }

    await client.sessions.revoke({ session_token: token });
    res.clearCookie('stytch_session');
    res.clearCookie('stytch_session_jwt');
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.get('/profile', async (req, res) => {
  const jwt = req.cookies.stytch_session_jwt;
  if (!jwt) return res.status(401).json({ error: 'No JWT' });
  try {
    const { session } = await client.sessions.authenticateJwtLocal({ session_jwt: jwt });
    // Check if session.session_id is in revokedSessions
    if (revokedSessions.has(session.session_id)) {
      return res.status(401).json({ error: 'Session revoked' });
    }

    res.json({ success: true, session_id: session.session_id });
  } catch (err) {
    res.status(401).json({ error: 'Invalid JWT' });
  }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
