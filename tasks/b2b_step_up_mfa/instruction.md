# Stytch B2B Step-up MFA

## Background
You are building a B2B SaaS application using Express.js and the Stytch Node.js SDK. You need to protect a sensitive route so that it requires multi-factor authentication (MFA).

## Requirements
- You have an existing Express app in `/home/user/app`.
- Implement the `POST /sensitive-action` endpoint in `/home/user/app/server.js`.
- The endpoint must read the `stytch_session` cookie.
- Authenticate the session using `client.sessions.authenticate({ session_token })`.
- If the session is invalid or missing, return HTTP 401 with `{"error": "Unauthorized"}`.
- If the session is valid, check if the member has completed MFA. For this task, MFA is considered complete if the `member_session.authentication_factors` array contains at least two factors, or contains a factor of type `otp` or `totp`.
- If MFA is not complete, return HTTP 403 with `{"error": "MFA required"}`.
- If MFA is complete, return HTTP 200 with `{"success": true}`.

## Implementation Guide
1. Modify `/home/user/app/server.js` to implement the `POST /sensitive-action` route.
2. Use the initialized `stytchClient` provided in the file.
3. Read the session token from `req.cookies.stytch_session`.
4. Handle Stytch API errors gracefully (return 401 for invalid tokens).

## Constraints
- Project path: `/home/user/app`
- Start command: `npm start`
- Port: 3000

## Integrations
- Stytch