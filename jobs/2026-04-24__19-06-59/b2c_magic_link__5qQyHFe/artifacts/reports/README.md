# Stytch B2C Magic Link Implementation

This application implements a passwordless authentication flow using Stytch Email Magic Links.

## Endpoints

### POST /login
Sends a magic link to the provided email.
- Body: `{"email": "user@example.com"}`
- Success Response: `200 OK`

### GET /authenticate
Authenticates the token from the magic link.
- Query Param: `token`
- Success Response: `200 OK` with `{"success": true, "user_id": "..."}`
- Failure Response: `401 Unauthorized`

## Setup
1. Install dependencies: `npm install`
2. Set environment variables: `STYTCH_PROJECT_ID`, `STYTCH_SECRET`
3. Start server: `node index.js`
