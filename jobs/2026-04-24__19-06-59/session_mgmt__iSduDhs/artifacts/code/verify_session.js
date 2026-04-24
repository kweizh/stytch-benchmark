const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: stytch.envs.test, // Defaulting to test environment, though not explicitly requested, it's safer for a generic script
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
    if (err.error_message) {
      console.error('Error authenticating session:', err.error_message);
    } else {
      console.error('Error authenticating session:', err.message || err);
    }
    process.exit(1);
  }
}

verifySession();
