import os
import json
import hashlib
import base64
import pytest

PROJECT_DIR = "/home/user/stytch_app"
PKCE_FILE = os.path.join(PROJECT_DIR, "pkce.json")

def test_pkce_file_exists():
    """Priority 3: Verify the output file exists."""
    assert os.path.isfile(PKCE_FILE), f"PKCE output file not found at {PKCE_FILE}"

def test_pkce_contents():
    """Priority 3: Verify the contents of the PKCE output file."""
    with open(PKCE_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {PKCE_FILE} does not contain valid JSON.")
    
    assert "code_verifier" in data, "Missing 'code_verifier' in pkce.json"
    assert "code_challenge" in data, "Missing 'code_challenge' in pkce.json"
    
    code_verifier = data["code_verifier"]
    code_challenge = data["code_challenge"]
    
    # Verify length of code_verifier (RFC 7636 requires 43-128 chars)
    assert len(code_verifier) >= 43, f"code_verifier is too short: {len(code_verifier)} characters (minimum 43)"
    assert len(code_verifier) <= 128, f"code_verifier is too long: {len(code_verifier)} characters (maximum 128)"
    
    # Verify the code_challenge is correctly derived from code_verifier
    # SHA-256 hash
    hash_obj = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    # Base64url encode without padding
    expected_challenge = base64.urlsafe_b64encode(hash_obj).decode('utf-8').rstrip('=')
    
    assert code_challenge == expected_challenge, f"code_challenge does not match the expected base64url-encoded SHA-256 hash of code_verifier. Expected: {expected_challenge}, Got: {code_challenge}"
