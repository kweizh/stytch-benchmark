import os
import stytch

def main():
    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables are not set")
        return

    # Read trial_id
    trial_id_path = "/logs/trial_id"
    if not os.path.exists(trial_id_path):
        trial_id_path = "/logs/artifacts/trial_id"
        
    try:
        with open(trial_id_path, "r") as f:
            trial_id = f.read().strip()
    except FileNotFoundError:
        print(f"Could not find trial_id at /logs/trial_id or /logs/artifacts/trial_id")
        return

    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )

    org_name = f"test-org-{trial_id}"
    org_slug = f"test-org-{trial_id}"

    print(f"Creating organization: {org_name}")
    resp = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug,
    )
    
    if resp.status_code != 200:
        print(f"Error creating organization: {resp}")
        return

    org_id = resp.organization.organization_id
    print(f"Organization created with ID: {org_id}")

    print("Updating organization settings...")
    update_resp = client.organizations.update(
        organization_id=org_id,
        auth_methods="RESTRICTED",
        allowed_auth_methods=["sso", "magic_link"]
    )

    if update_resp.status_code != 200:
        print(f"Error updating organization: {update_resp}")
        return

    print("Organization updated successfully.")
    print(f"Auth methods: {update_resp.organization.auth_methods}")
    print(f"Allowed auth methods: {update_resp.organization.allowed_auth_methods}")

if __name__ == "__main__":
    main()
