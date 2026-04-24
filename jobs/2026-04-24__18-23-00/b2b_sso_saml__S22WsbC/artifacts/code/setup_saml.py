import os
import stytch

def main():
    try:
        with open('/logs/trial_id', 'r') as f:
            trial_id = f.read().strip()
    except FileNotFoundError:
        with open('/logs/artifacts/trial_id', 'r') as f:
            trial_id = f.read().strip()

    client = stytch.B2BClient(
        project_id=os.environ["STYTCH_B2B_PROJECT_ID"],
        secret=os.environ["STYTCH_B2B_SECRET"],
    )

    print(f"Creating organization for trial_id: {trial_id}")
    org_resp = client.organizations.create(
        organization_name=f"SAML Org {trial_id}",
        organization_slug=f"saml-org-{trial_id}",
    )
    org_id = org_resp.organization.organization_id
    print(f"Created organization: {org_id}")

    saml_resp = client.sso.saml.create_connection(
        organization_id=org_id,
        display_name="My SAML Connection"
    )
    connection_id = saml_resp.connection.connection_id
    print(f"Created SAML connection: {connection_id}")

    update_resp = client.sso.saml.update_connection(
        organization_id=org_id,
        connection_id=connection_id,
        idp_sso_url="https://idp.example.com/sso",
        idp_entity_id="https://idp.example.com/entity"
    )
    print("Updated SAML connection successfully.")

if __name__ == "__main__":
    main()
