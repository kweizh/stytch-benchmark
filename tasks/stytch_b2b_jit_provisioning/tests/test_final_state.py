import os
import pytest

PROJECT_DIR = "/home/user/stytch_project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "setup_jit.py")

def test_script_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(SCRIPT_PATH), f"setup_jit.py not found at {SCRIPT_PATH}"

def test_script_imports_requests():
    """Priority 3 fallback: file content check."""
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "import requests" in content, "Expected 'import requests' in setup_jit.py"

def test_script_api_url():
    """Priority 3 fallback: file content check."""
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "https://test.stytch.com/v1/b2b/organizations/" in content, "Expected Stytch API URL in setup_jit.py"

def test_script_payload():
    """Priority 3 fallback: file content check."""
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "RESTRICTED" in content, "Expected 'RESTRICTED' for oauth_tenant_jit_provisioning in setup_jit.py"
    assert "SLACK-123" in content, "Expected 'SLACK-123' in setup_jit.py"
    assert "12345" in content, "Expected '12345' in setup_jit.py"
    assert "slack" in content.lower(), "Expected 'slack' in setup_jit.py"
    assert "github" in content.lower(), "Expected 'github' in setup_jit.py"

def test_script_credentials():
    """Priority 3 fallback: file content check."""
    with open(SCRIPT_PATH) as f:
        content = f.read()
    assert "project-test-00000000-0000-0000-0000-000000000000" in content, "Expected Project ID in setup_jit.py"
    assert "secret-test-11111111-1111-1111-1111-111111111111" in content, "Expected Secret in setup_jit.py"
