const stytch = require('stytch');

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

async function verifyAgentToken(jwt) {
  try {
    const response = await client.sessions.authenticate({
      session_jwt: jwt,
    });
    return response.member_session;
  } catch (error) {
    throw new Error(`Failed to verify agent token: ${error.message}`);
  }
}

module.exports = { verifyAgentToken };
