import os
import subprocess
import json
import pytest
import urllib.request
import urllib.parse
import base64
import random
import string

PROJECT_DIR = "/home/user/project"
LOG_FILE = "/home/user/project/output.log"

def test_script_execution_and_output():
    """Run the script and verify it outputs a valid organization_id."""
    script_path = os.path.join(PROJECT_DIR, "b2b_magic_link.js")
    assert os.path.isfile(script_path), f"b2b_magic_link.js not found at {script_path}"

    # Generate a random slug to avoid collision on multiple runs
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    test_slug = f"test-org-{random_suffix}"

    # Run the script
    result = subprocess.run(
        ["node", "b2b_magic_link.js", "Test Org", test_slug, "test@example.com"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    # Check if the script succeeded
    assert result.returncode == 0, f"Script execution failed: {result.stderr}"
    
    # Save output to log file to match the truth setup
    with open(LOG_FILE, "w") as f:
        f.write(result.stdout)
        
    # Read and parse output
    try:
        output_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        pytest.fail(f"Output is not valid JSON: {result.stdout}")
        
    assert "organization_id" in output_data, f"organization_id not found in JSON output: {output_data}"
    
    org_id = output_data["organization_id"]
    
    # Verify via Stytch API
    project_id = os.environ.get("STYTCH_PROJECT_ID")
    secret = os.environ.get("STYTCH_SECRET")
    
    assert project_id, "STYTCH_PROJECT_ID environment variable is missing."
    assert secret, "STYTCH_SECRET environment variable is missing."
    
    url = f"https://test.stytch.com/v1/b2b/organizations/{org_id}"
    
    auth_string = f"{project_id}:{secret}"
    auth_bytes = auth_string.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_string = base64_bytes.decode('ascii')
    
    req = urllib.request.Request(url)
    req.add_header('Authorization', f'Basic {base64_string}')
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode())
            assert "organization" in res_data, "Organization data not found in Stytch response."
            assert res_data["organization"]["organization_slug"] == test_slug, \
                f"Organization slug mismatch. Expected '{test_slug}', got {res_data['organization']['organization_slug']}"
    except urllib.error.HTTPError as e:
        pytest.fail(f"Stytch API returned HTTP error: {e.code} - {e.read().decode()}")
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Stytch API: {e.reason}")
