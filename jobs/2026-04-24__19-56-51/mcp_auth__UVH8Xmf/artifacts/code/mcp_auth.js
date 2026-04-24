"use strict";

const stytch = require("stytch");

// ---------------------------------------------------------------------------
// Stytch B2B client – initialised once and reused across calls.
// Reads credentials from environment variables so secrets never live in code.
// ---------------------------------------------------------------------------
const STYTCH_PROJECT_ID = process.env.STYTCH_PROJECT_ID;
const STYTCH_SECRET = process.env.STYTCH_SECRET;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  throw new Error(
    "Missing required environment variables: STYTCH_PROJECT_ID and STYTCH_SECRET must both be set."
  );
}

const client = new stytch.B2BClient({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
});

// ---------------------------------------------------------------------------
// verifyAgentToken
//
// Verifies a Stytch B2B session JWT and returns the member_session object.
//
// @param {string} jwt - The session_jwt issued by Stytch for the B2B member.
// @returns {Promise<object>} Resolves with the member_session object on success.
// @throws {Error} Throws if the JWT is missing, invalid, or the session has
//                 expired / been revoked.
// ---------------------------------------------------------------------------
async function verifyAgentToken(jwt) {
  if (!jwt || typeof jwt !== "string") {
    throw new Error("verifyAgentToken: jwt must be a non-empty string.");
  }

  // authenticateJwt performs local JWT verification (signature + expiry) using
  // the project's JWKS – no network round-trip required for the happy path.
  // The SDK falls back to a remote call when the signing key is not yet cached.
  const response = await client.sessions.authenticateJwt({
    session_jwt: jwt,
  });

  // The SDK throws a StytchError for any failure (invalid signature, expired
  // token, revoked session, …), so reaching this line means the JWT is valid.
  return response.member_session;
}

module.exports = { verifyAgentToken };
