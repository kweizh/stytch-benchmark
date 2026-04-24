import os
import requests
from requests.auth import HTTPBasicAuth
import pytest
import subprocess

TRIAL_ID_FILE = "/logs/trial_id"
PROJECT_DIR = "/home/user/workspace"
SCRIPT_FILE = os.path.join(PROJECT_DIR, "setup_saml.py")

def get_trial_id():
    with open(TRIAL_ID_FILE, "r") as f:
        return f.read().strip()

@pytest.fixture(scope="module", autouse=True)
def setup_and_run_script():
    """Run the user script before running verifications."""
    assert os.path.isfile(SCRIPT_FILE), f"The script {SCRIPT_FILE} does not exist."
    
    result = subprocess.run(
        ["python3", "setup_saml.py"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"The script failed to execute. stderr: {result.stderr}"
    yield

def test_organization_is_created():
    trial_id = get_trial_id()
    org_slug = f"saml-org-{trial_id}"
    
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
    
    assert response.status_code == 200, f"Stytch API request to search organization failed: {response.text}"
    
    data = response.json()
    organizations = data.get("organizations", [])
    
    assert len(organizations) > 0, f"Expected to find organization with slug '{org_slug}'"
    assert organizations[0]["organization_slug"] == org_slug, "Organization slug mismatch"

def test_saml_connection_is_configured():
    trial_id = get_trial_id()
    org_slug = f"saml-org-{trial_id}"
    
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    # First, get the organization ID
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
    
    org_id = organizations[0]["organization_id"]
    
    # Now get the SSO connections for this organization
    sso_response = requests.get(
        f"https://test.stytch.com/v1/b2b/sso/{org_id}",
        auth=HTTPBasicAuth(project_id, secret)
    )
    
    assert sso_response.status_code == 200, f"Failed to get SSO connections: {sso_response.text}"
    sso_data = sso_response.json()
    
    saml_connections = sso_data.get("saml_connections", [])
    assert len(saml_connections) > 0, f"Expected to find at least one SAML connection for organization {org_id}"
    
    # Verify the SAML connection configuration
    configured_connection = None
    for conn in saml_connections:
        if conn.get("idp_sso_url") == "https://idp.example.com/sso":
            configured_connection = conn
            break
            
    assert configured_connection is not None, "No SAML connection found with idp_sso_url 'https://idp.example.com/sso'"
    assert configured_connection.get("idp_entity_id") == "https://idp.example.com/entity", \
        f"Expected idp_entity_id to be 'https://idp.example.com/entity', got {configured_connection.get('idp_entity_id')}"