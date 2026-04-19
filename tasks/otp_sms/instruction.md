# Stytch OTP SMS Authentication with Node.js

## Background
Stytch provides a robust API for passwordless authentication. In this task, you will create a Node.js CLI script using the Stytch Node.js SDK to send a One-Time Passcode (OTP) via SMS to a user and authenticate the OTP code.

## Requirements
- Initialize a Node.js project in `/home/user/stytch_app`.
- Install the `stytch` package.
- Create a CLI script `stytch_sms.js` with two commands:
  1. `node stytch_sms.js send <phone_number>`: Sends an SMS OTP using the `stytch.Client` (B2C) `otps.sms.loginOrCreate` method and prints the resulting `phone_id` to stdout.
  2. `node stytch_sms.js authenticate <phone_id> <code>`: Authenticates the OTP using the `otps.authenticate` method and prints the resulting `user_id` to stdout.
- The script must read the Stytch credentials from the `STYTCH_PROJECT_ID` and `STYTCH_SECRET` environment variables.

## Implementation Guide
1. Run `npm init -y` and `npm install stytch` in `/home/user/stytch_app`.
2. Create `stytch_sms.js`.
3. Initialize the Stytch client:
   ```javascript
   const stytch = require('stytch');
   const client = new stytch.Client({
     project_id: process.env.STYTCH_PROJECT_ID,
     secret: process.env.STYTCH_SECRET,
   });
   ```
4. Implement the `send` command logic using `client.otps.sms.loginOrCreate({ phone_number })`.
5. Implement the `authenticate` command logic using `client.otps.authenticate({ method_id, code })`.

## Constraints
- Project path: `/home/user/stytch_app`
- The script must output only the requested ID (`phone_id` or `user_id`) to stdout on success, without any additional text.

## Integrations
- Stytch