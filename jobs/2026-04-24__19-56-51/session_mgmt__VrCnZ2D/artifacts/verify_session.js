'use strict';

const stytch = require('stytch');

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  console.error('Error: STYTCH_PROJECT_ID and STYTCH_SECRET environment variables must be set.');
  process.exit(1);
}

const token = process.argv[2];

if (!token) {
  console.error('Usage: node verify_session.js <session_token>');
  process.exit(1);
}

const client = new stytch.Client({
  project_id: projectId,
  secret: secret,
});

client.sessions.authenticate({ session_token: token })
  .then((response) => {
    const userId = response.session.user_id;
    console.log(userId);
  })
  .catch((err) => {
    console.error('Error authenticating session:', err.message || err);
    process.exit(1);
  });
