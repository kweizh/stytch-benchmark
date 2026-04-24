import os
import json
import requests
from requests.auth import HTTPBasicAuth
import pytest

TRIAL_ID_FILE = "/logs/artifacts/trial_id"
PROJECT_DIR = "/home/user/project"
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def get_trial_id():
    if os.path.isfile(TRIAL_ID_FILE):
        with open(TRIAL_ID_FILE, "r") as f:
            return f.read().strip()
    return "test"

def test_organization_is_created():
    trial_id = get_trial_id()
    org_slug = f"acme-corp-{trial_id}"

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
    assert organizations[0]["organization_slug"] == org_slug, "Organization slug mismatch"

def test_member_is_invited():
    trial_id = get_trial_id()
    org_slug = f"acme-corp-{trial_id}"
    email = f"new-member-{trial_id}@example.com"

    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")

    assert project_id and secret, "Stytch B2B credentials are not set in environment variables."

    # Get organization first
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
    assert org_response.status_code == 200, "Failed to get organization"
    org_data = org_response.json()
    assert len(org_data.get("organizations", [])) > 0, f"Organization {org_slug} not found"
    org_id = org_data["organizations"][0]["organization_id"]

    # Use Stytch API to search for the member
    member_response = requests.post(
        "https://test.stytch.com/v1/b2b/organizations/members/search",
        json={
            "organization_ids": [org_id],
            "query": {
                "operator": "AND",
                "operands": [
                    {
                        "filter_name": "member_emails",
                        "filter_value": [email]
                    }
                ]
            }
        },
        auth=HTTPBasicAuth(project_id, secret)
    )

    assert member_response.status_code == 200, f"Stytch API request failed: {member_response.text}"

    member_data = member_response.json()
    members = member_data.get("members", [])

    assert len(members) > 0, f"Expected to find member with email '{email}'"
    
    member = members[0]
    assert member["email_address"] == email, "Member email mismatch"
    assert member["status"] == "invited" or member["status"] == "active" or member["status"] == "pending", f"Member status is {member['status']}, expected invited/pending"

def test_output_file_exists_and_valid():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} not found"
    
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_FILE} is not valid JSON")
            
    assert "organization_id" in data, "organization_id missing in output.json"
    assert "member_id" in data, "member_id missing in output.json"
