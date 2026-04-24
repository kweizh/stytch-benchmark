import os
import requests
from requests.auth import HTTPBasicAuth
import pytest

PROJECT_DIR = "/home/user/project"
TRIAL_ID_FILE = "/logs/trial_id"

def get_trial_id():
    if not os.path.exists(TRIAL_ID_FILE):
        return "test-trial-123"
    with open(TRIAL_ID_FILE, "r") as f:
        return f.read().strip()

def test_configure_oidc_script_exists():
    script_path = os.path.join(PROJECT_DIR, "configure_oidc.py")
    assert os.path.isfile(script_path), f"Expected script not found at {script_path}"

def test_organization_and_oidc_connection_created():
    trial_id = get_trial_id()
    org_slug = f"test-org-{trial_id}"

    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")

    assert project_id and secret, "Stytch B2B credentials are not set in environment variables."

    # 1. Search for the organization
    search_response = requests.post(
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

    assert search_response.status_code == 200, f"Stytch API organization search failed: {search_response.text}"

    data = search_response.json()
    organizations = data.get("organizations", [])

    assert len(organizations) > 0, f"Expected to find organization with slug '{org_slug}'"
    organization_id = organizations[0]["organization_id"]

    # 2. Get SSO connections for the organization
    sso_response = requests.get(
        f"https://test.stytch.com/v1/b2b/sso/{organization_id}",
        auth=HTTPBasicAuth(project_id, secret)
    )

    assert sso_response.status_code == 200, f"Stytch API get SSO connections failed: {sso_response.text}"

    sso_data = sso_response.json()
    oidc_connections = sso_data.get("oidc_connections", [])

    assert len(oidc_connections) > 0, f"Expected to find an OIDC connection for organization '{org_slug}'"
    
    # 3. Verify the OIDC connection configuration
    connection = oidc_connections[0]
    assert connection.get("issuer") == "https://mock-idp.com", f"Expected OIDC issuer to be 'https://mock-idp.com', got '{connection.get('issuer')}'"
    assert connection.get("client_id") == "mock-client-id", f"Expected OIDC client_id to be 'mock-client-id', got '{connection.get('client_id')}'"