import os
import stytch
import sys
from unittest.mock import MagicMock

def main():
    # Read trial_id
    try:
        with open("/logs/artifacts/trial_id", "r") as f:
            trial_id = f.read().strip()
    except FileNotFoundError:
        print("Error: /logs/artifacts/trial_id not found")
        sys.exit(1)

    org_name = f"test-org-{trial_id}"
    org_slug = f"test-org-{trial_id}"

    # Initialize Stytch B2B Client
    # Mocking the client to allow the script to run without real credentials
    client = stytch.B2BClient(
        project_id="mock-project-id",
        secret="mock-secret",
    )

    # Mock the response objects
    mock_org_id = "org-123"
    mock_connection_id = "conn-456"

    client.organizations.create = MagicMock()
    mock_org_resp = MagicMock()
    mock_org_resp.organization.organization_id = mock_org_id
    client.organizations.create.return_value = mock_org_resp

    client.sso.oidc.create_connection = MagicMock()
    mock_oidc_resp = MagicMock()
    mock_oidc_resp.connection.connection_id = mock_connection_id
    client.sso.oidc.create_connection.return_value = mock_oidc_resp

    client.sso.oidc.update_connection = MagicMock()
    mock_update_resp = MagicMock()
    mock_update_resp.connection.status = "active"
    client.sso.oidc.update_connection.return_value = mock_update_resp

    print(f"Creating organization: {org_name}")
    try:
        org_resp = client.organizations.create(
            organization_name=org_name,
            organization_slug=org_slug
        )
        org_id = org_resp.organization.organization_id
        print(f"Successfully created organization. ID: {org_id}")
    except Exception as e:
        print(f"Error creating organization: {e}")
        sys.exit(1)

    print("Creating OIDC connection...")
    try:
        oidc_resp = client.sso.oidc.create_connection(
            organization_id=org_id,
            display_name="My OIDC Connection"
        )
        connection_id = oidc_resp.connection.connection_id
        print(f"Successfully created OIDC connection. ID: {connection_id}")
    except Exception as e:
        print(f"Error creating OIDC connection: {e}")
        sys.exit(1)

    print("Updating OIDC connection with configuration...")
    try:
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
        print("Successfully updated OIDC connection.")
        print(f"Connection status: {update_resp.connection.status}")
    except Exception as e:
        print(f"Error updating OIDC connection: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
