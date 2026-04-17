import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/stytch-b2c-otp"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "index.js")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"index.js not found at {SCRIPT_PATH}"

def test_script_execution_and_output():
    result = subprocess.run(
        ["node", "index.js"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"'node index.js' failed: {result.stderr}"
    
    stdout = result.stdout.strip()
    assert "stytch-session-" in stdout, f"Expected session token starting with 'stytch-session-' in output, got: {stdout}"
