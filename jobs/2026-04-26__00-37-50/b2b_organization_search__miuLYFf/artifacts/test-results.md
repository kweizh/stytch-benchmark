# B2B Discovery Organizations API - Test Results

## Server
- Running on port 3000 via `node index.js`

## Test 1: Missing token (returns 400)
```
POST /api/discovery/organizations
Body: {}

Response (400):
{"error_type":"missing_intermediate_session_token","error_message":"intermediate_session_token is required in the request body"}
```

## Test 2: Invalid token (Stytch error propagated, returns 400)
```
POST /api/discovery/organizations
Body: {"intermediate_session_token": "invalid-token-for-test"}

Response (400):
{"error_type":"invalid_session_token","error_message":"Session token format is invalid.","error_url":"https://stytch.com/docs/api/errors/400#invalid_session_token","request_id":"request-id-test-30558daf-fb03-4294-9fc2-26653499e0cd"}
```

## Test 3: Valid token (200 with discovered organizations)
- A valid intermediate_session_token from a real Stytch B2B auth flow would return the list of organizations.
