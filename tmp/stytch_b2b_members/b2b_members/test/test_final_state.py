import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/stytch_project"
SCRIPT_FILE = os.path.join(PROJECT_DIR, "manage_b2b.js")
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def test_script_executes_successfully():
    """Run the user's script and verify it completes without errors."""
    assert os.path.isfile(SCRIPT_FILE), f"Script not found at {SCRIPT_FILE}"
    
    # We run npm install just in case the user didn't, as per setup steps
    subprocess.run(["npm", "install"], cwd=PROJECT_DIR, capture_output=True)
    
    result = subprocess.run(
        ["node", "manage_b2b.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}\nStdout: {result.stdout}"

def test_output_file_exists():
    """Verify that the output file was created."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

def test_output_json_contains_valid_ids():
    """Verify the contents of the output JSON file."""
    with open(OUTPUT_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Output file {OUTPUT_FILE} is not valid JSON.")
            
    assert "organization_id" in data, "JSON does not contain 'organization_id'"
    assert data["organization_id"].startswith("organization-"), \
        f"organization_id should start with 'organization-', got: {data['organization_id']}"
        
    assert "member_id" in data, "JSON does not contain 'member_id'"
    assert data["member_id"].startswith("member-"), \
        f"member_id should start with 'member-', got: {data['member_id']}"
