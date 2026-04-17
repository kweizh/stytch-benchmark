# Stytch Passkeys with Express

## Background
Create an Express REST API that integrates Stytch WebAuthn (Passkeys) for authentication using the Stytch Node.js SDK.

## Requirements
- Initialize a Node.js project in `/home/user/app`.
- Install `express` and `stytch`.
- Create `server.js` that sets up the Express server on port 3000.
- Initialize the Stytch B2C client using `STYTCH_PROJECT_ID` and `STYTCH_SECRET` environment variables.
- Implement the following POST endpoints. They should parse JSON bodies and return the raw JSON responses from the Stytch SDK.
  - `POST /webauthn/register/start`: Accepts `user_id` and `domain`. Calls `stytchClient.webauthn.registerStart({ user_id, domain, use_base64_url_encoding: true })` and returns the response.
  - `POST /webauthn/register`: Accepts `user_id` and `public_key_credential`. Calls `stytchClient.webauthn.register({ user_id, public_key_credential })` and returns the response.
  - `POST /webauthn/authenticate/start`: Accepts `domain`. Calls `stytchClient.webauthn.authenticateStart({ domain })` and returns the response.
  - `POST /webauthn/authenticate`: Accepts `public_key_credential`. Calls `stytchClient.webauthn.authenticate({ public_key_credential })` and returns the response.

## Constraints
- Project path: `/home/user/app`
- Start command: `node server.js`
- Port: 3000
- Return the exact JSON response returned by the Stytch SDK (or the Stytch error object if it throws).