import os
import stytch

# Read credentials from environment variables
project_id = os.environ["STYTCH_B2B_PROJECT_ID"]
secret = os.environ["STYTCH_B2B_SECRET"]

# Read trial_id from file
with open("/logs/trial_id") as f:
    trial_id = f.read().strip()

org_name = f"test-org-{trial_id}"
org_slug = f"test-org-{trial_id}"

# Initialize the Stytch B2B client
client = stytch.B2BClient(project_id=project_id, secret=secret)

# Step 1: Create the organization
print(f"Creating organization: {org_name}")
create_resp = client.organizations.create(
    organization_name=org_name,
    organization_slug=org_slug,
)
print(f"Create response: {create_resp}")

organization_id = create_resp.organization.organization_id
print(f"Created organization ID: {organization_id}")

# Step 2: Update the organization to restrict auth methods
print("Updating organization auth methods to RESTRICTED (sso, magic_link)...")
update_resp = client.organizations.update(
    organization_id=organization_id,
    auth_methods="RESTRICTED",
    allowed_auth_methods=["sso", "magic_link"],
)
print(f"Update response: {update_resp}")

print("Done.")
