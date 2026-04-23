const stytch = require("stytch");

const { STYTCH_PROJECT_ID, STYTCH_SECRET } = process.env;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  throw new Error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variable.");
}

const client = new stytch.B2BClient({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
});

const verifyAgentToken = async (jwt) => {
  if (!jwt) {
    throw new Error("session_jwt is required.");
  }

  const response = await client.sessions.authenticate({
    session_jwt: jwt,
  });

  return response.member_session;
};

module.exports = { verifyAgentToken };
