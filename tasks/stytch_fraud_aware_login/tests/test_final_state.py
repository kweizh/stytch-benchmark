import os
import subprocess
import time
import socket
import pytest
import urllib.request
import urllib.error
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
def setup_and_start_app():
    # Write mock stytch SDK to simulate API responses
    mock_stytch_code = """
class Client {
    constructor(config) {
        this.config = config;
        this.fraud = {
            fingerprint: {
                lookup: this.lookup.bind(this)
            }
        };
    }
    async lookup(params) {
        const { telemetry_id } = params;
        if (telemetry_id === 'valid-allow-id') return { verdict: { action: 'ALLOW' } };
        if (telemetry_id === 'valid-challenge-id') return { verdict: { action: 'CHALLENGE' } };
        if (telemetry_id === 'valid-block-id') return { verdict: { action: 'BLOCK' } };
        if (!telemetry_id) throw new Error('telemetry_id missing in params');
        throw new Error('Not found');
    }
}
class B2BClient extends Client {}
module.exports = { Client, B2BClient };
"""
    stytch_dir = os.path.join(PROJECT_DIR, "node_modules", "stytch")
    os.makedirs(stytch_dir, exist_ok=True)
    with open(os.path.join(stytch_dir, "index.js"), "w") as f:
        f.write(mock_stytch_code)
    
    # Start the app
    process = subprocess.Popen(
        ["npm", "start"],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid,
        env=dict(os.environ, STYTCH_PROJECT_ID="project-test-1111", STYTCH_SECRET="secret-test-1111")
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

def make_post_request(telemetry_id=None):
    req = urllib.request.Request("http://localhost:3000/login", method="POST")
    req.add_header('Content-Type', 'application/json')
    if telemetry_id:
        req.add_header('X-Telemetry-ID', telemetry_id)
    
    try:
        with urllib.request.urlopen(req, data=b'{}') as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())

def test_missing_telemetry_id(setup_and_start_app):
    status, body = make_post_request(None)
    assert status == 400, f"Expected 400 for missing telemetry ID, got {status}"
    assert body.get("error") == "Telemetry ID missing", f"Expected error message 'Telemetry ID missing', got {body}"

def test_allow_verdict(setup_and_start_app):
    status, body = make_post_request("valid-allow-id")
    assert status == 200, f"Expected 200 for ALLOW verdict, got {status}"
    assert body.get("success") is True, f"Expected success: true, got {body}"

def test_challenge_verdict(setup_and_start_app):
    status, body = make_post_request("valid-challenge-id")
    assert status == 401, f"Expected 401 for CHALLENGE verdict, got {status}"
    assert body.get("error") == "MFA required", f"Expected error message 'MFA required', got {body}"

def test_block_verdict(setup_and_start_app):
    status, body = make_post_request("valid-block-id")
    assert status == 403, f"Expected 403 for BLOCK verdict, got {status}"
    assert body.get("error") == "Access denied", f"Expected error message 'Access denied', got {body}"

def test_invalid_telemetry_id(setup_and_start_app):
    status, body = make_post_request("invalid-id")
    assert status == 403, f"Expected 403 for invalid telemetry ID, got {status}"
    assert body.get("error") == "Access denied", f"Expected error message 'Access denied', got {body}"
