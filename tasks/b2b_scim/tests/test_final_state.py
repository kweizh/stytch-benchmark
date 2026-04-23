import os
import json
import pytest
import urllib.request
import base64

APP_DIR = "/home/user/app"
OUTPUT_FILE = os.path.join(APP_DIR, "scim_output.json")

def get_stytch_credentials():
    project_id = os.environ.get("STYTCH_PROJECT_ID")
    secret = os.environ.get("STYTCH_SECRET")
    assert project_id and secret, "STYTCH_PROJECT_ID and STYTCH_SECRET must be set in the environment"
    return project_id, secret

def make_stytch_request(endpoint, method="GET"):
    project_id, secret = get_stytch_credentials()
    
    # Determine base URL based on project_id prefix
    base_url = "https://test.stytch.com" if project_id.startswith("project-test-") else "https://api.stytch.com"
    url = f"{base_url}{endpoint}"
    
    req = urllib.request.Request(url, method=method)
    
    # Basic Auth
    auth_string = f"{project_id}:{secret}"
    auth_bytes = auth_string.encode("utf-8")
    b64_auth = base64.b64encode(auth_bytes).decode("utf-8")
    req.add_header("Authorization", f"Basic {b64_auth}")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        pytest.fail(f"Stytch API request failed: {e.code} {e.reason} - {error_body}")

def test_scim_output_exists_and_valid():
    assert os.path.isfile(OUTPUT_FILE), f"Expected {OUTPUT_FILE} to exist."
    
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Failed to parse {OUTPUT_FILE} as JSON")
            
    assert "organization_id" in data, "Missing organization_id in output"
    assert "connection_id" in data, "Missing connection_id in output"
    assert "base_url" in data, "Missing base_url in output"
    assert "bearer_token" in data, "Missing bearer_token in output"

def test_organization_created():
    with open(OUTPUT_FILE, "r") as f:
        data = json.load(f)
    org_id = data["organization_id"]
    
    response = make_stytch_request(f"/v1/b2b/organizations/{org_id}")
    org = response.get("organization", {})
    
    assert org.get("organization_name") == "Acme SCIM Org", \
        f"Expected organization name 'Acme SCIM Org', got '{org.get('organization_name')}'"

def test_scim_connection_created():
    with open(OUTPUT_FILE, "r") as f:
        data = json.load(f)
    org_id = data["organization_id"]
    conn_id = data["connection_id"]
    
    response = make_stytch_request(f"/v1/b2b/scim/{org_id}/connection")
    conn = response.get("connection", {})
    
    assert conn.get("connection_id") == conn_id, \
        f"Expected connection_id {conn_id}, got {conn.get('connection_id')}"
    assert conn.get("display_name") == "Acme SCIM Connection", \
        f"Expected display name 'Acme SCIM Connection', got '{conn.get('display_name')}'"
    assert conn.get("identity_provider") == "okta", \
        f"Expected identity_provider 'okta', got '{conn.get('identity_provider')}'"
