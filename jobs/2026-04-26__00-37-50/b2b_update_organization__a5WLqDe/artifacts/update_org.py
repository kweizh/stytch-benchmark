import os
import stytch

# Read credentials from environment variables
project_id = os.environ["STYTCH_B2B_PROJECT_ID"]
secret = os.environ["STYTCH_B2B_SECRET"]

# Read trial_id from file
with open("/logs/artifacts/trial_id") as f:
    trial_id = f.read().strip()

# Build org name and slug
org_name = f"test-org-{trial_id}"
org_slug = f"test-org-{trial_id}"

# Initialize the B2B client
client = stytch.B2BClient(project_id=project_id, secret=secret)

# Create the organization
create_resp = client.organizations.create(
    organization_name=org_name,
    organization_slug=org_slug,
)
print(f"Created organization: {create_resp.organization.organization_id}")

org_id = create_resp.organization.organization_id

# Update the organization to restrict auth methods
update_resp = client.organizations.update(
    organization_id=org_id,
    auth_methods="RESTRICTED",
    allowed_auth_methods=["sso", "magic_link"],
)
print(f"Updated organization auth_methods: {update_resp.organization.auth_methods}")
print(f"Updated organization allowed_auth_methods: {update_resp.organization.allowed_auth_methods}")
