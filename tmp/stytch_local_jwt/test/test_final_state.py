import os
import subprocess
import pytest
import urllib.request
import json

PROJECT_DIR = "/home/user/app"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "validate_jwt.js")

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_script_uses_local_validation():
    with open(SCRIPT_PATH, "r") as f:
        content = f.read()
    assert "authenticateJwtLocal" in content or "authenticateJwt" in content, \
        "Script must use local JWT validation method (authenticateJwtLocal)."

def test_invalid_jwt():
    result = subprocess.run(
        ["node", "validate_jwt.js", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid.signature"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    # The script should output "Invalid JWT" when validation fails
    assert "Invalid JWT" in result.stdout or "Invalid JWT" in result.stderr, \
        f"Expected output to contain 'Invalid JWT', got: {result.stdout} {result.stderr}"

def test_missing_jwt():
    result = subprocess.run(
        ["node", "validate_jwt.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    # The script should gracefully handle missing JWT or output Invalid JWT
    assert result.returncode != 0 or "Invalid JWT" in result.stdout or "Invalid JWT" in result.stderr, \
        "Script should handle missing JWT gracefully."