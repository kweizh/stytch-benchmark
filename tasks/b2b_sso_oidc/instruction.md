# Configure Stytch B2B OIDC Connection

## Background
You need to write a Python script that uses the Stytch B2B API to create a new organization and configure an OIDC SSO connection for it.

## Requirements
- Read the `trial_id` from `/logs/trial_id`.
- Create a new B2B Organization with the name `test-org-${trial_id}` and slug `test-org-${trial_id}`.
- Create an OIDC SSO connection for this organization with the display name `My OIDC Connection`.
- Update the OIDC connection to include the following configuration so it becomes active:
  - `client_id`: `mock-client-id`
  - `client_secret`: `mock-client-secret`
  - `issuer`: `https://mock-idp.com`
  - `authorization_url`: `https://mock-idp.com/auth`
  - `token_url`: `https://mock-idp.com/token`
  - `userinfo_url`: `https://mock-idp.com/userinfo`
  - `jwks_url`: `https://mock-idp.com/jwks`
- The script should be named `configure_oidc.py` and saved in `/home/user/project`.
- Run the script and save its standard output to `/home/user/project/output.log`.

## Constraints
- Project path: `/home/user/project`
- Log file: `/home/user/project/output.log`
- Note: Always use the `trial_id` suffix for the organization name and slug to avoid conflicts.

## Integrations
- Stytch