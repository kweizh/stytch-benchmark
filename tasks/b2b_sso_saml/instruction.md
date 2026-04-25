# Configure SAML Connection for B2B Organization

## Background
Stytch provides robust B2B authentication features including enterprise SSO. Your task is to write a Python script that creates a new B2B organization and configures a SAML connection for it using the Stytch B2B API.

## Requirements
- Read the `trial_id` from `/logs/artifacts/trial_id`.
- Create a new Stytch B2B organization with the name `SAML Org ${trial_id}` and the slug `saml-org-${trial_id}`.
- Create a SAML connection for this organization.
- Update the SAML connection with the IdP SSO URL `https://idp.example.com/sso` and a dummy IdP entity ID `https://idp.example.com/entity`.
- The script must be saved to `/home/user/workspace/setup_saml.py` and execute successfully.

## Constraints
- Project path: `/home/user/workspace`
- Use `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` environment variables for authentication.

## Integrations
- Stytch