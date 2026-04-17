# Stytch Fraud-Aware Login

## Background
You have an Express.js application at `/home/user/app`. It has a basic `/login` endpoint. We want to protect this endpoint using Stytch's Device Fingerprinting (DFP) to prevent bot and fraud attacks.

## Requirements
- The Express app must use the `stytch` Node.js SDK to verify the `X-Telemetry-ID` header provided by the client.
- Initialize the Stytch Client using `process.env.STYTCH_PROJECT_ID` and `process.env.STYTCH_SECRET`.
- In the `POST /login` route, extract the `X-Telemetry-ID` header.
- If the header is missing, return a `400 Bad Request` with `{"error": "Telemetry ID missing"}`.
- Call the Fingerprint Lookup API: `client.fraud.fingerprint.lookup({ telemetry_id })`.
- Based on the `action` in the `verdict` object of the response:
  - If `ALLOW`, return `200 OK` with `{"success": true}`.
  - If `CHALLENGE`, return `401 Unauthorized` with `{"error": "MFA required"}`.
  - If `BLOCK`, return `403 Forbidden` with `{"error": "Access denied"}`.
- If the Stytch API call fails (e.g., invalid telemetry ID returning a 404), catch the error and return `403 Forbidden` with `{"error": "Access denied"}`.

## Implementation Guide
1. Modify `/home/user/app/index.js` to implement the above logic.
2. Ensure the Stytch client is initialized correctly using the `stytch` package.
3. The app is started with `npm start` and listens on port 3000.

## Constraints
- Project path: /home/user/app
- Start command: npm start
- Port: 3000
