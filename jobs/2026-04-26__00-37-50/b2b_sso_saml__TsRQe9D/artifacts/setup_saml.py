#!/usr/bin/env python3
"""
Script to create a Stytch B2B organization and configure a SAML connection.
"""

import os
import stytch

# Read trial_id
with open("/logs/artifacts/trial_id", "r") as f:
    trial_id = f.read().strip()

print(f"Trial ID: {trial_id}")

# Read credentials from environment variables
project_id = os.environ["STYTCH_B2B_PROJECT_ID"]
secret = os.environ["STYTCH_B2B_SECRET"]

# Initialize Stytch B2B client
client = stytch.B2BClient(project_id=project_id, secret=secret)

# 1. Create a new B2B organization
org_name = f"SAML Org {trial_id}"
org_slug = f"saml-org-{trial_id}"

print(f"\nCreating organization: name='{org_name}', slug='{org_slug}'")
org_response = client.organizations.create(
    organization_name=org_name,
    organization_slug=org_slug,
)
print(f"Organization created: {org_response.organization.organization_id}")
organization_id = org_response.organization.organization_id

# 2. Create a SAML connection for the organization
print(f"\nCreating SAML connection for organization: {organization_id}")
saml_create_response = client.sso.saml.create_connection(
    organization_id=organization_id,
    display_name="SAML Connection",
)
print(f"SAML connection created: {saml_create_response.connection.connection_id}")
connection_id = saml_create_response.connection.connection_id

# 3. Update the SAML connection with IdP SSO URL and IdP entity ID
idp_sso_url = "https://idp.example.com/sso"
idp_entity_id = "https://idp.example.com/entity"

print(f"\nUpdating SAML connection with IdP SSO URL='{idp_sso_url}' and IdP Entity ID='{idp_entity_id}'")
saml_update_response = client.sso.saml.update_connection(
    organization_id=organization_id,
    connection_id=connection_id,
    idp_sso_url=idp_sso_url,
    idp_entity_id=idp_entity_id,
)
print(f"SAML connection updated: {saml_update_response.connection.connection_id}")
print(f"  IdP SSO URL: {saml_update_response.connection.idp_sso_url}")
print(f"  IdP Entity ID: {saml_update_response.connection.idp_entity_id}")

print("\nDone! SAML connection configured successfully.")
