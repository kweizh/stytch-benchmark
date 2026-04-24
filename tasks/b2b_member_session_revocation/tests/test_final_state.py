import os
import subprocess
import time
import socket
import pytest
import requests
from requests.auth import HTTPBasicAuth

PROJECT_DIR = "/home/user/project"
TRIAL_ID_FILE = "/logs/trial_id"

def get_trial_id():
    if os.path.exists(TRIAL_ID_FILE):
        with open(TRIAL_ID_FILE, "r") as f:
            return f.read().strip()
    return "test-trial-id"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
    return False

@pytest.fixture(scope="module")
def stytch_session():
    """Create a test organization, member, and generate a valid session_token."""
    trial_id = get_trial_id()
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    assert project_id and secret, "Stytch B2B credentials are missing."

    auth = HTTPBasicAuth(project_id, secret)
    base_url = "https://test.stytch.com/v1/b2b"

    # Create Organization
    org_slug = f"revoke-test-org-{trial_id}"
    resp = requests.post(f"{base_url}/organizations", json={
        "organization_name": org_slug,
        "organization_slug": org_slug
    }, auth=auth)
    
    if resp.status_code == 400 and "organization_slug_already_exists" in resp.text:
        search_resp = requests.post(f"{base_url}/organizations/search", json={
            "query": {"operator": "AND", "operands": [{"filter_name": "organization_slug", "filter_value": org_slug}]}
        }, auth=auth)
        org_id = search_resp.json()["organizations"][0]["organization_id"]
    else:
        assert resp.status_code in [200, 201], f"Failed to create org: {resp.text}"
        org_id = resp.json()["organization"]["organization_id"]

    # Create Member
    email = f"revoke-member-{trial_id}@example.com"
    resp = requests.post(f"{base_url}/organizations/{org_id}/members", json={
        "email_address": email
    }, auth=auth)
    
    if resp.status_code == 400 and "member_already_exists" in resp.text:
        search_member_resp = requests.post(f"{base_url}/organizations/{org_id}/members/search", json={
            "query": {"operator": "AND", "operands": [{"filter_name": "member_emails", "filter_value": [email]}]}
        }, auth=auth)
        member_id = search_member_resp.json()["members"][0]["member_id"]
    else:
        assert resp.status_code in [200, 201], f"Failed to create member: {resp.text}"
        member_id = resp.json()["member"]["member_id"]

    # Set password
    resp = requests.post(f"{base_url}/passwords", json={
        "organization_id": org_id,
        "email_address": email,
        "password": "Password123!"
    }, auth=auth)
    assert resp.status_code in [200, 201] or "password_already_exists" in resp.text or resp.status_code == 400, f"Failed to set password: {resp.text}"

    # Authenticate to get session_token
    resp = requests.post(f"{base_url}/passwords/authenticate", json={
        "organization_id": org_id,
        "email_address": email,
        "password": "Password123!"
    }, auth=auth)
    assert resp.status_code == 200, f"Failed to authenticate: {resp.text}"
    
    session_token = resp.json()["session_token"]
    
    return {
        "session_token": session_token,
        "member_id": member_id,
        "organization_id": org_id,
        "auth": auth,
        "base_url": base_url
    }

@pytest.fixture(scope="module")
def start_app():
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(3000):
        # Try node index.js if npm start fails
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        
        process = subprocess.Popen(
            ["node", "index.js"],
            cwd=PROJECT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        if not wait_for_port(3000):
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_revoke_session(stytch_session, start_app):
    """Use the amika API (requests) to call the local endpoint and verify session revocation."""
    url = "http://localhost:3000/revoke"
    payload = {"session_token": stytch_session["session_token"]}
    
    # 1. Call the user's API to revoke the session
    resp = requests.post(url, json=payload)
    assert resp.status_code == 200, f"Expected 200 OK from /revoke, got {resp.status_code}: {resp.text}"
    
    # 2. Verify that the session is actually revoked on Stytch
    verify_url = f"{stytch_session['base_url']}/sessions/authenticate"
    verify_payload = {"session_token": stytch_session["session_token"]}
    
    verify_resp = requests.post(verify_url, json=verify_payload, auth=stytch_session["auth"])
    assert verify_resp.status_code == 404, f"Expected 404 for revoked session, got {verify_resp.status_code}: {verify_resp.text}"
    
    # Check the error_type to ensure it's a session not found error
    error_data = verify_resp.json()
    assert error_data.get("error_type") == "session_not_found", f"Expected session_not_found error, got {error_data.get('error_type')}"
