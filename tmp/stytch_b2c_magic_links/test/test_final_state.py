import os
import subprocess
import time
import socket
import pytest
import urllib.request
import json

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=30):
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
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_index_js_exists():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "index.js")), "index.js not found in /home/user/app"

def test_stytch_client_initialization():
    with open(os.path.join(PROJECT_DIR, "index.js"), "r") as f:
        content = f.read()
    assert "stytch.Client" in content or "new stytch.Client" in content, "Stytch B2C client initialization not found in index.js"
    assert "magicLinks.email.loginOrCreate" in content or "magicLinks.email.send" in content, "Magic link send method not found in index.js"
    assert "magicLinks.authenticate" in content, "Magic link authenticate method not found in index.js"

def test_send_magic_link_endpoint(start_app):
    req = urllib.request.Request(
        "http://localhost:3000/send-magic-link",
        data=json.dumps({"email": "test@example.com"}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        response = urllib.request.urlopen(req)
        assert response.status == 200, "Expected 200 OK for /send-magic-link"
    except urllib.error.HTTPError as e:
        # A 400 Bad Request from Stytch is acceptable if it's due to invalid redirect URL or project settings
        assert e.code in [200, 400, 500], f"Unexpected HTTP status {e.code} for /send-magic-link"

def test_authenticate_endpoint(start_app):
    try:
        response = urllib.request.urlopen("http://localhost:3000/authenticate?token=dummy_token")
        # Should not succeed with a dummy token
        assert False, "Expected an error for invalid token"
    except urllib.error.HTTPError as e:
        assert e.code in [400, 401, 500], f"Expected error status for invalid token, got {e.code}"
