# Secure Session Revocation with Local JWTs

## Background
You have an Express.js application at `/home/user/app` that uses the Stytch Node.js SDK for B2C authentication.
The app uses local JWT verification (`authenticateJwtLocal`) in the `/profile` endpoint to minimize network calls.
However, there is a security vulnerability: when a user logs out via `/logout`, the session is revoked in the Stytch backend and cookies are cleared, but the local JWT remains cryptographically valid for up to 5 minutes. If an attacker intercepts the JWT before logout, they can still use it to access `/profile` until it expires.

## Requirements
1. Update the `/logout` endpoint to extract the `session_id` from the user's JWT and add it to the provided `revokedSessions` Set (an in-memory blocklist) before revoking the session.
2. Update the `/profile` endpoint to check if the authenticated session's `session_id` is in the `revokedSessions` Set. If it is, return a `401` status code with the JSON response `{"error": "Session revoked"}`.

## Implementation Guide
1. In `/logout`, use `client.sessions.authenticateJwtLocal({ session_jwt: req.cookies.stytch_session_jwt })` to decode the JWT and get the `session.session_id`, then add it to `revokedSessions`.
2. In `/profile`, after verifying the JWT, check `revokedSessions.has(session.session_id)`.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: 3000
- You must use the `revokedSessions` Set. Do not change `/profile` to use a network call (`authenticate`).