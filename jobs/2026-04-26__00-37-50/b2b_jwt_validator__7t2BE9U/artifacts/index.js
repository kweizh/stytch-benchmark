"use strict";

const express = require("express");
const stytch = require("stytch");

const PORT = 3000;

// ---------------------------------------------------------------------------
// Validate required environment variables up-front so the service fails fast
// ---------------------------------------------------------------------------
const { STYTCH_B2B_PROJECT_ID, STYTCH_B2B_SECRET } = process.env;

if (!STYTCH_B2B_PROJECT_ID || !STYTCH_B2B_SECRET) {
  console.error(
    "ERROR: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET environment variables must be set."
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Stytch B2B client
// The SDK fetches the JWKS from Stytch once (and caches it) so that every
// subsequent call to authenticateJwtLocal() is a pure local operation with
// no outbound network request to the Stytch API.
// ---------------------------------------------------------------------------
const stytchClient = new stytch.B2BClient({
  project_id: STYTCH_B2B_PROJECT_ID,
  secret: STYTCH_B2B_SECRET,
});

// ---------------------------------------------------------------------------
// Express app
// ---------------------------------------------------------------------------
const app = express();
app.use(express.json());

/**
 * POST /validate
 *
 * Body: { "session_jwt": "<token>" }
 *
 * Responses:
 *   200  { "member_id": "<member_id>" }   — JWT is valid
 *   400                                   — Missing or malformed request body
 *   401                                   — JWT is invalid or expired
 */
app.post("/validate", async (req, res) => {
  const { session_jwt } = req.body ?? {};

  if (!session_jwt || typeof session_jwt !== "string") {
    return res
      .status(400)
      .json({ error: "Request body must contain a 'session_jwt' string." });
  }

  try {
    // authenticateJwtLocal validates the JWT signature and expiry using the
    // locally cached JWKS — no call is made to Stytch's authenticate endpoint.
    const memberSession = await stytchClient.sessions.authenticateJwtLocal({
      session_jwt,
    });

    return res.status(200).json({ member_id: memberSession.member_id });
  } catch (err) {
    // Any error (expired token, bad signature, malformed JWT, …) → 401
    console.error("JWT validation failed:", err?.message ?? err);
    return res.status(401).json({ error: "Invalid or expired session_jwt." });
  }
});

// ---------------------------------------------------------------------------
// Start server
// ---------------------------------------------------------------------------
app.listen(PORT, () => {
  console.log(`Stytch B2B JWT validator listening on port ${PORT}`);
});
