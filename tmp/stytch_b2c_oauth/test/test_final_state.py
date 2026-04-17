import os
import subprocess
import time
import socket
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
    process.wait(timeout=30)

def test_login_redirects(start_app):
    """Priority 1: Check that /login redirects to Stytch."""
    result = subprocess.run(
        ["curl", "-I", "http://localhost:3000/login"],
        capture_output=True, text=True
    )
    assert "302" in result.stdout or "301" in result.stdout, "Expected a redirect from /login"
    assert "stytch.com" in result.stdout.lower() or "stytch" in result.stdout.lower(), "Expected redirect to Stytch OAuth URL"

def test_profile_requires_auth(start_app):
    """Priority 1: Check that /profile requires authentication."""
    result = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "http://localhost:3000/profile"],
        capture_output=True, text=True
    )
    assert result.stdout.strip() == "401", "Expected 401 Unauthorized for /profile without session"
