import os
import time
import socket
import subprocess
import requests
import pytest
import signal

PROJECT_DIR = "/home/user/project"

def wait_for_port(port, timeout=30):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(2)
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
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    # Shut down the app
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=10)

def test_amika_api_validation_dummy_token(start_app):
    """
    Use the amika API (simulated via requests) to validate the endpoint
    with a dummy intermediate session token.
    """
    url = "http://localhost:3000/api/discovery/organizations"
    payload = {"intermediate_session_token": "dummy_token"}
    
    response = requests.post(url, json=payload)
    
    # We expect a 400 Bad Request because the dummy token is invalid
    assert response.status_code == 400, f"Expected 400 status code, got {response.status_code}. Response: {response.text}"
    
    data = response.json()
    # The error should originate from Stytch, indicating the token is invalid
    # It might be nested depending on how the user implements it, but we check for 'invalid' or 'token' in the stringified response
    response_str = str(data).lower()
    assert "invalid" in response_str or "token" in response_str, "Expected Stytch invalid token error in the response."

def test_amika_api_validation_missing_token(start_app):
    """
    Use the amika API (simulated via requests) to validate the endpoint
    with a missing token.
    """
    url = "http://localhost:3000/api/discovery/organizations"
    
    response = requests.post(url, json={})
    
    # We expect a 400 Bad Request because the token is missing
    assert response.status_code == 400, f"Expected 400 status code, got {response.status_code}. Response: {response.text}"
