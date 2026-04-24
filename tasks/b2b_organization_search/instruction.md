# B2B Organization Search via Discovery

## Background
You need to implement a REST API endpoint that allows an authenticated user to discover and list the B2B organizations they are associated with or eligible to join. This utilizes Stytch's B2B Discovery APIs.

## Requirements
- Set up an Express.js server running on port 3000.
- Implement a `POST /api/discovery/organizations` endpoint.
- The endpoint must accept a JSON body with an `intermediate_session_token`.
- Use the Stytch Node.js SDK (`stytch`) to call the B2B Discovery Organizations List method.
- Return the discovered organizations in the response as JSON (status 200).
- If the token is invalid or missing, propagate the error from Stytch (e.g. return 400 with the error details).

## Constraints
- Project path: `/home/user/project`
- Start command: `node index.js`
- Port: 3000
- You MUST use real systems and API keys from the environment (`STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET`). NEVER use fake dependencies nor mock the target.