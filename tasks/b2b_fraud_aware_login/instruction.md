# Stytch B2B Fraud-Aware Login CLI

## Background
Stytch Device Fingerprinting protects B2B applications from automated attacks and risky logins. You need to implement a simple CLI script that integrates Stytch Device Fingerprinting to evaluate a user's risk level before allowing them to log in.

## Requirements
- Create a Node.js script `login.js` in `/home/user/project`.
- The script should receive a `telemetry_id` as the first command-line argument.
- Initialize the Stytch B2B client using `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` environment variables.
- The script must call the Stytch Device Fingerprinting Lookup API (e.g., via the Stytch SDK `client.fraud.fingerprints.lookup({ telemetry_id })` or by making an HTTP request to `https://test.stytch.com/v1/fraud/fingerprints/lookup` with Basic Auth using the project credentials).
- Check the `verdict.action` from the response:
  - If it is `"BLOCK"`, the script must print `"Access Denied: Blocked"` and exit with code 1.
  - If it is `"CHALLENGE"`, the script must print `"MFA Required"` and exit with code 1.
  - If it is `"ALLOW"`, the script must print `"Login Successful"` and exit with code 0.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/project`.
2. Install the `stytch` package.
3. Create `login.js`.
4. Read the `telemetry_id` from `process.argv[2]`.
5. Use the Stytch B2B client to look up the fingerprint.
6. Evaluate the verdict and print the appropriate message and exit code.

## Constraints
- Project path: `/home/user/project`
- Ensure the script handles errors from the API gracefully (e.g., invalid telemetry ID).

## Integrations
- Stytch B2B