import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/stytch_app"

def test_stytch_sms_cli():
    # Ensure environment variables are present
    project_id = os.environ.get("STYTCH_PROJECT_ID")
    secret = os.environ.get("STYTCH_SECRET")
    
    assert project_id is not None, "STYTCH_PROJECT_ID environment variable is missing."
    assert secret is not None, "STYTCH_SECRET environment variable is missing."

    # Test 'send' command
    send_result = subprocess.run(
        ["node", "stytch_sms.js", "send", "+10000000000"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert send_result.returncode == 0, f"'send' command failed with error: {send_result.stderr}"
    
    phone_id = send_result.stdout.strip()
    assert phone_id.startswith("phone-"), f"Expected phone_id starting with 'phone-', got: {phone_id}"

    # Test 'authenticate' command
    auth_result = subprocess.run(
        ["node", "stytch_sms.js", "authenticate", phone_id, "000000"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert auth_result.returncode == 0, f"'authenticate' command failed with error: {auth_result.stderr}"
    
    user_id = auth_result.stdout.strip()
    assert user_id.startswith("user-"), f"Expected user_id starting with 'user-', got: {user_id}"
