# Delete a B2B Organization

## Background
You have a Stytch B2B project configured. Your task is to write a Python script that safely deletes a specific B2B organization using the Stytch API.

## Requirements
- Create a Python script `/home/user/project/delete_org.py`.
- The script must read the organization ID from `/logs/org_id.txt`.
- Use the `stytch` Python SDK to delete this organization.
- Write the deleted organization ID to `/home/user/project/output.log` after successful deletion.
- The script must use the environment variables `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` for authentication.

## Implementation Guide
1. Initialize a Python project in `/home/user/project`.
2. Install the `stytch` SDK.
3. Write `delete_org.py` to perform the deletion.
4. Run the script and verify the output log.

## Constraints
- Project path: `/home/user/project`
- Log file: `/home/user/project/output.log`
- Ensure the script runs successfully with `python delete_org.py`.

## Integrations
- Stytch