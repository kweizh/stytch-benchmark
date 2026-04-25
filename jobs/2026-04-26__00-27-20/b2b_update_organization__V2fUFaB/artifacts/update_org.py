import os
import stytch

def main():
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET")
        return

    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )

    with open("/logs/artifacts/trial_id", "r") as f:
        trial_id = f.read().strip()

    org_name = f"test-org-{trial_id}"
    org_slug = f"test-org-{trial_id}"

    # Create organization
    create_resp = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug,
    )
    
    org_id = create_resp.organization.organization_id
    
    # Update organization
    update_resp = client.organizations.update(
        organization_id=org_id,
        auth_methods="RESTRICTED",
        allowed_auth_methods=["sso", "magic_link"]
    )
    
    print(f"Successfully created and updated organization: {org_id}")

if __name__ == "__main__":
    main()
