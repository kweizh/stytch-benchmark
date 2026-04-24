import os
import stytch

def main():
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("Missing Stytch credentials")
        return
        
    try:
        with open("/logs/trial_id", "r") as f:
            trial_id = f.read().strip()
    except FileNotFoundError:
        with open("/logs/artifacts/trial_id", "r") as f:
            trial_id = f.read().strip()
            
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )
    
    org_name = f"test-org-{trial_id}"
    org_slug = f"test-org-{trial_id}"
    
    # Create organization
    print(f"Creating organization: {org_name}")
    resp = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug,
    )
    
    org_id = resp.organization.organization_id
    print(f"Created organization with ID: {org_id}")
    
    # Update organization settings
    print("Updating organization settings...")
    update_resp = client.organizations.update(
        organization_id=org_id,
        auth_methods="RESTRICTED",
        allowed_auth_methods=["sso", "magic_link"]
    )
    
    print("Organization updated successfully.")
    print(f"Auth methods: {update_resp.organization.auth_methods}")
    print(f"Allowed auth methods: {update_resp.organization.allowed_auth_methods}")

if __name__ == "__main__":
    main()
