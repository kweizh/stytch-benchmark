"""
Delete a Stytch B2B Organization.

Reads the organization ID from /logs/org_id.txt, deletes it via the
Stytch Python SDK, and writes the deleted organization ID to
/home/user/project/output.log.

Authentication uses the environment variables:
  STYTCH_B2B_PROJECT_ID
  STYTCH_B2B_SECRET
"""

import os
import sys

from stytch import B2BClient

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
ORG_ID_FILE = "/logs/org_id.txt"
OUTPUT_LOG = "/home/user/project/output.log"


def main() -> None:
    # --- Read credentials from environment -----------------------------------
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        print(
            "ERROR: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET must be set.",
            file=sys.stderr,
        )
        sys.exit(1)

    # --- Read the organization ID from file ----------------------------------
    try:
        with open(ORG_ID_FILE, "r") as fh:
            org_id = fh.read().strip()
    except FileNotFoundError:
        print(f"ERROR: org_id file not found at {ORG_ID_FILE}", file=sys.stderr)
        sys.exit(1)

    if not org_id:
        print("ERROR: org_id file is empty.", file=sys.stderr)
        sys.exit(1)

    print(f"Organization ID to delete: {org_id}")

    # --- Initialize the Stytch B2B client ------------------------------------
    # environment is inferred from the project_id prefix ("project-test-" → test)
    env = "test" if project_id.startswith("project-test-") else "live"
    client = B2BClient(project_id=project_id, secret=secret, environment=env)

    # --- Delete the organization ---------------------------------------------
    print(f"Deleting organization '{org_id}' ...")
    response = client.organizations.delete(organization_id=org_id)

    # The SDK raises on non-2xx responses, so reaching here means success.
    print(f"Successfully deleted organization: {org_id}")
    print(f"Response status code: {response.status_code}")

    # --- Write the deleted org ID to the output log --------------------------
    os.makedirs(os.path.dirname(OUTPUT_LOG), exist_ok=True)
    with open(OUTPUT_LOG, "w") as fh:
        fh.write(f"{org_id}\n")

    print(f"Deleted organization ID written to {OUTPUT_LOG}")


if __name__ == "__main__":
    main()
