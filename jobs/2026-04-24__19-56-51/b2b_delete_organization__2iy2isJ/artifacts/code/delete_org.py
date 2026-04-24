"""
delete_org.py

Reads a B2B organization ID from /logs/org_id.txt and deletes it via the
Stytch B2B API. On success, writes the deleted organization ID to
/home/user/project/output.log.

Required environment variables:
  STYTCH_B2B_PROJECT_ID  – Stytch B2B project ID
  STYTCH_B2B_SECRET      – Stytch B2B secret key
"""

import os
import sys

import stytch

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ORG_ID_FILE = "/logs/org_id.txt"
OUTPUT_LOG = "/home/user/project/output.log"

# ---------------------------------------------------------------------------
# Read credentials from environment
# ---------------------------------------------------------------------------
project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
secret = os.environ.get("STYTCH_B2B_SECRET")

if not project_id or not secret:
    print(
        "ERROR: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET "
        "environment variables must be set.",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Read organization ID from file
# ---------------------------------------------------------------------------
try:
    with open(ORG_ID_FILE, "r") as f:
        organization_id = f.read().strip()
except FileNotFoundError:
    print(f"ERROR: Could not find org ID file at {ORG_ID_FILE}", file=sys.stderr)
    sys.exit(1)

if not organization_id:
    print(f"ERROR: {ORG_ID_FILE} is empty.", file=sys.stderr)
    sys.exit(1)

print(f"Organization ID to delete: {organization_id}")

# ---------------------------------------------------------------------------
# Initialize Stytch B2B client
# ---------------------------------------------------------------------------
client = stytch.B2BClient(project_id=project_id, secret=secret)

# ---------------------------------------------------------------------------
# Delete the organization
# ---------------------------------------------------------------------------
try:
    response = client.organizations.delete(organization_id=organization_id)
    print(f"Delete response status: {response.status_code}")
except Exception as e:
    print(f"ERROR: Failed to delete organization: {e}", file=sys.stderr)
    sys.exit(1)

if response.status_code != 200:
    print(
        f"ERROR: Unexpected status code {response.status_code} from Stytch API.",
        file=sys.stderr,
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Write deleted organization ID to output log
# ---------------------------------------------------------------------------
with open(OUTPUT_LOG, "w") as f:
    f.write(organization_id + "\n")

print(f"Successfully deleted organization: {organization_id}")
print(f"Deleted organization ID written to: {OUTPUT_LOG}")
