import os
import requests
from requests.auth import HTTPBasicAuth
import pytest

ORG_ID_FILE = "/logs/org_id.txt"
OUTPUT_LOG = "/home/user/project/output.log"

def test_output_log_exists_and_contains_org_id():
    assert os.path.isfile(ORG_ID_FILE), f"Expected {ORG_ID_FILE} to exist."
    with open(ORG_ID_FILE, "r") as f:
        org_id = f.read().strip()
        
    assert os.path.isfile(OUTPUT_LOG), f"Expected script to create {OUTPUT_LOG}."
    with open(OUTPUT_LOG, "r") as f:
        log_content = f.read()
        
    assert org_id in log_content, f"Expected organization ID {org_id} to be in {OUTPUT_LOG}."

def test_organization_is_deleted_via_amika_api():
    """Use the amika API (simulated via requests) to validate the organization is deleted."""
    assert os.path.isfile(ORG_ID_FILE), f"Expected {ORG_ID_FILE} to exist."
    with open(ORG_ID_FILE, "r") as f:
        org_id = f.read().strip()
        
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    assert project_id and secret, "Stytch B2B credentials are not set."
    
    # Verify the organization is deleted by trying to fetch it
    response = requests.get(
        f"https://test.stytch.com/v1/b2b/organizations/{org_id}",
        auth=HTTPBasicAuth(project_id, secret)
    )
    
    # A deleted organization should return a 404 Not Found error
    assert response.status_code == 404, f"Expected 404 Not Found for deleted organization {org_id}, but got {response.status_code}: {response.text}"
