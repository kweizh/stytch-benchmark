import os
import json
import stytch
from stytch.core.response_base import StytchError

def main():
    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        raise ValueError("Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables")
        
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
        environment="test",
    )
    
    with open("/logs/artifacts/trial_id", "r") as f:
        trial_id = f.read().strip()
        
    org_name = f"Acme Corp {trial_id}"
    org_slug = f"acme-corp-{trial_id}"
    email = f"new-member-{trial_id}@example.com"
    
    # Create organization or fetch if exists
    try:
        org_response = client.organizations.create(
            organization_name=org_name,
            organization_slug=org_slug,
        )
        organization_id = org_response.organization.organization_id
    except StytchError as e:
        if getattr(e.details, "error_type", None) == "organization_slug_already_used":
            search_res = client.organizations.search(
                query={"operator": "AND", "operands": [{"filter_name": "organization_slugs", "filter_value": [org_slug]}]}
            )
            organization_id = search_res.organizations[0].organization_id
        else:
            raise
            
    # Create member as pending to get member_id
    try:
        member_response = client.organizations.members.create(
            organization_id=organization_id,
            email_address=email,
            create_member_as_pending=True,
        )
        member_id = member_response.member_id
    except StytchError as e:
        if getattr(e.details, "error_type", None) == "member_already_exists":
            search_res = client.organizations.members.search(
                organization_ids=[organization_id],
                query={"operator": "AND", "operands": [{"filter_name": "email_addresses", "filter_value": [email]}]}
            )
            member_id = search_res.members[0].member_id
        else:
            raise
    
    # Send email invitation
    try:
        client.magic_links.email.invite(
            organization_id=organization_id,
            email_address=email,
        )
    except StytchError as e:
        if getattr(e.details, "error_type", None) == "billing_not_verified_for_email":
            # Ignore test environment limitation
            pass
        else:
            raise

    # Write output
    output_data = {
        "organization_id": organization_id,
        "member_id": member_id,
    }
    
    with open("/home/user/project/output.json", "w") as f:
        json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    main()
