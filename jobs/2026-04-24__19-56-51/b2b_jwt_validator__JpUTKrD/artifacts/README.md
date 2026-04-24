# Stytch B2B Local JWT Validator

## Overview
A standalone Node.js/Express service that validates Stytch B2B `session_jwt`
tokens **locally** (via cached JWKS) without making a per-request network call
to Stytch's authenticate endpoint.

## Files
- `code/index.js`    — main Express application
- `code/package.json` — project manifest (express ^5, stytch ^14)

## Environment variables (required)
| Variable | Description |
|---|---|
| `STYTCH_B2B_PROJECT_ID` | Your Stytch B2B project ID (e.g. `project-live-...`) |
| `STYTCH_B2B_SECRET` | Your Stytch B2B secret key |

## Running
```bash
npm install          # install express + stytch
npm start            # node index.js  — listens on port 3000
```

## API

### `POST /validate`
**Request body**
```json
{ "session_jwt": "<token>" }
```

**Responses**
| Status | Body | Condition |
|---|---|---|
| 200 | `{ "member_id": "member-live-..." }` | JWT is valid & not expired |
| 400 | `{ "error": "..." }` | Missing / non-string `session_jwt` |
| 401 | `{ "error": "..." }` | JWT is invalid, expired, or malformed |
| 500 | `{ "error": "..." }` | Unexpected server error |

### `GET /health`
Returns `{ "status": "ok" }` — useful for load-balancer health checks.

## How local validation works
The Stytch Node SDK's `B2BClient` fetches the project's JWKS from Stytch on
first use and caches it in memory.  
`sessions.authenticateJwtLocal({ session_jwt })` then verifies the JWT
signature and expiry claims entirely in-process — **no outbound HTTP on the
hot path**.

The SDK re-fetches JWKS automatically when it encounters an unknown key ID
(`kid`), so rolling JWKS keys are handled transparently.
