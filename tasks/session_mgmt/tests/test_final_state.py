import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/stytch-app"
SCRIPT_FILE = os.path.join(PROJECT_DIR, "verify_session.js")

def test_script_exists():
    assert os.path.isfile(SCRIPT_FILE), f"The script {SCRIPT_FILE} does not exist."

def test_script_uses_stytch_client():
    with open(SCRIPT_FILE, "r") as f:
        content = f.read()
    
    assert "require('stytch')" in content or "from 'stytch'" in content or 'require("stytch")' in content or 'from "stytch"' in content, \
        "The script must import the stytch package."
    
    assert "stytch.Client" in content, "The script must initialize a stytch.Client."
    
    assert "STYTCH_PROJECT_ID" in content and "STYTCH_SECRET" in content, \
        "The script must use STYTCH_PROJECT_ID and STYTCH_SECRET from the environment."
    
    assert "sessions.authenticate" in content, \
        "The script must call client.sessions.authenticate."

def test_script_execution_handles_invalid_token():
    # We run the script with a dummy token.
    # It should make an API call to Stytch and fail gracefully, or throw an error that we can catch.
    # We provide dummy credentials so the Stytch client initializes without throwing immediately.
    env = os.environ.copy()
    env["STYTCH_PROJECT_ID"] = "project-test-00000000-0000-0000-0000-000000000000"
    env["STYTCH_SECRET"] = "secret-test-11111111-1111-1111-1111-111111111111"
    
    result = subprocess.run(
        ["node", "verify_session.js", "dummy_session_token_123"],
        cwd=PROJECT_DIR,
        env=env,
        capture_output=True,
        text=True
    )
    
    # We don't strictly check for success because the token is invalid,
    # but we ensure that node executed the file.
    # If the script has syntax errors or missing dependencies, it would fail with a different error.
    assert "MODULE_NOT_FOUND" not in result.stderr, "The script failed due to missing modules. Did you run npm install stytch?"
    assert "SyntaxError" not in result.stderr, "The script has a syntax error."
