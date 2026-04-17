# Set up B2B SSO with SAML integration using Stytch

## Background
You are building a B2B SaaS application and need to programmatically configure a SAML Single Sign-On (SSO) connection for a new tenant organization using the Stytch Python SDK.

## Requirements
Write a Python script at `/home/user/stytch_sso/create_saml.py` that:
1. Initializes a Stytch `B2BClient` using the test project credentials.
2. Calls the Stytch API to create a SAML connection for the specified organization.
3. Prints the resulting `connection_id` to standard output.

## Implementation Guide
1. Import the `stytch` module.
2. Create a `stytch.B2BClient` with:
   - `project_id`: `project-test-123`
   - `secret`: `secret-test-456`
3. Call `client.sso.saml.create_connection` with the following parameters:
   - `organization_id`: `org-123`
   - `display_name`: `Acme SAML`
   - `identity_provider`: `okta`
4. Extract `connection.connection_id` from the response and print it.

*Note: Do not run the script to test against real Stytch servers, as the credentials are fake. Just write the script correctly.*

## Constraints
- Project path: `/home/user/stytch_sso`
- File to create: `/home/user/stytch_sso/create_saml.py`