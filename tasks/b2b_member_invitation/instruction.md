# Stytch B2B Member Invitation

## Background
You have a Python project at `/home/user/project`. Create a script `invite_member.py` that initializes a Stytch B2B Organization and sends an email invitation to a new member using the Stytch Python SDK.

## Requirements
- Create a Stytch B2B Organization named `Acme Corp ${trial_id}` with slug `acme-corp-${trial_id}`.
- Send an email invitation to `new-member-${trial_id}@example.com` to join the organization.
- Write the resulting Organization ID and Member ID to `/home/user/project/output.json`.

## Constraints
- Project path: /home/user/project
- Log file: /home/user/project/output.json
- Execution script: `invite_member.py`
- Use `stytch` Python package.
- Do not hardcode the suffix; it must be derived from `/logs/artifacts/trial_id`.

## Integrations
- Stytch