# Implement Stytch B2B Discovery Flow API

## Background
Stytch B2B provides a "Discovery" flow that allows End Users to authenticate without specifying an Organization in advance. This is done via a Discovery Magic Link flow. After an End User is authenticated, an Intermediate Session is returned along with a list of associated Organizations. The user can then exchange this session to log into an existing organization or create a new one.

## Requirements
Implement an Express.js REST API in `/home/user/project` that uses the `stytch` Node.js SDK to provide the following endpoints:

1. **`POST /api/discovery/send`**: 
   - Accepts JSON: `{ "email": "..." }`
   - Calls Stytch to send a discovery magic link to the provided email.
   - Returns the Stytch API response.

2. **`POST /api/discovery/authenticate`**: 
   - Accepts JSON: `{ "discovery_magic_links_token": "..." }`
   - Calls Stytch to authenticate the discovery magic link token.
   - Returns the `intermediate_session_token` and `discovered_organizations`.

3. **`POST /api/discovery/exchange`**: 
   - Accepts JSON: `{ "intermediate_session_token": "...", "organization_id": "..." }`
   - Calls Stytch to exchange the intermediate session for a full member session in the specified organization.
   - Returns the full `member_session`.

4. **`POST /api/discovery/create`**: 
   - Accepts JSON: `{ "intermediate_session_token": "...", "organization_name": "..." }`
   - Calls Stytch to create a new organization using the intermediate session.
   - Returns the newly created `organization` and `member_session`.

## Constraints
- Project path: `/home/user/project`
- Start command: `node index.js`
- Port: 3000
- Read Stytch credentials from `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` environment variables.

## Integrations
- Stytch