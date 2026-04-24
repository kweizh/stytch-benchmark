import os
import subprocess
import time
import socket
import pytest
import requests
from requests.auth import HTTPBasicAuth

PROJECT_DIR = "/home/user/app"
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
    trial_id = get_trial_id()
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    assert project_id and secret, "Stytch B2B credentials are missing."

    auth = HTTPBasicAuth(project_id, secret)
    base_url = "https://test.stytch.com/v1/b2b"

    org_slug = f"test-jwt-org-{trial_id}"
    resp = requests.post(f"{base_url}/organizations", json={
        "organization_name": org_slug,
        "organization_slug": org_slug,
        "auth_methods": "all_allowed"
    }, auth=auth)
    assert resp.status_code in [200, 201], f"Failed to create org: {resp.text}"
    org_id = resp.json()["organization"]["organization_id"]

    email = f"member-{trial_id}@example.com"
    resp = requests.post(f"{base_url}/organizations/{org_id}/members", json={
        "email_address": email
    }, auth=auth)
    assert resp.status_code in [200, 201], f"Failed to create member: {resp.text}"
    member_id = resp.json()["member_id"]

    resp = requests.post(f"{base_url}/passwords", json={
        "organization_id": org_id,
        "email_address": email,
        "password": "Password123!"
    }, auth=auth)
    assert resp.status_code in [200, 201], f"Failed to set password: {resp.text}"

    resp = requests.post(f"{base_url}/passwords/authenticate", json={
        "organization_id": org_id,
        "email_address": email,
        "password": "Password123!"
    }, auth=auth)
    assert resp.status_code == 200, f"Failed to authenticate: {resp.text}"
    
    session_jwt = resp.json()["session_jwt"]
    
    return {
        "session_jwt": session_jwt,
        "member_id": member_id,
        "organization_id": org_id
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
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_valid_jwt(stytch_session, start_app):
    url = "http://localhost:3000/validate"
    payload = {"session_jwt": stytch_session["session_jwt"]}
    
    resp = requests.post(url, json=payload)
    assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}: {resp.text}"
    
    data = resp.json()
    assert data.get("member_id") == stytch_session["member_id"], \
        f"Expected member_id {stytch_session['member_id']}, got {data.get('member_id')}"

def test_invalid_jwt(start_app):
    url = "http://localhost:3000/validate"
    payload = {"session_jwt": "invalid.jwt.token"}
    
    resp = requests.post(url, json=payload)
    assert resp.status_code == 401, f"Expected 401 Unauthorized for invalid JWT, got {resp.status_code}"

def test_uses_local_validation():
    script_path = os.path.join(PROJECT_DIR, "index.js")
    if not os.path.exists(script_path):
        js_files = [f for f in os.listdir(PROJECT_DIR) if f.endswith(".js")]
        assert len(js_files) > 0, "No JavaScript files found in the project directory."
        script_path = os.path.join(PROJECT_DIR, js_files[0])
        
    with open(script_path, "r") as f:
        content = f.read()
        
    has_local = "authenticateJwtLocal" in content
    has_custom_jwks = "jwks" in content.lower() or "verify" in content.lower()
    
    assert has_local or has_custom_jwks, \
        "Expected the code to use 'authenticateJwtLocal' or a custom JWKS validation method."
