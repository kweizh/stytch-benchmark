# Implement Stytch B2C Magic Link Signup and Login

## Background
You are building a Node.js Express application and need to implement a passwordless authentication flow using Stytch's Email Magic Links. This allows users to sign up or log in by clicking a link sent to their email.

## Requirements
- Create an Express server with two endpoints:
  1. `POST /login`: Takes an `email` in the JSON request body. It should use the Stytch Node.js SDK to send a magic link to that email by calling `loginOrCreate`. Set both `login_magic_link_url` and `signup_magic_link_url` to `http://localhost:3000/authenticate`.
  2. `GET /authenticate`: Accepts a `token` query parameter. It should use the Stytch Node.js SDK to authenticate the token. If successful, respond with a JSON object containing `{"success": true, "user_id": "<stytch_user_id>"}`. If it fails, respond with a 401 status code.
- The server must listen on port 3000.
- Use the `stytch` npm package.
- Configure the Stytch client using the `STYTCH_PROJECT_ID` and `STYTCH_SECRET` environment variables.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/stytch-app`.
2. Install `express` and `stytch`.
3. Create `index.js` setting up the Express server with JSON body parsing.
4. Initialize the Stytch client using environment variables.
5. Implement the `POST /login` and `GET /authenticate` routes as specified.

## Constraints
- Project path: `/home/user/stytch-app`
- Start command: `node index.js`
- Port: `3000`
- STYTCH_PROJECT_ID and STYTCH_SECRET will be provided in the environment.

## Integrations
- Stytch