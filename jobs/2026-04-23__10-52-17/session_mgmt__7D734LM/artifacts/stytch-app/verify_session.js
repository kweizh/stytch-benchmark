const stytch = require("stytch");

const token = process.argv[2];

if (!token) {
  console.error("Usage: node verify_session.js <session_token>");
  process.exit(1);
}

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  console.error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.");
  process.exit(1);
}

const client = new stytch.Client({
  project_id: projectId,
  secret,
});

async function verifySession() {
  try {
    const response = await client.sessions.authenticate({
      session_token: token,
    });
    if (!response || !response.session || !response.session.user_id) {
      console.error("Session verification succeeded but user_id was not returned.");
      process.exit(1);
    }
    console.log(response.session.user_id);
  } catch (error) {
    const message = error?.message || "Failed to authenticate session token.";
    console.error(message);
    process.exit(1);
  }
}

verifySession();
