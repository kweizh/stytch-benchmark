# Stytch B2B TOTP Setup

## Background
Stytch provides B2B authentication features, including Multi-Factor Authentication (MFA) via Time-Based One-Time Passcodes (TOTP). This task requires you to write a Python script that sets up TOTP for a specific B2B member.

## Requirements
Write a Python script at `/home/user/stytch_project/setup_totp.py` that accomplishes the following:
1. Accepts two command-line arguments: `organization_id` and `member_id`.
2. Initializes a Stytch B2B client using the `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` environment variables.
3. Creates a new TOTP instance for the member using the Stytch B2B API.
4. Extracts the TOTP `secret` from the response.
5. Uses the `pyotp` library to generate a valid 6-digit TOTP code based on the `secret`.
6. Authenticates the TOTP instance using the generated code to complete the enrollment process.
7. Writes a JSON file to `/home/user/stytch_project/totp_info.json` containing the `totp_registration_id` and the first recovery code from the creation response. The JSON structure should be:
   ```json
   {
     "totp_registration_id": "<registration_id>",
     "recovery_code": "<first_recovery_code>"
   }
   ```

## Implementation Guide
1. Ensure you have `stytch` and `pyotp` installed.
2. In `setup_totp.py`, instantiate the `stytch.B2BClient`.
3. Call `client.totps.create(...)` passing the `organization_id` and `member_id`.
4. From the response, get the `secret` and `recovery_codes`.
5. Use `pyotp.TOTP(secret).now()` to generate the current code.
6. Call `client.totps.authenticate(...)` passing the `organization_id`, `member_id`, and `code`.
7. Save the required information to `totp_info.json`.

## Constraints
- Project path: /home/user/stytch_project
- Log file: /home/user/stytch_project/output.log
- You must use the `trial_id` from `/logs/trial_id` if you need to create any uniquely named entities, though this script only requires the provided IDs.

## Integrations
- stytch