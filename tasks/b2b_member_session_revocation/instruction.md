# Implement B2B Member Session Revocation

## Background
In B2B applications, members may need to log out or administrators may need to revoke a member's session for security reasons. You need to implement a simple Node.js Express server that exposes an endpoint to revoke a specific Stytch B2B session.

## Requirements
- Create a Node.js Express server listening on port 3000.
- Implement a `POST /revoke` endpoint that accepts a JSON body with a `session_token`.
- The endpoint must use the Stytch Node.js SDK to revoke the provided session token using the B2B Sessions Revoke API.
- If successful, return a 200 status code. If an error occurs, return an appropriate error status.

## Constraints
- Project path: `/home/user/project`
- Start command: `npm start` (or `node index.js`)
- Port: 3000

## Integrations
- Stytch B2B