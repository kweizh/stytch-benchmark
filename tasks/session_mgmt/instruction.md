# Verify Stytch B2C Session

## Background
Stytch is a developer-first identity platform. In this task, you will use the Stytch Node.js SDK to verify a B2C `session_token`.

## Requirements
- Write a Node.js script `verify_session.js` that authenticates a Stytch B2C `session_token`.
- Read the session token from the first command-line argument (`process.argv[2]`).
- Use `stytch.Client` initialized with `STYTCH_PROJECT_ID` and `STYTCH_SECRET` environment variables.
- Call `client.sessions.authenticate({ session_token: token })` to verify the token.
- Print the resulting `user_id` from the session to the standard output.

## Implementation Guide
1. Navigate to `/home/user/stytch-app`.
2. Install the `stytch` Node.js package.
3. Create `verify_session.js` to initialize the client and authenticate the session.
4. Handle errors appropriately (e.g., if the token is invalid, exit gracefully).

## Constraints
- Project path: `/home/user/stytch-app`
- The script must be executable via `node verify_session.js <token>`.
- Do not hardcode project ID or secret; use `STYTCH_PROJECT_ID` and `STYTCH_SECRET`.

## Integrations
- None