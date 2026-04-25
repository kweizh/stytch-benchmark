"use strict";

const stytch = require("stytch");

const { STYTCH_PROJECT_ID, STYTCH_SECRET } = process.env;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  throw new Error("STYTCH_PROJECT_ID and STYTCH_SECRET must be set in the environment");
}

const client = new stytch.B2BClient({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
});

async function verifyAgentToken(jwt) {
  if (!jwt) {
    throw new Error("session_jwt is required");
  }

  try {
    const response = await client.sessions.authenticate({
      session_jwt: jwt,
    });

    return response.member_session;
  } catch (error) {
    const message = error?.message || "Invalid session JWT";
    throw new Error(message);
  }
}

module.exports = { verifyAgentToken };
