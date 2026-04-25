const stytch = require('stytch');

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

/**
 * Verifies a Stytch B2B session JWT.
 * @param {string} jwt - The session JWT to verify.
 * @returns {Promise<object>} - The member session object if successful.
 * @throws {Error} - If the JWT is invalid or authentication fails.
 */
async function verifyAgentToken(jwt) {
  try {
    const response = await client.sessions.authenticate({
      session_jwt: jwt,
    });
    return response.member_session;
  } catch (error) {
    console.error('Stytch authentication error:', error);
    throw error;
  }
}

module.exports = { verifyAgentToken };
