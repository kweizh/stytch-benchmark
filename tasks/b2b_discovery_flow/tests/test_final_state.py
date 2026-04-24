import os
import subprocess
import time
import socket
import pytest
import urllib.request
import urllib.error
import json

PROJECT_DIR = "/home/user/project"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(5)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )
    
    # Wait for the app to be ready
    if not wait_for_port(3000):
        # Kill the process group before failing
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on required port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def make_post_request(path, payload):
    url = f"http://localhost:3000{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return 500, {"error": str(e)}

def test_api_discovery_send(start_app):
    status, response = make_post_request("/api/discovery/send", {"email": "sandbox@stytch.com"})
    assert status == 200, f"Expected 200 OK for /api/discovery/send, got {status} with response {response}"
    assert "status_code" in response, "Expected 'status_code' in response from Stytch API"
    assert response["status_code"] == 200, "Expected Stytch status_code to be 200"

def test_api_discovery_authenticate(start_app):
    status, response = make_post_request("/api/discovery/authenticate", {"discovery_magic_links_token": "invalid_token_123"})
    # Stytch should return a 400 or 401 for an invalid token, and the API should proxy it
    assert status >= 400, f"Expected error status for invalid token, got {status}"
    assert "error_type" in response or "status_code" in response, f"Expected Stytch error response, got {response}"

def test_api_discovery_exchange(start_app):
    status, response = make_post_request("/api/discovery/exchange", {
        "intermediate_session_token": "invalid_session_123",
        "organization_id": "organization-test-00000000-0000-0000-0000-000000000000"
    })
    assert status >= 400, f"Expected error status for invalid session, got {status}"
    assert "error_type" in response or "status_code" in response, f"Expected Stytch error response, got {response}"

def test_api_discovery_create(start_app):
    status, response = make_post_request("/api/discovery/create", {
        "intermediate_session_token": "invalid_session_123",
        "organization_name": "Test Org"
    })
    assert status >= 400, f"Expected error status for invalid session, got {status}"
    assert "error_type" in response or "status_code" in response, f"Expected Stytch error response, got {response}"
