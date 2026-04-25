import os
import sys
from stytch import B2BClient

ORG_ID_PATH = "/logs/org_id.txt"
OUTPUT_LOG_PATH = "/home/user/project/output.log"


def read_org_id(path: str) -> str:
    with open(path, "r", encoding="utf-8") as handle:
        org_id = handle.read().strip()
    if not org_id:
        raise ValueError(f"Organization ID file {path} is empty.")
    return org_id


def main() -> int:
    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        raise EnvironmentError(
            "STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET must be set in the environment."
        )

    org_id = read_org_id(ORG_ID_PATH)

    client = B2BClient(project_id=project_id, secret=secret)

    try:
        client.organizations.delete(organization_id=org_id)
    except Exception as exc:  # pragma: no cover - SDK raises typed errors
        print(f"Failed to delete organization {org_id}: {exc}", file=sys.stderr)
        return 1

    with open(OUTPUT_LOG_PATH, "w", encoding="utf-8") as handle:
        handle.write(f"{org_id}\n")

    print(f"Deleted organization {org_id} and wrote to {OUTPUT_LOG_PATH}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
