#!/usr/bin/env python3
import os
import sys

import stytch


def get_env_var(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def read_trial_id(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return handle.read().strip()
    except FileNotFoundError as exc:
        raise RuntimeError(f"trial_id file not found at {path}") from exc


def extract_org_id(response) -> str:
    org_id = getattr(response, "organization_id", None)
    if org_id:
        return org_id

    org = getattr(response, "organization", None)
    if org:
        org_id = getattr(org, "organization_id", None)
        if org_id:
            return org_id

    raise RuntimeError("Unable to determine organization_id from create response")


def main() -> int:
    project_id = get_env_var("STYTCH_B2B_PROJECT_ID")
    secret = get_env_var("STYTCH_B2B_SECRET")
    trial_id = read_trial_id("/logs/trial_id")

    client = stytch.B2BClient(project_id=project_id, secret=secret)

    organization_name = f"test-org-{trial_id}"
    organization_slug = f"test-org-{trial_id}"

    create_response = client.organizations.create(
        organization_name=organization_name,
        organization_slug=organization_slug,
    )

    organization_id = extract_org_id(create_response)

    client.organizations.update(
        organization_id=organization_id,
        auth_methods="RESTRICTED",
        allowed_auth_methods=["sso", "magic_link"],
    )

    print(
        "Organization created and updated successfully:",
        f"id={organization_id}",
        f"name={organization_name}",
    )
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # pragma: no cover - surface all errors
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)
