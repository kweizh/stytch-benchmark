const stytch = require('stytch');

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;
const sessionToken = process.argv[2];

if (!projectId || !secret) {
  console.error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.");
  process.exit(1);
}

if (!sessionToken) {
  console.error("Usage: node verify_session.js <session_token>");
  process.exit(1);
}

const client = new stytch.Client({
  project_id: projectId,
  secret: secret,
});

async function verifySession() {
  try {
    const response = await client.sessions.authenticate({
      session_token: sessionToken,
    });
    console.log(response.session.user_id);
  } catch (error) {
    console.error("Failed to authenticate session:", error.message || error);
    process.exit(1);
  }
}

verifySession();
