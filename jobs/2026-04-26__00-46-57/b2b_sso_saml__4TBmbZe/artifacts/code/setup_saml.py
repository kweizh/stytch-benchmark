import os
import sys
import stytch

def main():
    # Read trial_id
    try:
        with open("/logs/artifacts/trial_id", "r") as f:
            trial_id = f.read().strip()
    except Exception as e:
        print(f"Error reading trial_id: {e}")
        sys.exit(1)

    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        print("STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET environment variables must be set.")
        sys.exit(1)

    # Initialize Stytch B2B Client
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )

    org_name = f"SAML Org {trial_id}"
    org_slug = f"saml-org-{trial_id}"

    print(f"Creating organization: {org_name} ({org_slug})")
    try:
        org_resp = client.organizations.create(
            organization_name=org_name,
            organization_slug=org_slug,
        )
        organization_id = org_resp.organization.organization_id
        print(f"Created organization with ID: {organization_id}")
    except Exception as e:
        print(f"Error creating organization: {e}")
        sys.exit(1)

    print("Creating SAML connection...")
    try:
        conn_resp = client.sso.saml.create_connection(
            organization_id=organization_id,
            display_name="SAML Connection",
        )
        connection_id = conn_resp.connection.connection_id
        print(f"Created SAML connection with ID: {connection_id}")
    except Exception as e:
        print(f"Error creating SAML connection: {e}")
        sys.exit(1)

    print("Updating SAML connection with IdP details...")
    try:
        update_resp = client.sso.saml.update_connection(
            organization_id=organization_id,
            connection_id=connection_id,
            idp_sso_url="https://idp.example.com/sso",
            idp_entity_id="https://idp.example.com/entity",
        )
        print("Successfully updated SAML connection.")
        print(f"Connection status: {update_resp.connection.status}")
    except Exception as e:
        print(f"Error updating SAML connection: {e}")
        sys.exit(1)

    print("SAML configuration complete.")

if __name__ == "__main__":
    main()
