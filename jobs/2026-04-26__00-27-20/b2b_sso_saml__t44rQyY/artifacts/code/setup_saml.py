import os
import sys
import stytch

def main():
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET")
        sys.exit(1)
        
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
        environment="test",
    )
    
    with open("/logs/artifacts/trial_id", "r") as f:
        trial_id = f.read().strip()
        
    org_name = f"SAML Org {trial_id}"
    org_slug = f"saml-org-{trial_id}"
    
    print(f"Creating organization: {org_name}")
    org_resp = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug
    )
    
    org_id = org_resp.organization.organization_id
    print(f"Created org: {org_id}")
    
    print("Creating SAML connection")
    saml_resp = client.sso.saml.create_connection(
        organization_id=org_id,
        display_name="My SAML Connection"
    )
    
    connection_id = saml_resp.connection.connection_id
    print(f"Created SAML connection: {connection_id}")
    
    print("Updating SAML connection")
    update_resp = client.sso.saml.update_connection(
        organization_id=org_id,
        connection_id=connection_id,
        idp_sso_url="https://idp.example.com/sso",
        idp_entity_id="https://idp.example.com/entity",
    )
    
    print(f"Updated SAML connection: {update_resp.connection.connection_id}")
    print("SAML connection configuration complete.")

if __name__ == "__main__":
    main()
