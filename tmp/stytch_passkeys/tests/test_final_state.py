import os
import subprocess
import json
import pytest

PROJECT_DIR = "/home/user/app"

@pytest.fixture(scope="module")
def setup_test_user():
    # Create a test user via Stytch SDK
    script = """
    const stytch = require('stytch');
    const client = new stytch.Client({
      project_id: process.env.STYTCH_PROJECT_ID,
      secret: process.env.STYTCH_SECRET,
    });
    client.users.create({
      email: { email_address: "test-passkey-" + Date.now() + "@example.com" }
    })
      .then(res => console.log(JSON.stringify(res)))
      .catch(err => { console.error(err); process.exit(1); });
    """
    
    result = subprocess.run(
        ["node", "-e", script],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    if result.returncode != 0:
        pytest.fail(f"Failed to create test user: {result.stderr}")
        
    try:
        user_data = json.loads(result.stdout)
        user_id = user_data["user_id"]
    except (json.JSONDecodeError, KeyError) as e:
        pytest.fail(f"Failed to parse user creation response: {result.stdout}")
        
    yield user_id
    
    # Clean up the test user
    cleanup_script = f"""
    const stytch = require('stytch');
    const client = new stytch.Client({{
      project_id: process.env.STYTCH_PROJECT_ID,
      secret: process.env.STYTCH_SECRET,
    }});
    client.users.delete('{user_id}')
      .then(() => console.log('deleted'))
      .catch(err => {{ console.error(err); process.exit(1); }});
    """
    subprocess.run(["node", "-e", cleanup_script], capture_output=True, text=True, cwd=PROJECT_DIR)

def test_script_execution_and_output(setup_test_user):
    """Priority 1: Use the script itself to verify it outputs valid WebAuthn options."""
    user_id = setup_test_user
    
    result = subprocess.run(
        ["node", "index.js", user_id],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"
    
    try:
        output_json = json.loads(result.stdout.strip())
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON: {result.stdout}")
        
    assert "challenge" in output_json, "Expected 'challenge' in WebAuthn creation options"
    assert "rp" in output_json, "Expected 'rp' in WebAuthn creation options"
    assert "user" in output_json, "Expected 'user' in WebAuthn creation options"
    assert "pubKeyCredParams" in output_json, "Expected 'pubKeyCredParams' in WebAuthn creation options"
    
def test_script_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(os.path.join(PROJECT_DIR, "index.js")), "index.js not found in project directory."