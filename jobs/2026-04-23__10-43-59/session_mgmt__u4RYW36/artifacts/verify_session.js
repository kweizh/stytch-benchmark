const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: process.env.STYTCH_ENV === 'live' ? stytch.envs.live : stytch.envs.test
});

async function verifySession() {
  const token = process.argv[2];
  if (!token) {
    console.error('Error: Session token is required as the first argument');
    process.exit(1);
  }

  try {
    const response = await client.sessions.authenticate({
      session_token: token
    });
    console.log(response.session.user_id);
  } catch (error) {
    console.error('Error authenticating session:', error.error_message || error.message || error);
    process.exit(1);
  }
}

verifySession();
