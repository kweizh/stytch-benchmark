import os
import subprocess
import pytest
import json
import time
import random

PROJECT_DIR = "/home/user/project"
SCRIPT_PATH = os.path.join(PROJECT_DIR, "provision.js")

@pytest.fixture(scope="module")
def setup_test_domain():
    # Generate a unique domain to avoid conflicts across test runs
    domain = f"testdomain{random.randint(1000, 9999)}.com"
    email1 = f"test1@{domain}"
    email2 = f"test2@{domain}"
    return domain, email1, email2

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"provision.js not found at {SCRIPT_PATH}"

def test_provisioning_flow(setup_test_domain):
    domain, email1, email2 = setup_test_domain
    
    # Run the script for the first email
    res1 = subprocess.run(
        ["node", "provision.js", email1],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert res1.returncode == 0, f"Script failed for first email: {res1.stderr}"
    
    member_id1 = res1.stdout.strip()
    assert member_id1.startswith("member-test-") or member_id1.startswith("member-live-"), \
        f"Output does not look like a valid member_id: {member_id1}"
    
    # Wait a moment to ensure API consistency
    time.sleep(2)
    
    # Run the script for the second email
    res2 = subprocess.run(
        ["node", "provision.js", email2],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    assert res2.returncode == 0, f"Script failed for second email: {res2.stderr}"
    
    member_id2 = res2.stdout.strip()
    assert member_id2.startswith("member-test-") or member_id2.startswith("member-live-"), \
        f"Output does not look like a valid member_id: {member_id2}"
    
    assert member_id1 != member_id2, "Expected different member_ids for different emails."
    
    # Use a small verification script to query Stytch API and verify organization setup
    verify_script = f"""
const stytch = require('stytch');
const client = new stytch.B2BClient({{
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
}});

async function verify() {{
  try {{
    const orgs = await client.organizations.search({{
      query: {{
        operator: 'OR',
        operands: [{{ filter_name: 'email_allowed_domains', filter_value: ['{domain}'] }}]
      }}
    }});
    
    if (orgs.organizations.length !== 1) {{
        console.error("Expected exactly 1 organization with domain {domain}, found " + orgs.organizations.length);
        process.exit(1);
    }}
    
    const org = orgs.organizations[0];
    if (org.organization_name !== '{domain}') {{
        console.error("Expected organization_name to be '{domain}', got " + org.organization_name);
        process.exit(1);
    }}
    
    if (org.email_jit_provisioning !== 'RESTRICTED') {{
        console.error("Expected email_jit_provisioning to be 'RESTRICTED', got " + org.email_jit_provisioning);
        process.exit(1);
    }}
    
    if (org.sso_jit_provisioning !== 'ALL_ALLOWED') {{
        console.error("Expected sso_jit_provisioning to be 'ALL_ALLOWED', got " + org.sso_jit_provisioning);
        process.exit(1);
    }}
    
    // verify both members exist in this org
    const mem1 = await client.organizations.members.get({{
      organization_id: org.organization_id,
      member_id: '{member_id1}'
    }});
    
    if (mem1.member.email_address !== '{email1}') {{
        console.error("Member 1 email mismatch");
        process.exit(1);
    }}
    
    const mem2 = await client.organizations.members.get({{
      organization_id: org.organization_id,
      member_id: '{member_id2}'
    }});
    
    if (mem2.member.email_address !== '{email2}') {{
        console.error("Member 2 email mismatch");
        process.exit(1);
    }}
    
    console.log("SUCCESS");
  }} catch (err) {{
    console.error(err);
    process.exit(1);
  }}
}}

verify();
"""
    
    verify_path = os.path.join(PROJECT_DIR, "verify_test.js")
    with open(verify_path, "w") as f:
        f.write(verify_script)
        
    verify_res = subprocess.run(
        ["node", "verify_test.js"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    assert verify_res.returncode == 0, f"Verification script failed: {verify_res.stderr}\n{verify_res.stdout}"
    assert "SUCCESS" in verify_res.stdout, "Verification script did not output SUCCESS."
