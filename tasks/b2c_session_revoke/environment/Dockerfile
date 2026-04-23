FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Express.js app with Stytch SDK for B2C session revocation task."

RUN cd /home/user/app && \
    cat > package.json <<'EOF'
{
  "name": "app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  }
}
EOF

RUN cd /home/user/app && \
    npm install express cookie-parser stytch

RUN cd /home/user/app && \
    cat > index.js <<'EOF'
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
    // TODO: Extract session_id from JWT and add to revokedSessions
    
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
    // TODO: Check if session.session_id is in revokedSessions
    
    res.json({ success: true, session_id: session.session_id });
  } catch (err) {
    res.status(401).json({ error: 'Invalid JWT' });
  }
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
EOF

# Container contents:
#   - Node.js installed
#   - /home/user/app with Express + Stytch application
#   - Unsecured /profile and /logout endpoints

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
