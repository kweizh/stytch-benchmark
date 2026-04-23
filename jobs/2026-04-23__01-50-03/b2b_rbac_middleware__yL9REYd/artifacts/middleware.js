const stytch = require('stytch');

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

/**
 * Middleware to authenticate Stytch B2B session and check RBAC permissions.
 */
const authMiddleware = async (req, res, next) => {
  const sessionToken = req.cookies?.stytch_session;

  if (!sessionToken) {
    return res.status(401).send('Unauthorized');
  }

  try {
    // Authenticate the session and perform RBAC check.
    // organization_id is omitted as per instructions if Stytch can infer it.
    const response = await client.sessions.authenticate({
      session_token: sessionToken,
      authorization_check: {
        resource_id: 'stytch.organization',
        action: 'write',
      },
    });

    // If successful, attach the member_session to the request object.
    req.member_session = response.member_session;
    next();
  } catch (error) {
    // Check if the error is due to insufficient permissions (403).
    if (error.status_code === 403) {
      return res.status(403).send('Forbidden');
    }

    // Default to 401 for other authentication failures (e.g., session expired/invalid).
    return res.status(401).send('Unauthorized');
  }
};

module.exports = { authMiddleware };
