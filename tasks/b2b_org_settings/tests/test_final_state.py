import os
import subprocess
import json
import pytest
import urllib.request
import urllib.parse
import base64
import uuid

PROJECT_DIR = "/home/user/app"

def get_stytch_credentials():
    project_id = os.environ.get("STYTCH_PROJECT_ID")
    secret = os.environ.get("STYTCH_SECRET")
    assert project_id, "STYTCH_PROJECT_ID is not set in the environment"
    assert secret, "STYTCH_SECRET is not set in the environment"
    return project_id, secret

def make_stytch_request(method, path, data=None):
    project_id, secret = get_stytch_credentials()
    url = f"https://test.stytch.com/v1{path}"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic " + base64.b64encode(f"{project_id}:{secret}".encode()).decode()
    }
    
    req = urllib.request.Request(url, headers=headers, method=method)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        pytest.fail(f"Stytch API error: {e.code} {error_body}")

@pytest.fixture(scope="module")
def setup_test_org():
    # Create a test organization
    unique_id = str(uuid.uuid4())[:8]
    org_name = f"test-org-settings-{unique_id}"
    org_slug = f"test-org-settings-slug-{unique_id}"
    
    data = {
        "organization_name": org_name,
        "organization_slug": org_slug,
        "email_allowed_domains": ["example.com"]
    }
    
    result = make_stytch_request("POST", "/b2b/organizations", data)
    org_id = result.get("organization", {}).get("organization_id")
    assert org_id, "Failed to create test organization"
    
    yield org_id
    
    # Clean up
    try:
        make_stytch_request("DELETE", f"/b2b/organizations/{org_id}")
    except:
        pass

def test_script_exists():
    script_path = os.path.join(PROJECT_DIR, "update_org.js")
    assert os.path.isfile(script_path), f"update_org.js not found at {script_path}"

def test_update_org_settings(setup_test_org):
    org_id = setup_test_org
    
    # Run the user's script
    script_path = os.path.join(PROJECT_DIR, "update_org.js")
    result = subprocess.run(
        ["node", script_path, org_id],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    
    # Verify the changes using Stytch API
    org_data = make_stytch_request("GET", f"/b2b/organizations/{org_id}")
    org = org_data.get("organization", {})
    
    assert org.get("auth_methods", "").upper() == "RESTRICTED", f"Expected auth_methods to be 'RESTRICTED', got {org.get('auth_methods')}"
    
    allowed_auth_methods = org.get("allowed_auth_methods", [])
    assert "sso" in allowed_auth_methods, f"Expected 'sso' in allowed_auth_methods, got {allowed_auth_methods}"
    assert "magic_link" in allowed_auth_methods, f"Expected 'magic_link' in allowed_auth_methods, got {allowed_auth_methods}"
    
    assert org.get("email_jit_provisioning", "").upper() == "RESTRICTED", f"Expected email_jit_provisioning to be 'RESTRICTED', got {org.get('email_jit_provisioning')}"
