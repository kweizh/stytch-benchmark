# B2B SCIM Endpoint Setup

## Files

| File | Description |
|------|-------------|
| `setup_scim.js` | Main provisioning script |
| `package.json` | Node.js project manifest (includes `stytch` dependency) |

## Setup

```bash
cd /home/user/app
npm install        # installs stytch SDK (already done)
```

## Usage

Export your **B2B** project credentials, then run the script:

```bash
export STYTCH_PROJECT_ID="project-live-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export STYTCH_SECRET="secret-live-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

node setup_scim.js
```

## What the script does

1. **Creates a B2B Organization** named `"Acme SCIM Org"` with a unique slug
   (`acme-scim-org-<timestamp>`).
2. **Creates a SCIM connection** on that organization with:
   - `display_name`: `"Acme SCIM Connection"`
   - `identity_provider`: `"okta"`
3. **Writes `/home/user/app/scim_output.json`** containing:

```json
{
  "organization_id": "<org-id>",
  "connection_id": "<connection-id>",
  "base_url": "<scim-base-url>",
  "bearer_token": "<full-bearer-token>"
}
```

> ⚠️  The `bearer_token` is only returned **once** at connection creation time.
> Store it securely — it cannot be retrieved again (only rotated).

## Notes

- `STYTCH_PROJECT_ID` / `STYTCH_SECRET` are never hard-coded; they are read from
  environment variables at runtime.
- A **B2B** Stytch project is required. Consumer project credentials will return
  an `invalid_b2b_endpoint` error.
