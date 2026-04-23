# B2B SCIM Endpoint Setup

## Files
| File | Description |
|------|-------------|
| `setup_scim.js` | Main provisioning script |
| `package.json`  | Node.js project manifest (stytch v14) |

## Prerequisites
- Node.js ≥ 16
- A Stytch **B2B** project (not a Consumer project)

## Setup
```bash
cd /home/user/app
npm install          # installs stytch@14
```

## Usage
```bash
export STYTCH_PROJECT_ID="project-live-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
export STYTCH_SECRET="secret-live-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

node setup_scim.js
```

## What the script does
1. Creates a new B2B Organisation named **"Acme SCIM Org"** with a unique slug  
   (`acme-scim-org-<unix-timestamp-ms>`).
2. Creates a SCIM connection named **"Acme SCIM Connection"** using **Okta** as the  
   identity provider.
3. Writes `/home/user/app/scim_output.json` with:
   ```json
   {
     "organization_id": "org-live-…",
     "connection_id":   "scim-connection-…",
     "base_url":        "https://scim.stytch.com/v1/…",
     "bearer_token":    "…"
   }
   ```

## Error handling
- Exits with code `1` and a clear message if either env var is missing.
- Exits with code `1` and the API error message if any Stytch call fails.
