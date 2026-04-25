import os
import subprocess
import time
import socket
import pytest
import requests
import json
import stytch
import pyotp

PROJECT_DIR = "/home/user/app"

@pytest.fixture(scope="module")
def stytch_client():
    project_id = os.environ["STYTCH_PROJECT_ID"]
    secret = os.environ["STYTCH_SECRET"]
    return stytch.Client(project_id=project_id, secret=secret)

@pytest.fixture(scope="module")
def start_app():
    # Install dependencies first if needed
    if not os.path.exists(os.path.join(PROJECT_DIR, "node_modules")):
        subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)

    process = subprocess.Popen(
        ["node", "index.js"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # wait for port 3000
    start_time = time.time()
    ready = False
    while time.time() - start_time < 30:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', 3000)) == 0:
                ready = True
                break
        time.sleep(1)

    if not ready:
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000")

    yield

    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=5)

def test_invalid_session_token(start_app):
    """Priority 1: Use requests to verify invalid token handling."""
    resp = requests.post(
        "http://localhost:3000/transfer",
        json={"session_token": "invalid_token_123"},
        timeout=5
    )
    assert resp.status_code == 401, f"Expected 401 for invalid token, got {resp.status_code}"

def test_one_factor_session(start_app, stytch_client):
    """Priority 1: Verify 403 for 1-factor session."""
    email = f"test-{time.time()}@example.com"
    pwd_resp = stytch_client.passwords.create(
        email=email,
        password="Password123!",
        session_duration_minutes=60
    )
    session_token = pwd_resp.session_token

    resp = requests.post(
        "http://localhost:3000/transfer",
        json={"session_token": session_token},
        timeout=5
    )
    assert resp.status_code == 403, f"Expected 403 for 1-factor token, got {resp.status_code}"

    data = resp.json()
    assert "error" in data, "Expected 'error' in response JSON"

def test_two_factor_session(start_app, stytch_client):
    """Priority 1: Verify 200 for 2-factor session."""
    email = f"test-{time.time()}@example.com"
    pwd_resp = stytch_client.passwords.create(
        email=email,
        password="Password123!",
        session_duration_minutes=60
    )
    session_token = pwd_resp.session_token
    user_id = pwd_resp.user_id

    # Add second factor (TOTP)
    totp_resp = stytch_client.totps.create(user_id=user_id)
    secret = totp_resp.secret

    totp = pyotp.TOTP(secret)
    code = totp.now()

    auth_resp = stytch_client.totps.authenticate(
        user_id=user_id,
        totp_code=code,
        session_token=session_token,
        session_duration_minutes=60
    )
    session_token_2 = auth_resp.session_token

    resp = requests.post(
        "http://localhost:3000/transfer",
        json={"session_token": session_token_2},
        timeout=5
    )
    assert resp.status_code == 200, f"Expected 200 for 2-factor token, got {resp.status_code}"

    data = resp.json()
    assert data.get("success") is True, f"Expected {{'success': True}}, got {data}"