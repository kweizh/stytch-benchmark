#!/usr/bin/env python3
"""
Configure Stytch B2B OIDC Connection:
  1. Read trial_id from /logs/artifacts/trial_id
  2. Create a new B2B Organization
  3. Create an OIDC SSO connection
  4. Update the OIDC connection with full configuration
"""

import os
import stytch

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
TRIAL_ID_FILE = "/logs/artifacts/trial_id"

PROJECT_ID = os.environ["STYTCH_B2B_PROJECT_ID"]
SECRET     = os.environ["STYTCH_B2B_SECRET"]

# ---------------------------------------------------------------------------
# Read trial_id
# ---------------------------------------------------------------------------
with open(TRIAL_ID_FILE) as f:
    trial_id = f.read().strip()

org_name = f"test-org-{trial_id}"
org_slug = f"test-org-{trial_id}"

print(f"trial_id : {trial_id}")
print(f"org_name : {org_name}")
print(f"org_slug : {org_slug}")

# ---------------------------------------------------------------------------
# Stytch B2B client
# ---------------------------------------------------------------------------
client = stytch.B2BClient(project_id=PROJECT_ID, secret=SECRET)

# ---------------------------------------------------------------------------
# Step 1: Create organization
# ---------------------------------------------------------------------------
print("\n--- Creating organization ---")
org_resp = client.organizations.create(
    organization_name=org_name,
    organization_slug=org_slug,
)
print(f"HTTP status  : {org_resp.status_code}")
org_id = org_resp.organization.organization_id
print(f"organization_id : {org_id}")

# ---------------------------------------------------------------------------
# Step 2: Create OIDC SSO connection
# ---------------------------------------------------------------------------
print("\n--- Creating OIDC SSO connection ---")
create_resp = client.sso.oidc.create_connection(
    organization_id=org_id,
    display_name="My OIDC Connection",
)
print(f"HTTP status : {create_resp.status_code}")
connection_id = create_resp.connection.connection_id
print(f"connection_id : {connection_id}")

# ---------------------------------------------------------------------------
# Step 3: Update OIDC connection with full configuration
# ---------------------------------------------------------------------------
print("\n--- Updating OIDC SSO connection ---")
update_resp = client.sso.oidc.update_connection(
    organization_id=org_id,
    connection_id=connection_id,
    display_name="My OIDC Connection",
    client_id="mock-client-id",
    client_secret="mock-client-secret",
    issuer="https://mock-idp.com",
    authorization_url="https://mock-idp.com/auth",
    token_url="https://mock-idp.com/token",
    userinfo_url="https://mock-idp.com/userinfo",
    jwks_url="https://mock-idp.com/jwks",
)
print(f"HTTP status : {update_resp.status_code}")
conn = update_resp.connection
print(f"connection_id   : {conn.connection_id}")
print(f"display_name    : {conn.display_name}")
print(f"status          : {conn.status}")
print(f"issuer          : {conn.issuer}")
print(f"client_id       : {conn.client_id}")
print(f"authorization_url: {conn.authorization_url}")
print(f"token_url       : {conn.token_url}")
print(f"userinfo_url    : {conn.userinfo_url}")
print(f"jwks_url        : {conn.jwks_url}")

print("\nDone.")
