import os
import requests
from requests.auth import HTTPBasicAuth

ORG_ID_FILE = "/logs/org_id.txt"
TRIAL_ID_FILE = "/logs/artifacts/trial_id"

def get_trial_id():
    if os.path.exists(TRIAL_ID_FILE):
        with open(TRIAL_ID_FILE, "r") as f:
            return f.read().strip()
    return "default-trial"

def test_prepare_and_verify_organization():
    trial_id = get_trial_id()
    org_slug = f"test-org-delete-{trial_id}"

    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")

    assert project_id and secret, "Stytch B2B credentials are not set."

    # Create the organization
    response = requests.post(
        "https://test.stytch.com/v1/b2b/organizations",
        json={
            "organization_name": org_slug,
            "organization_slug": org_slug
        },
        auth=HTTPBasicAuth(project_id, secret)
    )

    assert response.status_code in (200, 201), f"Failed to create organization: {response.text}"

    data = response.json()
    org_id = data["organization"]["organization_id"]

    # Write the org_id to a file for the agent to use
    os.makedirs("/logs", exist_ok=True)
    with open(ORG_ID_FILE, "w") as f:
        f.write(org_id)

    assert os.path.isfile(ORG_ID_FILE), f"Expected {ORG_ID_FILE} to exist."
