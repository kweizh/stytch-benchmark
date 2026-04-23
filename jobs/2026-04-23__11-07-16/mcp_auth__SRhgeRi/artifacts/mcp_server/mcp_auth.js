"use strict";

/**
 * mcp_auth.js
 *
 * MCP server authentication layer using the Stytch B2B SDK.
 *
 * Environment variables required:
 *   STYTCH_PROJECT_ID  – Stytch B2B project ID  (e.g. "project-live-…")
 *   STYTCH_SECRET      – Stytch B2B secret key   (e.g. "secret-live-…")
 */

const { B2BClient } = require("stytch");

// ---------------------------------------------------------------------------
// Lazy-initialised singleton client
// ---------------------------------------------------------------------------
let _client = null;

/**
 * Returns a shared B2BClient instance, initialised from environment variables.
 * Throws a descriptive error if the required variables are absent.
 *
 * @returns {B2BClient}
 */
function getClient() {
  if (_client) return _client;

  const projectId = process.env.STYTCH_PROJECT_ID;
  const secret = process.env.STYTCH_SECRET;

  if (!projectId) {
    throw new Error(
      "Missing environment variable: STYTCH_PROJECT_ID must be set before calling verifyAgentToken."
    );
  }
  if (!secret) {
    throw new Error(
      "Missing environment variable: STYTCH_SECRET must be set before calling verifyAgentToken."
    );
  }

  _client = new B2BClient({ project_id: projectId, secret });
  return _client;
}

// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------

/**
 * Verifies a Stytch B2B session JWT.
 *
 * Calls the Stytch `sessions.authenticateJwt` endpoint which:
 *   - Validates the JWT signature using Stytch's JWKS.
 *   - Confirms the session has not been revoked.
 *   - Returns fresh session data from the Stytch API.
 *
 * @param {string} jwt - The `session_jwt` issued by Stytch for a B2B member session.
 * @returns {Promise<object>} Resolves with the `member_session` object on success.
 * @throws {Error} Throws if the JWT is missing, invalid, expired, or revoked.
 */
async function verifyAgentToken(jwt) {
  if (!jwt || typeof jwt !== "string") {
    throw new Error("verifyAgentToken: jwt argument must be a non-empty string.");
  }

  const client = getClient();

  // authenticateJwt validates locally via JWKS then confirms with the API.
  // The response shape is: { member_session, member, organization, ... }
  const response = await client.sessions.authenticateJwt({ session_jwt: jwt });

  // member_session contains session metadata, member_id, organization_id, etc.
  return response.member_session;
}

module.exports = { verifyAgentToken };
