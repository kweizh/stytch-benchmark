FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Express.js app with Stytch SDK for step-up authentication task."

RUN cd /home/user/app && \
    cat > package.json <<'EOF'
{
  "name": "stytch-step-up",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "cookie-parser": "^1.4.6",
    "express": "^4.19.2",
    "stytch": "^10.5.0"
  },
  "devDependencies": {
    "supertest": "^7.0.0"
  }
}
EOF

RUN cd /home/user/app && \
    cat > app.js <<'EOF'
const express = require('express');
const stytch = require('stytch');
const cookieParser = require('cookie-parser');

const app = express();
app.use(cookieParser());
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID || 'project-test-123',
  secret: process.env.STYTCH_SECRET || 'secret-test-123',
});

// Export client so it can be mocked in tests
app.locals.stytchClient = client;

app.post('/transfer', async (req, res) => {
  const sessionToken = req.cookies['stytch_session'];
  if (!sessionToken) return res.status(401).send('Unauthorized');

  try {
    const { session } = await app.locals.stytchClient.sessions.authenticate({
      session_token: sessionToken,
    });
    
    // TODO: Implement Step-up Authentication Logic here
    // 1. Check if `session.authentication_factors` array contains a factor with `type` equal to 'totp'
    // 2. If it does NOT contain it, return 403 with text 'Step-up authentication required'
    
    res.status(200).send('Transfer successful');
  } catch (err) {
    res.status(401).send('Unauthorized');
  }
});

module.exports = app;
EOF

RUN cd /home/user/app && npm install

# Container contents:
#   - Node.js 24 installed
#   - /home/user/app - Express app with stytch SDK
#   - app.js contains the initial POST /transfer route

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
