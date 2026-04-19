import os
import subprocess
import time
import socket
import json
import pytest

PROJECT_DIR = "/home/user/app"

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
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
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
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_authenticate_start(start_app):
    """Verify POST /webauthn/authenticate/start returns public_key_credential_request_options."""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            "http://localhost:3000/webauthn/authenticate/start",
            "-H", "Content-Type: application/json",
            "-d", '{"domain": "localhost"}'
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert "public_key_credential_request_options" in data, \
        f"Expected public_key_credential_request_options in response, got: {data}"

def test_authenticate(start_app):
    """Verify POST /webauthn/authenticate proxies the error from Stytch API."""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            "http://localhost:3000/webauthn/authenticate",
            "-H", "Content-Type: application/json",
            "-d", '{"public_key_credential": "invalid_credential"}'
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    # The Stytch API should return an error object containing error_type
    assert "error_type" in data, f"Expected Stytch error object with error_type, got: {data}"
    assert "invalid" in data["error_type"].lower(), f"Expected an invalid credential error, got: {data['error_type']}"

def test_register_start(start_app):
    """Verify POST /webauthn/register/start returns public_key_credential_creation_options."""
    # We need a real user_id to get a valid response from Stytch. 
    # But since we don't have one, we can pass a dummy one and check for a Stytch error.
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            "http://localhost:3000/webauthn/register/start",
            "-H", "Content-Type: application/json",
            "-d", '{"user_id": "user-test-invalid", "domain": "localhost"}'
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert "error_type" in data, f"Expected Stytch error object with error_type, got: {data}"

def test_register(start_app):
    """Verify POST /webauthn/register proxies the error from Stytch API."""
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST",
            "http://localhost:3000/webauthn/register",
            "-H", "Content-Type: application/json",
            "-d", '{"user_id": "user-test-invalid", "public_key_credential": "invalid_credential"}'
        ],
        capture_output=True, text=True
    )
    assert result.returncode == 0, f"curl failed: {result.stderr}"
    
    try:
        data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Expected JSON response, got: {result.stdout}")
        
    assert "error_type" in data, f"Expected Stytch error object with error_type, got: {data}"
