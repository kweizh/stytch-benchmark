import os
import subprocess
import time
import socket
import pytest
import json
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/stytch-app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
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
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_login_endpoint(start_app):
    """Test the POST /login endpoint."""
    url = "http://localhost:3000/login"
    data = json.dumps({"email": "sandbox@stytch.com"}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"POST /login request failed: {e}")

def test_authenticate_endpoint(start_app):
    """Test the GET /authenticate endpoint with the sandbox token."""
    token = "DOYoip3rvIMMW5lgItikFK-Ak1CfMsgjuiCyI7uuU94="
    url = f"http://localhost:3000/authenticate?token={token}"
    
    try:
        with urllib.request.urlopen(url) as response:
            assert response.status == 200, f"Expected status 200, got {response.status}"
            body = response.read().decode('utf-8')
            res_json = json.loads(body)
            assert res_json.get("success") is True, f"Expected success: true, got: {res_json}"
            assert "user_id" in res_json, f"Expected user_id in response, got: {res_json}"
    except urllib.error.URLError as e:
        pytest.fail(f"GET /authenticate request failed: {e}")
