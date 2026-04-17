import os
import json
import subprocess
import pytest

PROJECT_DIR = "/home/user/myproject"
OUTPUT_FILE = os.path.join(PROJECT_DIR, "output.json")

def test_output_file_exists():
    """Priority 3 fallback: basic file existence check."""
    assert os.path.isfile(OUTPUT_FILE), f"Output file not found at {OUTPUT_FILE}"

def test_output_file_contains_valid_json():
    """Priority 3 fallback: parse JSON and check keys."""
    with open(OUTPUT_FILE) as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {OUTPUT_FILE} does not contain valid JSON.")
    
    assert "organization_id" in data, "organization_id is missing from output.json."
    assert "connection_id" in data, "connection_id is missing from output.json."

def test_stytch_verification_script():
    """Priority 1: Use Node.js script with Stytch SDK to verify the backend state."""
    # Write a temporary verification script that uses the installed stytch SDK
    script_path = os.path.join(PROJECT_DIR, "verify_stytch_state.js")
    script_content = """
const stytch = require('stytch');
const fs = require('fs');

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const output = JSON.parse(fs.readFileSync('output.json', 'utf8'));

async function verify() {
  let orgResp;
  try {
    orgResp = await client.organizations.get({ organization_id: output.organization_id });
  } catch (err) {
    throw new Error(`Failed to get organization: ${err.message}`);
  }
  
  if (orgResp.organization.organization_name !== 'Acme Corp') {
    throw new Error(`Expected organization name 'Acme Corp', got '${orgResp.organization.organization_name}'`);
  }
  if (orgResp.organization.organization_slug !== 'acme-corp') {
    throw new Error(`Expected organization slug 'acme-corp', got '${orgResp.organization.organization_slug}'`);
  }
  
  let ssoResp;
  try {
    ssoResp = await client.sso.getConnections({ organization_id: output.organization_id });
  } catch (err) {
    throw new Error(`Failed to get SSO connections: ${err.message}`);
  }
  
  const samlConnection = ssoResp.saml_connections.find(c => c.connection_id === output.connection_id);
  if (!samlConnection) {
    throw new Error(`SAML connection with ID ${output.connection_id} not found in organization.`);
  }
  if (samlConnection.display_name !== 'Acme SAML') {
    throw new Error(`Expected SAML connection display name 'Acme SAML', got '${samlConnection.display_name}'`);
  }
  
  console.log('SUCCESS');
}

verify().catch(err => {
  console.error(err.message);
  process.exit(1);
});
"""
    with open(script_path, "w") as f:
        f.write(script_content)
        
    result = subprocess.run(
        ["node", "verify_stytch_state.js"],
        capture_output=True,
        text=True,
        cwd=PROJECT_DIR
    )
    assert result.returncode == 0, f"Stytch API verification failed: {result.stderr.strip() or result.stdout.strip()}"
    assert "SUCCESS" in result.stdout, "Verification script did not output SUCCESS."
