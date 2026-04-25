"use strict";

const stytch = require("stytch");

/**
 * Lazily-initialised Stytch B2BClient singleton.
 * Credentials are read from environment variables so that no secrets are
 * hard-coded in source.
 */
let _client = null;

function getClient() {
  if (!_client) {
    const projectId = process.env.STYTCH_PROJECT_ID;
    const secret = process.env.STYTCH_SECRET;

    if (!projectId || !secret) {
      throw new Error(
        "Missing required environment variables: STYTCH_PROJECT_ID and/or STYTCH_SECRET"
      );
    }

    _client = new stytch.B2BClient({
      project_id: projectId,
      secret,
    });
  }

  return _client;
}

/**
 * Verify a Stytch B2B session JWT for an incoming MCP agent request.
 *
 * @param {string} jwt - The session_jwt issued by Stytch to the agent.
 * @returns {Promise<object>} Resolves with the `member_session` object on success.
 * @throws {Error} Throws if the JWT is missing, invalid, or the Stytch API
 *                 returns an error response.
 *
 * @example
 * const { verifyAgentToken } = require("./mcp_auth");
 *
 * app.use(async (req, res, next) => {
 *   const jwt = req.headers.authorization?.replace(/^Bearer\s+/i, "");
 *   try {
 *     req.memberSession = await verifyAgentToken(jwt);
 *     next();
 *   } catch (err) {
 *     res.status(401).json({ error: err.message });
 *   }
 * });
 */
async function verifyAgentToken(jwt) {
  if (!jwt || typeof jwt !== "string") {
    throw new Error("verifyAgentToken: a non-empty JWT string is required");
  }

  const client = getClient();

  // authenticateJwt validates the session JWT locally using the cached JWKS
  // (no round-trip to Stytch's API unless the key set needs refreshing).
  const response = await client.sessions.authenticateJwt({
    session_jwt: jwt,
  });

  // Stytch SDK throws on non-200 status codes, but guard defensively.
  if (!response.member_session) {
    throw new Error("verifyAgentToken: Stytch response missing member_session");
  }

  return response.member_session;
}

module.exports = { verifyAgentToken };
