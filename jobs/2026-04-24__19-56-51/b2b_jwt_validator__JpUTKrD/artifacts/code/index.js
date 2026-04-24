"use strict";

const express = require("express");
const stytch = require("stytch");

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------
const PROJECT_ID = process.env.STYTCH_B2B_PROJECT_ID;
const SECRET = process.env.STYTCH_B2B_SECRET;
const PORT = process.env.PORT || 3000;

if (!PROJECT_ID || !SECRET) {
  console.error(
    "ERROR: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET environment variables are required."
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Stytch B2B client
// The SDK automatically fetches and caches the JWKS from Stytch so that
// subsequent calls to authenticateJwtLocal() are fully offline/local.
// ---------------------------------------------------------------------------
const stytchClient = new stytch.B2BClient({
  project_id: PROJECT_ID,
  secret: SECRET,
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
 * Validates the JWT locally using the cached JWKS — no per-request network
 * call to Stytch's authenticate endpoint.
 *
 * Responses:
 *   200  { "member_id": "<member_id>" }   – valid JWT
 *   400  { "error": "..." }               – missing / malformed request
 *   401  { "error": "..." }               – invalid or expired JWT
 */
app.post("/validate", async (req, res) => {
  const { session_jwt } = req.body || {};

  if (!session_jwt || typeof session_jwt !== "string") {
    return res
      .status(400)
      .json({ error: 'Missing or invalid "session_jwt" in request body.' });
  }

  try {
    // authenticateJwtLocal validates the JWT signature and expiry entirely
    // using the locally cached JWKS — it never calls Stytch's /authenticate
    // endpoint on the hot path.
    const result = await stytchClient.sessions.authenticateJwtLocal({
      session_jwt,
    });

    const member_id = result.member_session.member_id;
    return res.status(200).json({ member_id });
  } catch (err) {
    // The SDK throws a StytchError for invalid / expired JWTs
    const isAuthError =
      err?.error_type === "jwt_expired" ||
      err?.error_type === "jwt_invalid" ||
      err?.error_type === "session_not_found" ||
      err?.status_code === 401 ||
      err?.status_code === 403 ||
      // jose / jsonwebtoken library errors thrown internally by the SDK
      err?.code === "ERR_JWT_EXPIRED" ||
      err?.code === "ERR_JWS_INVALID" ||
      err?.code === "ERR_JWT_CLAIM_VALIDATION_FAILED" ||
      (err instanceof Error &&
        /expired|invalid|signature|jwt/i.test(err.message));

    if (isAuthError) {
      return res.status(401).json({ error: "Invalid or expired session JWT." });
    }

    // Unexpected error (e.g. JWKS fetch failure on cold start)
    console.error("Unexpected error during JWT validation:", err);
    return res.status(500).json({ error: "Internal server error." });
  }
});

// ---------------------------------------------------------------------------
// Health-check (optional, handy for load-balancers / smoke tests)
// ---------------------------------------------------------------------------
app.get("/health", (_req, res) => res.json({ status: "ok" }));

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------
app.listen(PORT, () => {
  console.log(`Stytch B2B JWT validator listening on port ${PORT}`);
  console.log(`Project ID: ${PROJECT_ID}`);
});
