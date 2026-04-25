import os
import stytch

def main():
    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        print("Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables")
        return

    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )

    try:
        with open("/logs/artifacts/trial_id", "r") as f:
            trial_id = f.read().strip()
    except FileNotFoundError:
        print("trial_id file not found")
        return

    org_name = f"test-org-{trial_id}"
    org_slug = f"test-org-{trial_id}"

    print(f"Creating organization: {org_name}")
    try:
        create_resp = client.organizations.create(
            organization_name=org_name,
            organization_slug=org_slug,
        )
        organization_id = create_resp.organization.organization_id
        print(f"Created organization with ID: {organization_id}")
    except Exception as e:
        print(f"Error creating organization: {e}")
        return

    print(f"Updating organization settings for: {organization_id}")
    try:
        update_resp = client.organizations.update(
            organization_id=organization_id,
            auth_methods="RESTRICTED",
            allowed_auth_methods=["sso", "magic_link"],
        )
        print("Successfully updated organization settings")
        print(f"Auth Methods: {update_resp.organization.auth_methods}")
        print(f"Allowed Auth Methods: {update_resp.organization.allowed_auth_methods}")
    except Exception as e:
        print(f"Error updating organization: {e}")

if __name__ == "__main__":
    main()
