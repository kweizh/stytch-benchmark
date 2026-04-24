import os
import stytch
from stytch.b2b.client import Client

def main():
    # Read trial_id from /logs/trial_id as per requirements
    # Fallback to /logs/artifacts/trial_id if not found
    trial_id_path = "/logs/trial_id"
    if not os.path.exists(trial_id_path):
        trial_id_path = "/logs/artifacts/trial_id"
    
    with open(trial_id_path, "r") as f:
        trial_id = f.read().strip()
    
    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("Error: STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET not set")
        return

    client = Client(
        project_id=project_id,
        secret=secret
    )

    org_name = f"SAML Org {trial_id}"
    org_slug = f"saml-org-{trial_id}"

    print(f"Creating organization: {org_name} ({org_slug})")
    resp = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug
    )
    organization_id = resp.organization.organization_id
    print(f"Created Organization ID: {organization_id}")

    print("Creating SAML connection...")
    resp = client.sso.saml.create_connection(
        organization_id=organization_id,
        display_name="SAML Connection"
    )
    connection_id = resp.connection.connection_id
    print(f"Created SAML Connection ID: {connection_id}")

    print("Updating SAML connection with IdP details...")
    resp = client.sso.saml.update_connection(
        organization_id=organization_id,
        connection_id=connection_id,
        idp_sso_url="https://idp.example.com/sso",
        idp_entity_id="https://idp.example.com/entity"
    )
    print(f"Successfully updated SAML connection: {resp.connection.connection_id}")

if __name__ == "__main__":
    main()
