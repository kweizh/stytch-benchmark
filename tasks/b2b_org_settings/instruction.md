# Update B2B Organization Settings

## Background
You need to update the settings for a Stytch B2B organization using the Stytch Node.js SDK.

## Requirements
- You have a Node.js project at `/home/user/app` with `stytch` installed.
- Create a Node.js script `update_org.js` in `/home/user/app`.
- The script should use the `stytch` SDK to update a B2B organization.
- It should read `STYTCH_PROJECT_ID` and `STYTCH_SECRET` from environment variables.
- It should take the `organization_id` as the first command-line argument.
- The script must update the organization's `auth_methods` to `RESTRICTED` and `allowed_auth_methods` to `['sso', 'magic_link']`.
- It must also update `email_jit_provisioning` to `RESTRICTED`.

## Implementation Guide
1. Go to `/home/user/app`.
2. Create `update_org.js`.
3. Instantiate `stytch.B2BClient`.
4. Call `client.organizations.update({ organization_id, auth_methods: 'RESTRICTED', allowed_auth_methods: ['sso', 'magic_link'], email_jit_provisioning: 'RESTRICTED' })`.

## Constraints
- Project path: /home/user/app
- The script should log "Organization updated successfully" upon success.
