import os
import sys
import stytch

def main():
    try:
        with open('/logs/trial_id', 'r') as f:
            trial_id = f.read().strip()
    except FileNotFoundError:
        try:
            with open('/logs/artifacts/trial_id', 'r') as f:
                trial_id = f.read().strip()
        except FileNotFoundError:
            print("Could not find trial_id")
            sys.exit(1)
            
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("Missing Stytch credentials")
        sys.exit(1)
        
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )
    
    org_name = f"test-org-{trial_id}"
    org_slug = f"test-org-{trial_id}"
    
    # Create organization
    org_resp = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug
    )
    
    org_id = org_resp.organization.organization_id
    print(f"Created organization: {org_id}")
    
    # Create OIDC Connection
    conn_resp = client.sso.oidc.create_connection(
        organization_id=org_id,
        display_name="My OIDC Connection"
    )
    
    connection_id = conn_resp.connection.connection_id
    print(f"Created OIDC connection: {connection_id}")
    
    # Update OIDC connection
    update_resp = client.sso.oidc.update_connection(
        organization_id=org_id,
        connection_id=connection_id,
        client_id="mock-client-id",
        client_secret="mock-client-secret",
        issuer="https://mock-idp.com",
        authorization_url="https://mock-idp.com/auth",
        token_url="https://mock-idp.com/token",
        userinfo_url="https://mock-idp.com/userinfo",
        jwks_url="https://mock-idp.com/jwks"
    )
    
    print(f"Updated OIDC connection: {update_resp.connection.connection_id}")

if __name__ == "__main__":
    main()
