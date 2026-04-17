import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.parse
import base64
import hashlib
import re

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

def stytch_api_call(path, project_id, secret, data=None):
    url = f"https://test.stytch.com{path}"
    auth = base64.b64encode(f"{project_id}:{secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    }
    
    if data is not None:
        req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=headers)
    else:
        req = urllib.request.Request(url, headers=headers)
    
    try:
        res = urllib.request.urlopen(req)
        return json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Stytch API Error: {e.read().decode()}")
        raise e

@pytest.fixture(scope="module")
def stytch_env():
    project_id = os.environ.get("STYTCH_PROJECT_ID")
    secret = os.environ.get("STYTCH_SECRET")
    assert project_id and secret, "Stytch API keys not found in environment."
    
    org_res = stytch_api_call("/v1/b2b/organizations", project_id, secret, {
        "organization_name": "Test Org",
        "organization_slug": f"test-org-{int(time.time())}"
    })
    org_id = org_res["organization"]["organization_id"]
    
    member_res = stytch_api_call(f"/v1/b2b/organizations/{org_id}/members", project_id, secret, {
        "email_address": f"test+{int(time.time())}@example.com"
    })
    member_id = member_res["member"]["member_id"]
    
    client_res = stytch_api_call("/v1/connected_apps/clients", project_id, secret, {
        "client_name": "Test App",
        "client_type": "third_party_public",
        "redirect_urls": ["https://example.com/callback"]
    })
    client_id = client_res["connected_app"]["client_id"]
    
    return {
        "org_id": org_id,
        "member_id": member_id,
        "client_id": client_id,
        "project_id": project_id,
        "secret": secret
    }

@pytest.fixture(scope="module")
def start_app(stytch_env):
    env = os.environ.copy()
    env["TEST_ORG_ID"] = stytch_env["org_id"]
    env["TEST_MEMBER_ID"] = stytch_env["member_id"]
    
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("Express app failed to start and listen on port 3000.")
    
    yield stytch_env
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def test_authorize_endpoint_filters_scopes(start_app):
    stytch_env = start_app
    client_id = stytch_env["client_id"]
    
    # Generate PKCE
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode().rstrip("=")
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest()).decode().rstrip("=")
    
    params = urllib.parse.urlencode({
        "client_id": client_id,
        "scope": "read:profile write:profile",
        "redirect_uri": "https://example.com/callback",
        "state": "xyz",
        "code_challenge": code_challenge,
        "code_challenge_method": "S256"
    })
    url = f"http://localhost:3000/authorize?{params}"
    
    opener = urllib.request.build_opener(NoRedirectHandler())
    req = urllib.request.Request(url)
    try:
        res = opener.open(req)
        final_url = res.geturl()
        status = res.getcode()
        headers = res.headers
    except urllib.error.HTTPError as e:
        final_url = e.geturl()
        status = e.getcode()
        headers = e.headers
        
    assert status in [301, 302, 303, 307, 308], f"Expected redirect status code, got {status}"
    location = headers.get("Location")
    assert location and "example.com/callback" in location, f"Expected redirect to callback URI, got Location: {location}"
    
    # Extract code
    match = re.search(r"code=([^&]+)", location)
    assert match, f"Authorization code not found in redirect URI: {location}"
    code = match.group(1)
    
    # Exchange code for token
    token_url = "https://test.stytch.com/v1/oauth2/token"
    token_data = {
        "client_id": client_id,
        "grant_type": "authorization_code",
        "code": code,
        "code_verifier": code_verifier
    }
    
    try:
        req = urllib.request.Request(token_url, data=json.dumps(token_data).encode(), headers={"Content-Type": "application/json"})
        res = urllib.request.urlopen(req)
        token_res = json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        pytest.fail(f"Token exchange failed: {e.read().decode()}")
        
    access_token = token_res.get("access_token")
    assert access_token, "No access token returned in token exchange."
    
    # Decode JWT payload (middle part)
    payload_b64 = access_token.split('.')[1]
    # Add padding if necessary
    payload_b64 += "=" * ((4 - len(payload_b64) % 4) % 4)
    payload = json.loads(base64.urlsafe_b64decode(payload_b64).decode())
    
    scopes = payload.get("scope", "")
    assert "read:profile" in scopes, f"Expected read:profile in scopes, got: {scopes}"
    assert "write:profile" not in scopes, f"Expected write:profile to be filtered out, but got: {scopes}"
