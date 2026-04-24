# Update Stytch B2B Organization Authentication Methods

## Background
You have a Stytch B2B project. You need to create a new B2B organization and then update its settings to restrict the allowed authentication methods. By default, organizations allow all authentication methods (`ALL_ALLOWED`). Your goal is to restrict them to only Single Sign-On (SSO) and Magic Links.

## Requirements
- Write a Python script `update_org.py` that uses the `stytch` Python library.
- Read `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` from environment variables to initialize the `stytch.B2BClient`.
- Read the `trial_id` from `/logs/trial_id`.
- Create a new B2B organization with the name `test-org-${trial_id}` and slug `test-org-${trial_id}`.
- Update the organization's settings so that `auth_methods` is set to `RESTRICTED` and `allowed_auth_methods` is set to `["sso", "magic_link"]`.

## Constraints
- Project path: `/home/user/stytch_project`
- Script to run: `python3 /home/user/stytch_project/update_org.py`

## Integrations
- Stytch