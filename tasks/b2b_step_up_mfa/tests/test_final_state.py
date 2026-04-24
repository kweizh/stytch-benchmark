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
    project_id = os.environ["STYTCH_B2B_PROJECT_ID"]
    secret = os.environ["STYTCH_B2B_SECRET"]
    return stytch.B2BClient(project_id=project_id, secret=secret)

@pytest.fixture(scope="module")
def start_app():
    # Install dependencies first if needed
    if not os.path.exists(os.path.join(PROJECT_DIR, "node_modules")):
        subprocess.run(["npm", "install"], cwd=PROJECT_DIR, check=True)
        
    process = subprocess.Popen(
        ["npm", "start"],
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

def get_trial_id():
    try:
        with open("/logs/artifacts/trial_id", "r") as f:
            return f.read().strip()
    except Exception:
        return str(int(time.time() * 1000))

def test_invalid_session_token(start_app):
    """Priority 1: Use requests to verify invalid token handling."""
    resp = requests.post(
        "http://localhost:3000/sensitive-action",
        cookies={"stytch_session": "invalid_token_123"},
        timeout=5
    )
    assert resp.status_code == 401, f"Expected 401 for invalid token, got {resp.status_code}"

def test_one_factor_session(start_app, stytch_client):
    """Priority 1: Verify 403 for 1-factor session."""
    trial_id = get_trial_id()
    org_name = f"Test Org {trial_id} 1F"
    org_resp = stytch_client.organizations.create(
        organization_name=org_name,
        organization_slug=f"test-org-1f-{trial_id}"
    )
    org_id = org_resp.organization.organization_id

    email = f"test-1f-{trial_id}@example.com"
    member_resp = stytch_client.organizations.members.create(
        organization_id=org_id,
        email_address=email,
        mfa_phone_number="+10000000000",
        mfa_enrolled=True
    )
    member_id = member_resp.member.member_id

    # Send SMS OTP (Sandbox bypass)
    stytch_client.otps.sms.send(
        organization_id=org_id,
        member_id=member_id,
        mfa_phone_number="+10000000000"
    )

    # Authenticate SMS OTP to get a 1-factor session
    auth_resp = stytch_client.otps.sms.authenticate(
        organization_id=org_id,
        member_id=member_id,
        code="000000"
    )
    session_token = auth_resp.session_token

    resp = requests.post(
        "http://localhost:3000/sensitive-action",
        cookies={"stytch_session": session_token},
        timeout=5
    )
    assert resp.status_code == 403, f"Expected 403 for 1-factor token, got {resp.status_code}"

def test_two_factor_session(start_app, stytch_client):
    """Priority 1: Verify 200 for 2-factor session."""
    trial_id = get_trial_id()
    org_name = f"Test Org {trial_id} 2F"
    org_resp = stytch_client.organizations.create(
        organization_name=org_name,
        organization_slug=f"test-org-2f-{trial_id}"
    )
    org_id = org_resp.organization.organization_id

    email = f"test-2f-{trial_id}@example.com"
    member_resp = stytch_client.organizations.members.create(
        organization_id=org_id,
        email_address=email,
        mfa_phone_number="+10000000000",
        mfa_enrolled=True
    )
    member_id = member_resp.member.member_id

    # Send SMS OTP (Sandbox bypass)
    stytch_client.otps.sms.send(
        organization_id=org_id,
        member_id=member_id,
        mfa_phone_number="+10000000000"
    )

    # Authenticate SMS OTP to get a 1-factor session
    auth_resp = stytch_client.otps.sms.authenticate(
        organization_id=org_id,
        member_id=member_id,
        code="000000"
    )
    session_token = auth_resp.session_token

    # Add second factor (TOTP)
    totp_resp = stytch_client.totps.create(
        organization_id=org_id,
        member_id=member_id
    )
    secret = totp_resp.secret
    
    totp = pyotp.TOTP(secret)
    code = totp.now()
    
    # Authenticate TOTP to step up the session to 2 factors
    auth_resp_2 = stytch_client.totps.authenticate(
        organization_id=org_id,
        member_id=member_id,
        code=code,
        session_token=session_token
    )
    session_token_2 = auth_resp_2.session_token

    resp = requests.post(
        "http://localhost:3000/sensitive-action",
        cookies={"stytch_session": session_token_2},
        timeout=5
    )
    assert resp.status_code == 200, f"Expected 200 for 2-factor token, got {resp.status_code}"
