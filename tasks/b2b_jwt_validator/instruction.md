# Stytch B2B Local JWT Validator

## Background
Stytch B2B sessions can be represented as a `session_jwt` which has a 5-minute lifespan. Validating a JWT locally (using JWKS) is significantly faster than communicating with Stytch's API on every request.

## Requirements
Write a standalone Node.js Express service that exposes an endpoint to validate incoming B2B `session_jwt` tokens locally.

1.  **Endpoint**: `POST /validate`
2.  **Payload**: JSON body containing `{ "session_jwt": "<token>" }`.
3.  **Behavior**:
    *   The service MUST validate the JWT locally using the Stytch Node.js SDK (`authenticateJwtLocal` method) or a standard JWT library with the Stytch JWKS endpoint.
    *   It MUST NOT make a network call to Stytch's `authenticate` endpoint for every validation request.
    *   If the JWT is valid, return `200 OK` with `{ "member_id": "<member_id>" }`.
    *   If the JWT is invalid or expired, return `401 Unauthorized`.
4.  **Configuration**: Use `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` from the environment.

## Constraints
- **Project path**: `/home/user/app`
- **Start command**: `npm start`
- **Port**: 3000
- **Dependencies**: Use Node.js and Express. You may use the official `stytch` SDK or a custom JWT validator.

## Integrations
- Stytch
