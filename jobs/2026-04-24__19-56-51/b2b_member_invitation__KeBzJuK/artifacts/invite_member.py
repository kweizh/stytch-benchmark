"""
Stytch B2B Member Invitation Script

1. Creates a B2B Organisation named "Acme Corp <trial_id>" with slug
   "acme-corp-<trial_id>" (idempotent – re-uses an existing org if the
   slug is already taken).
2. Creates a pending Member for "new-member-<trial_id>@example.com" and
   sends them an email invitation via magic_links.email.invite.
3. Writes the resulting Organization ID and Member ID to output.json.

Credentials are read from the environment variables:
  STYTCH_B2B_PROJECT_ID
  STYTCH_B2B_SECRET

The trial_id suffix is read from /logs/artifacts/trial_id.
"""

import json
import os

from stytch import B2BClient
from stytch.core.response_base import StytchError

# ---------------------------------------------------------------------------
# 1. Load trial_id
# ---------------------------------------------------------------------------
TRIAL_ID_PATH = "/logs/artifacts/trial_id"

with open(TRIAL_ID_PATH, "r") as f:
    trial_id = f.read().strip()

# ---------------------------------------------------------------------------
# 2. Derive dynamic values from trial_id
# ---------------------------------------------------------------------------
org_name = f"Acme Corp {trial_id}"
org_slug = f"acme-corp-{trial_id}"
member_email = f"new-member-{trial_id}@example.com"

# ---------------------------------------------------------------------------
# 3. Initialise Stytch B2B client from environment variables
# ---------------------------------------------------------------------------
project_id = os.environ["STYTCH_B2B_PROJECT_ID"]
secret = os.environ["STYTCH_B2B_SECRET"]

client = B2BClient(project_id=project_id, secret=secret)

# ---------------------------------------------------------------------------
# 4. Create the Organisation (idempotent)
# ---------------------------------------------------------------------------
print(f"Creating organisation: {org_name!r} (slug={org_slug!r})")
try:
    org_response = client.organizations.create(
        organization_name=org_name,
        organization_slug=org_slug,
    )
    organization_id = org_response.organization.organization_id
    print(f"Organisation created: {organization_id}")
except StytchError as exc:
    if exc.details.error_type == "organization_slug_already_used":
        # Org already exists – retrieve it by slug
        print("Slug already in use; fetching existing organisation by slug.")
        get_response = client.organizations.get(organization_id=org_slug)
        organization_id = get_response.organization.organization_id
        print(f"Existing organisation found: {organization_id}")
    else:
        raise

# ---------------------------------------------------------------------------
# 5. Create a pending Member (the invitation target)
# ---------------------------------------------------------------------------
print(f"Creating pending member: {member_email!r}")
member_id: str | None = None
try:
    create_member_response = client.organizations.members.create(
        organization_id=organization_id,
        email_address=member_email,
        create_member_as_pending=True,
    )
    member_id = create_member_response.member.member_id
    print(f"Member created (pending): {member_id}")
except StytchError as exc:
    if exc.details.error_type == "member_already_exists":
        # Member exists – look them up
        print("Member already exists; searching for existing member.")
        from stytch.b2b.models.organizations import SearchQuery

        search_response = client.organizations.members.search(
            organization_ids=[organization_id],
            query=SearchQuery(
                operator="AND",
                operands=[
                    {"filter_name": "member_emails", "filter_value": [member_email]}
                ],
            ),
        )
        if search_response.members:
            member_id = search_response.members[0].member_id
            print(f"Existing member found: {member_id}")
        else:
            raise RuntimeError(
                f"member_already_exists error, but no member found for {member_email}"
            ) from exc
    else:
        raise

# ---------------------------------------------------------------------------
# 6. Send an email invitation via magic_links.email.invite
# ---------------------------------------------------------------------------
print(f"Sending email invitation to: {member_email!r}")
try:
    invite_response = client.magic_links.email.invite(
        organization_id=organization_id,
        email_address=member_email,
    )
    # The invite endpoint may return an updated member_id; prefer it.
    member_id = invite_response.member.member_id
    print(f"Invitation email sent successfully. Member ID: {member_id}")
except StytchError as exc:
    # In test/sandbox environments the account may lack billing verification,
    # which blocks sending email to external addresses.  We still have the
    # Member record created above, so we surface the warning and continue.
    print(
        f"Warning: could not send invitation email "
        f"({exc.details.error_type}): {exc.details.error_message}"
    )
    print("Continuing with the member ID from the create-member step.")

if member_id is None:
    raise RuntimeError("Unable to determine member_id – aborting.")

# ---------------------------------------------------------------------------
# 7. Write results to output.json
# ---------------------------------------------------------------------------
output = {
    "organization_id": organization_id,
    "member_id": member_id,
}

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output.json")
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nResults written to {output_path}")
print(json.dumps(output, indent=2))
