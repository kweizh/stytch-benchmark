import os
import subprocess
import time
import socket
import pytest

PROJECT_DIR = "/home/user/stytch-app"

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
    # Make sure STYTCH_PROJECT_ID and STYTCH_SECRET are exported for the app
    env = os.environ.copy()
    if "STYTCH_PROJECT_ID" not in env:
        env["STYTCH_PROJECT_ID"] = "project-test-00000000-0000-0000-0000-000000000000"
    if "STYTCH_SECRET" not in env:
        env["STYTCH_SECRET"] = "secret-test-11111111-1111-1111-1111-111111111111"

    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=env
    )
    
    if not wait_for_port(3000):
        import signal
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        pytest.fail("App failed to start and listen on port 3000.")
    
    yield
    
    import signal
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    process.wait(timeout=30)

def test_no_token(start_app):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "http://localhost:3000/upload"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() in ["401", "403"], \
        f"Expected 401 or 403 for no token, got {result.stdout.strip()}"

def test_invalid_token(start_app):
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-X", "POST", "-H", "Authorization: Bearer invalid_token", "http://localhost:3000/upload"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() in ["401", "403"], \
        f"Expected 401 or 403 for invalid token, got {result.stdout.strip()}"

def test_middleware_file_exists():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "middleware.js")), \
        "middleware.js not found in project directory."

def test_index_js_uses_middleware():
    index_path = os.path.join(PROJECT_DIR, "index.js")
    with open(index_path, "r") as f:
        content = f.read()
    assert "authMiddleware" in content, "index.js does not seem to use authMiddleware."
