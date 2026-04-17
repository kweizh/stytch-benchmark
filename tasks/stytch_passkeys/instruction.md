# Stytch Passkey Registration

## Background
Stytch enables passwordless authentication via Passkeys (WebAuthn). The first step to register a Passkey is to generate the `public_key_credential_creation_options` from the backend.

## Requirements
Write a Node.js script `/home/user/app/index.js` that:
1. Imports the `stytch` SDK.
2. Initializes the Stytch `Client` using `STYTCH_PROJECT_ID` and `STYTCH_SECRET` from environment variables.
3. Reads a `user_id` from the first command-line argument (`process.argv[2]`).
4. Calls the `client.webauthn.registerStart` method with the provided `user_id`, `domain: "example.com"`, and `return_passkey_credential_options: true`.
5. Prints the `public_key_credential_creation_options` property from the response as a JSON string to standard output.

## Constraints
- Project path: `/home/user/app`
- The `stytch` SDK is already installed in `/home/user/app`.
- The script must be named `index.js` and be executable via `node index.js <user_id>`.

## Integrations
- Stytch