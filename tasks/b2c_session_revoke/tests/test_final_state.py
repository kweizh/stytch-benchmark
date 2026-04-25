import os
import subprocess
import time
import socket
import pytest
import requests
import uuid

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
    # Ensure STYTCH_PROJECT_ID and STYTCH_SECRET are available
    assert "STYTCH_PROJECT_ID" in os.environ, "STYTCH_PROJECT_ID is not set"
    assert "STYTCH_SECRET" in os.environ, "STYTCH_SECRET is not set"

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

def test_session_revocation_blocklist(start_app):
    base_url = "http://localhost:3000"
    session = requests.Session()

    # 1. Register
    email = f"test-{uuid.uuid4()}@example.com"
    password = f"{uuid.uuid4()}".replace("-", "").upper()[:16]
    resp = session.post(f"{base_url}/register", json={"email": email, "password": password})
    assert resp.status_code == 200, f"Register failed: {resp.text}"

    # Extract cookies
    cookies = session.cookies.get_dict()
    assert "stytch_session" in cookies, "stytch_session cookie missing after register"
    assert "stytch_session_jwt" in cookies, "stytch_session_jwt cookie missing after register"

    jwt_cookie = cookies["stytch_session_jwt"]

    # 2. Access profile
    resp = session.get(f"{base_url}/profile")
    assert resp.status_code == 200, f"Profile access failed: {resp.text}"

    # 3. Logout
    resp = session.post(f"{base_url}/logout")
    assert resp.status_code == 200, f"Logout failed: {resp.text}"

    # 4. Access profile again with the stolen JWT
    stolen_session = requests.Session()
    stolen_session.cookies.set("stytch_session_jwt", jwt_cookie)
    resp = stolen_session.get(f"{base_url}/profile")

    assert resp.status_code == 401, f"Expected 401 Unauthorized, got {resp.status_code}"
    try:
        data = resp.json()
    except Exception:
        pytest.fail(f"Expected JSON response, got {resp.text}")
    assert data.get("error") == "Session revoked", f"Expected error 'Session revoked', got {data}"
