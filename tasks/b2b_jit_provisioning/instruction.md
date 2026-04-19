# Stytch B2B JIT Provisioning with Allowed Tenants

## Background
Stytch's B2B Authentication product allows configuring Just-In-Time (JIT) Provisioning for organizations. You need to restrict JIT provisioning so that only members authenticating via specific OAuth tenants can join the organization automatically.

## Requirements
Write a Python script `setup_jit.py` that uses the `requests` library to update a Stytch B2B Organization's settings.
- The script must accept the organization ID as a command-line argument.
- It should make a `PUT` request to the Stytch test environment API: `https://test.stytch.com/v1/b2b/organizations/<organization_id>`.
- Set `oauth_tenant_jit_provisioning` to `RESTRICTED`.
- Set `allowed_oauth_tenants` to allow `slack` (with tenant ID `SLACK-123`) and `github` (with tenant ID `12345`).
- Use Basic Authentication with Project ID `project-test-00000000-0000-0000-0000-000000000000` and Secret `secret-test-11111111-1111-1111-1111-111111111111`.
- Print the status code of the response to stdout.

## Constraints
- Project path: `/home/user/stytch_project`
- The script must be named `setup_jit.py` and placed in the project path.
- Use the `requests` library for HTTP calls.