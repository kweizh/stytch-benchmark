# B2B SCIM Endpoint Setup

## Background
You are building an automated user provisioning pipeline for a B2B organization using Stytch's SCIM API. You need to create a Node.js script that programmatically provisions a new organization and sets up a SCIM connection for it.

## Requirements
- Initialize a Node.js project in `/home/user/app` and install the `stytch` SDK.
- Write a script `setup_scim.js` that uses the Stytch B2B Client.
- The script must:
  1. Create a new B2B Organization with `organization_name` "Acme SCIM Org" and a unique slug (e.g., `acme-scim-org-<timestamp>`).
  2. Create a SCIM connection for this organization with `display_name` "Acme SCIM Connection" and `identity_provider` "okta".
  3. Write a JSON file to `/home/user/app/scim_output.json` containing:
     - `organization_id`
     - `connection_id`
     - `base_url`
     - `bearer_token` (from the created SCIM connection)

## Implementation Guide
1. Run `npm init -y` and `npm install stytch` in `/home/user/app`.
2. Create `/home/user/app/setup_scim.js`.
3. Use the SDK to instantiate `new stytch.B2BClient({ project_id: process.env.STYTCH_PROJECT_ID, secret: process.env.STYTCH_SECRET })`.
4. Call `client.organizations.create(...)` and then `client.scim.connection.create(...)`.
5. Write the extracted properties to `scim_output.json`.

## Constraints
- **Project path**: `/home/user/app`
- Do not hardcode the `STYTCH_PROJECT_ID` or `STYTCH_SECRET`; use environment variables.
