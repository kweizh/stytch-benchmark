import os
import requests
from requests.auth import HTTPBasicAuth

TRIAL_ID_FILE = "/logs/artifacts/trial_id"

def get_trial_id():
    if os.path.exists(TRIAL_ID_FILE):
        with open(TRIAL_ID_FILE, "r") as f:
            return f.read().strip()
    return "default-trial"

def test_organization_auth_methods_updated():
    trial_id = get_trial_id()
    org_slug = f"test-org-{trial_id}"

    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")

    assert project_id and secret, "Stytch B2B credentials are not set in environment variables."

    # Use Stytch API to search for the organization
    response = requests.post(
        "https://test.stytch.com/v1/b2b/organizations/search",
        json={
            "query": {
                "operator": "AND",
                "operands": [
                    {
                        "filter_name": "organization_slug",
                        "filter_value": org_slug
                    }
                ]
            }
        },
        auth=HTTPBasicAuth(project_id, secret)
    )

    assert response.status_code == 200, f"Stytch API request failed: {response.text}"

    data = response.json()
    organizations = data.get("organizations", [])

    assert len(organizations) > 0, f"Expected to find organization with slug '{org_slug}'"

    org = organizations[0]
    assert org["organization_slug"] == org_slug, "Organization slug mismatch"

    # Verify auth methods
    assert org.get("auth_methods") == "RESTRICTED", f"Expected auth_methods to be 'RESTRICTED', got {org.get('auth_methods')}"

    allowed_auth_methods = org.get("allowed_auth_methods", [])
    expected_methods = ["sso", "magic_link"]

    # Check that both lists contain exactly the same elements
    assert set(allowed_auth_methods) == set(expected_methods), f"Expected allowed_auth_methods to be {expected_methods}, got {allowed_auth_methods}"
