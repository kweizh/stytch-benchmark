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
        time.sleep(1)
    return False

@pytest.fixture(scope="module")
def start_app():
    # Start the app
    process = subprocess.Popen(
        ["node", "server.js"],
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
        pytest.fail("App failed to start and listen on required ports.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_send_discovery(start_app):
    req = urllib.request.Request(
        'http://localhost:3000/send-discovery',
        data=json.dumps({"email": "test@stytch.com"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        response = urllib.request.urlopen(req)
        assert response.getcode() == 200, f"Expected 200 OK, got {response.getcode()}"
        data = json.loads(response.read().decode('utf-8'))
        assert "status_code" in data, "Expected status_code in response"
        assert "message_id" in data, "Expected message_id in response"
    except urllib.error.HTTPError as e:
        pytest.fail(f"HTTPError on /send-discovery: {e.read().decode('utf-8')}")
    except Exception as e:
        pytest.fail(f"Error on /send-discovery: {str(e)}")

def test_complete_discovery_invalid_token(start_app):
    req = urllib.request.Request(
        'http://localhost:3000/complete-discovery',
        data=json.dumps({
            "intermediate_session_token": "fake_token",
            "discovered_organizations": []
        }).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        response = urllib.request.urlopen(req)
        pytest.fail(f"Expected 400 Bad Request, but got 200 OK: {response.read().decode('utf-8')}")
    except urllib.error.HTTPError as e:
        assert e.code == 400, f"Expected 400 Bad Request, got {e.code}"
        data = json.loads(e.read().decode('utf-8'))
        assert "invalid_token" in str(data) or "error_type" in data or "status_code" in data, \
            f"Expected Stytch error indicating invalid token, got: {data}"

def test_server_code_contains_discovery_methods():
    server_js_path = os.path.join(PROJECT_DIR, "server.js")
    assert os.path.isfile(server_js_path), f"server.js not found at {server_js_path}"
    with open(server_js_path, "r") as f:
        content = f.read()
    assert "intermediateSessions.exchange" in content, "Expected to find 'intermediateSessions.exchange' in server.js"
    assert "organizations.create" in content, "Expected to find 'organizations.create' in server.js"
