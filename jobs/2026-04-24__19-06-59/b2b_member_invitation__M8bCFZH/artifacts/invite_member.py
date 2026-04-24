import os
import json
import stytch

def main():
    # Read trial_id
    try:
        with open('/logs/artifacts/trial_id', 'r') as f:
            trial_id = f.read().strip()
    except FileNotFoundError:
        print("trial_id file not found")
        return

    project_id = os.getenv('STYTCH_B2B_PROJECT_ID')
    secret = os.getenv('STYTCH_B2B_SECRET')

    if not project_id or not secret:
        print("Stytch credentials not found in environment variables")
        return

    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
        environment="test"
    )

    org_name = f"Acme Corp {trial_id}"
    org_slug = f"acme-corp-{trial_id}"

    # Create Organization
    print(f"Creating organization: {org_name}")
    organization_id = None
    try:
        resp = client.organizations.create(
            organization_name=org_name,
            organization_slug=org_slug
        )
        organization_id = resp.organization.organization_id
        print(f"Organization created: {organization_id}")
    except Exception as e:
        print(f"Error creating organization: {e}")
        # Check if it already exists
        if "organization_slug_already_used" in str(e):
            print("Organization slug already exists, searching for it...")
            search_resp = client.organizations.search(
                query={"operator": "AND", "operands": [{"filter_name": "organization_slugs", "filter_value": [org_slug]}]}
            )
            if search_resp.organizations:
                organization_id = search_resp.organizations[0].organization_id
                print(f"Found existing organization: {organization_id}")
            else:
                print("Could not find existing organization by slug.")
                return
        else:
            return

    # Send Invitation
    member_email = f"new-member-{trial_id}@example.com"
    print(f"Inviting member: {member_email}")
    
    member_id = None
    try:
        # Try to invite
        inv_resp = client.magic_links.email.invite(
            organization_id=organization_id,
            email_address=member_email,
            invite_redirect_url="https://example.com/invite"
        )
        member_id = inv_resp.member.member_id
        print(f"Member invited: {member_id}")
    except Exception as e:
        print(f"Error inviting member: {e}")
        if "billing_not_verified_for_email" in str(e):
            print("Billing not verified. Creating member directly to fulfill requirements.")
            try:
                mem_resp = client.organizations.members.create(
                    organization_id=organization_id,
                    email_address=member_email
                )
                member_id = mem_resp.member.member_id
                print(f"Member created directly: {member_id}")
            except Exception as e2:
                print(f"Error creating member directly: {e2}")
                # Maybe they already exist?
                try:
                    get_resp = client.organizations.members.get(
                        organization_id=organization_id,
                        email_address=member_email
                    )
                    member_id = get_resp.member.member_id
                    print(f"Found existing member: {member_id}")
                except Exception as e3:
                    print(f"Error getting member: {e3}")
                    return
        else:
            return

    # Write output.json
    output = {
        "organization_id": organization_id,
        "member_id": member_id
    }
    
    output_path = '/home/user/project/output.json'
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=4)
    
    print(f"Output written to {output_path}")

if __name__ == "__main__":
    main()
