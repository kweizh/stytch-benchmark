import os
import subprocess
import time
import socket
import pytest
import json
import uuid
import hmac
import hashlib
import struct
import base64
import urllib.request
import urllib.error

PROJECT_DIR = "/home/user/app"

def wait_for_port(port, timeout=60):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex(('localhost', port)) == 0:
                return True
        time.sleep(1)
    return False

def get_totp_token(secret, interval=30):
    secret += '=' * (-len(secret) % 8)
    key = base64.b32decode(secret, casefold=True)
    t = int(time.time() / interval)
    msg = struct.pack(">Q", t)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = h[19] & 15
    token = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return f"{token:06d}"

@pytest.fixture(scope="module")
def start_app():
    # Install dependencies
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
    
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

def make_post_request(url, data):
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))
    except Exception as e:
        pytest.fail(f"Request to {url} failed: {str(e)}")

def test_totp_flow(start_app):
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    
    # Step 1: Create user
    status, data = make_post_request('http://localhost:3000/users', {'email': email})
    assert status in (200, 201), f"Expected 200 or 201 for /users, got {status}. Response: {data}"
    assert 'user_id' in data, f"Expected 'user_id' in /users response, got: {data}"
    user_id = data['user_id']
    
    # Step 2: Enroll TOTP
    status, data = make_post_request('http://localhost:3000/totp/enroll', {'user_id': user_id})
    assert status == 200, f"Expected 200 for /totp/enroll, got {status}. Response: {data}"
    assert 'totp_id' in data, f"Expected 'totp_id' in /totp/enroll response, got: {data}"
    assert 'secret' in data, f"Expected 'secret' in /totp/enroll response, got: {data}"
    totp_id = data['totp_id']
    secret = data['secret']
    
    # Step 3: Verify TOTP
    totp_code = get_totp_token(secret)
    status, data = make_post_request('http://localhost:3000/totp/verify', {
        'user_id': user_id,
        'totp_code': totp_code
    })
    assert status == 200, f"Expected 200 for /totp/verify, got {status}. Response: {data}"
    assert 'session_token' in data, f"Expected 'session_token' in /totp/verify response, got: {data}"
