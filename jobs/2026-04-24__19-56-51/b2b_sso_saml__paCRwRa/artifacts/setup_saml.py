#!/usr/bin/env python3
"""
Script to create a B2B organization and configure a SAML connection using the Stytch B2B API.
"""

import os
import sys

import stytch


def read_trial_id(path: str = "/logs/artifacts/trial_id") -> str:
    with open(path, "r") as f:
        return f.read().strip()


def main():
    # Read trial_id
    trial_id = read_trial_id()
    print(f"Trial ID: {trial_id}")

    # Read credentials from environment variables
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        print("ERROR: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET must be set.")
        sys.exit(1)

    # Initialize the Stytch B2B client
    client = stytch.B2BClient(project_id=project_id, secret=secret)

    # -------------------------------------------------------------------------
    # Step 1: Create the B2B organization
    # -------------------------------------------------------------------------
    org_name = f"SAML Org {trial_id}"
    org_slug = f"saml-org-{trial_id}"

    print(f"\nCreating organization: name='{org_name}', slug='{org_slug}' ...")
    org_response = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug,
    )
    organization = org_response.organization
    organization_id = organization.organization_id
    print(f"Organization created successfully. organization_id={organization_id}")

    # -------------------------------------------------------------------------
    # Step 2: Create a SAML connection for the organization
    # -------------------------------------------------------------------------
    print(f"\nCreating SAML connection for organization_id={organization_id} ...")
    create_response = client.sso.saml.create_connection(
        organization_id=organization_id,
    )
    connection = create_response.connection
    connection_id = connection.connection_id
    print(f"SAML connection created successfully. connection_id={connection_id}")

    # -------------------------------------------------------------------------
    # Step 3: Update the SAML connection with IdP details
    # -------------------------------------------------------------------------
    idp_sso_url = "https://idp.example.com/sso"
    idp_entity_id = "https://idp.example.com/entity"

    print(f"\nUpdating SAML connection with idp_sso_url='{idp_sso_url}' and idp_entity_id='{idp_entity_id}' ...")
    update_response = client.sso.saml.update_connection(
        organization_id=organization_id,
        connection_id=connection_id,
        idp_sso_url=idp_sso_url,
        idp_entity_id=idp_entity_id,
    )
    updated_connection = update_response.connection
    print(f"SAML connection updated successfully.")
    print(f"  connection_id : {updated_connection.connection_id}")
    print(f"  idp_sso_url   : {updated_connection.idp_sso_url}")
    print(f"  idp_entity_id : {updated_connection.idp_entity_id}")
    print(f"  status        : {updated_connection.status}")

    print("\nSetup complete!")
    return {
        "organization_id": organization_id,
        "connection_id": connection_id,
    }


if __name__ == "__main__":
    main()
