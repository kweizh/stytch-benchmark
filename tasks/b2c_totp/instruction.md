# Stytch B2C TOTP Flow API

## Background
Implement a TOTP authenticator app enrollment and verification flow for a B2C application using Express.js and the Stytch Node.js SDK.

## Requirements
Create an Express REST API with the following endpoints:
- `POST /users`: Accepts JSON `{ "email": "user@example.com" }`. Creates a Stytch B2C user and returns `{ "user_id": "..." }`.
- `POST /totp/enroll`: Accepts JSON `{ "user_id": "..." }`. Creates a TOTP instance for the user using Stytch, and returns `{ "totp_id": "...", "secret": "..." }` (extract the base32 secret from the Stytch response).
- `POST /totp/verify`: Accepts JSON `{ "user_id": "...", "totp_code": "..." }`. Authenticates the TOTP code using Stytch, creating a session. Returns `{ "session_token": "..." }`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/app`.
2. Install `express` and `stytch`.
3. Create `index.js` that sets up the Express server.
4. Configure the Stytch B2C client using the `STYTCH_PROJECT_ID` and `STYTCH_SECRET` environment variables.
5. Implement the three endpoints, ensuring they return the exact JSON keys required.
6. Start the server on port 3000.

## Constraints
- Project path: /home/user/app
- Start command: node index.js
- Port: 3000
- The Stytch client must use the B2C environment (test environment is fine, derived from the project ID).

## Integrations
- Stytch