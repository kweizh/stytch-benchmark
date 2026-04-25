const stytch = require('stytch');

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  console.error('Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables');
  process.exit(1);
}

const client = new stytch.Client({
  project_id: projectId,
  secret: secret,
  env: projectId.startsWith('project-test-') ? stytch.envs.test : stytch.envs.live,
});

const sessionToken = process.argv[2];

if (!sessionToken) {
  console.error('Usage: node verify_session.js <session_token>');
  process.exit(1);
}

async function verifySession() {
  try {
    const response = await client.sessions.authenticate({
      session_token: sessionToken,
    });
    console.log(response.session.user_id);
  } catch (err) {
    console.error('Error authenticating session:', err);
    process.exit(1);
  }
}

verifySession();
