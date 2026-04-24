const stytch = require('stytch');

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  console.error('STYTCH_PROJECT_ID and STYTCH_SECRET environment variables are missing.');
  process.exit(1);
}

const client = new stytch.Client({
  project_id: projectId,
  secret: secret,
});

async function main() {
  const token = process.argv[2];

  if (!token) {
    console.error('Usage: node verify_session.js <session_token>');
    process.exit(1);
  }

  try {
    const res = await client.sessions.authenticate({
      session_token: token,
    });
    
    if (res.session && res.session.user_id) {
      console.log(res.session.user_id);
    } else {
      console.error('Authentication succeeded but user_id was not found.');
      process.exit(1);
    }
  } catch (error) {
    console.error('Failed to authenticate session:', error.message || error);
    process.exit(1);
  }
}

main();
