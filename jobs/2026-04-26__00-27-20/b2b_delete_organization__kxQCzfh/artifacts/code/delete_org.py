import os
import sys
import stytch

def main():
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("Missing Stytch credentials (STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET)")
        sys.exit(1)

    try:
        with open("/logs/org_id.txt", "r") as f:
            org_id = f.read().strip()
    except FileNotFoundError:
        print("File /logs/org_id.txt not found")
        sys.exit(1)

    if not org_id:
        print("No organization ID found in /logs/org_id.txt")
        sys.exit(1)

    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )

    try:
        response = client.organizations.delete(organization_id=org_id)
        if response.status_code == 200:
            with open("/home/user/project/output.log", "w") as f:
                f.write(org_id)
            print(f"Successfully deleted organization {org_id}")
        else:
            print(f"Failed to delete organization {org_id}: {response}")
            sys.exit(1)
    except Exception as e:
        print(f"Error deleting organization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
