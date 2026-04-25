const stytch = require("stytch");

const token = process.argv[2];

if (!token) {
  console.error("Usage: node verify_session.js <session_token>");
  process.exit(1);
}

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  console.error("STYTCH_PROJECT_ID and STYTCH_SECRET must be set in the environment.");
  process.exit(1);
}

const client = new stytch.Client({
  project_id: projectId,
  secret,
});

async function main() {
  try {
    const response = await client.sessions.authenticate({ session_token: token });
    if (!response || !response.user_id) {
      console.error("Session authenticated, but no user_id was returned.");
      process.exit(1);
    }

    console.log(response.user_id);
  } catch (error) {
    const message = error?.message || "Failed to authenticate session token.";
    console.error(message);
    process.exit(1);
  }
}

main();
