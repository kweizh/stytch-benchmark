# Stytch Step-Up MFA

## Background
In sensitive operations like financial transfers, it's common to require Step-Up Authentication (MFA). You will build an Express.js endpoint that uses the Stytch Node.js SDK to enforce this.

## Requirements
- Create an Express.js server in `/home/user/app`.
- Implement a `POST /transfer` endpoint that accepts a JSON body containing a `session_token`.
- Use the `stytch` Node.js SDK (B2C Client) to authenticate the session.
- If the session is invalid, return a `401 Unauthorized` status code.
- If the session is valid but has fewer than 2 authentication factors, return a `403 Forbidden` status code with the JSON response `{"error": "Step-up MFA required"}`.
- If the session is valid and has 2 or more authentication factors, return a `200 OK` status code with the JSON response `{"success": true}`.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/app`.
2. Install `express` and `stytch`.
3. Create `index.js` that initializes the Stytch B2C client using `STYTCH_PROJECT_ID` and `STYTCH_SECRET` environment variables.
4. Implement the `POST /transfer` endpoint to check `session.authentication_factors.length`.
5. Start the server on port 3000.

## Constraints
- Project path: `/home/user/app`
- Start command: `node index.js`
- Port: 3000