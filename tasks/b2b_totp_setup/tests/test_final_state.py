import os
import json
import requests
from requests.auth import HTTPBasicAuth
import pytest

TRIAL_ID_FILE = "/logs/artifacts/trial_id"
INFO_FILE = "/home/user/stytch_project/totp_info.json"

def get_trial_id():
    if os.path.exists(TRIAL_ID_FILE):
        with open(TRIAL_ID_FILE, "r") as f:
            return f.read().strip()
    return "test-trial"

def test_totp_info_file_exists():
    assert os.path.isfile(INFO_FILE), f"Expected {INFO_FILE} to exist."

def test_totp_registration_active():
    """Verify the TOTP registration is active using the Stytch API."""
    with open(INFO_FILE, "r") as f:
        data = json.load(f)
    
    totp_registration_id = data.get("totp_registration_id")
    assert totp_registration_id, "totp_registration_id not found in totp_info.json"
    
    trial_id = get_trial_id()
    org_slug = f"test-totp-org-{trial_id}"
    
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    assert project_id and secret, "Stytch B2B credentials are not set in environment variables."
    
    # First, search for the organization
    org_response = requests.post(
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
    
    assert org_response.status_code == 200, f"Organization search failed: {org_response.text}"
    orgs = org_response.json().get("organizations", [])
    assert len(orgs) > 0, f"Expected to find organization with slug '{org_slug}'"
    organization_id = orgs[0]["organization_id"]
    
    # Next, search for the member
    member_email = f"member-{trial_id}@example.com"
    member_response = requests.post(
        f"https://test.stytch.com/v1/b2b/organizations/{organization_id}/members/search",
        json={
            "query": {
                "operator": "AND",
                "operands": [
                    {
                        "filter_name": "member_emails",
                        "filter_value": [member_email]
                    }
                ]
            }
        },
        auth=HTTPBasicAuth(project_id, secret)
    )
    
    assert member_response.status_code == 200, f"Member search failed: {member_response.text}"
    members = member_response.json().get("members", [])
    assert len(members) > 0, f"Expected to find member with email '{member_email}'"
    member = members[0]
    
    # Check if the member has an active TOTP registration with the ID
    assert member.get("totp_registration_id") == totp_registration_id, \
        f"Member's active TOTP registration ({member.get('totp_registration_id')}) does not match the one in JSON ({totp_registration_id})."
