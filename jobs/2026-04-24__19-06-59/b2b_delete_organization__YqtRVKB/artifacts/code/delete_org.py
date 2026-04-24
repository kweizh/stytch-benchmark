import os
import stytch

def main():
    # Load environment variables
    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        print("Error: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET environment variables must be set.")
        return

    # Initialize Stytch B2B client
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )

    # Read organization ID from file
    try:
        with open("/logs/org_id.txt", "r") as f:
            org_id = f.read().strip()
    except FileNotFoundError:
        print("Error: /logs/org_id.txt not found.")
        return

    if not org_id:
        print("Error: Organization ID in /logs/org_id.txt is empty.")
        return

    print(f"Attempting to delete organization: {org_id}")

    # Delete the organization
    try:
        response = client.organizations.delete(
            organization_id=org_id
        )
        
        # Check if the deletion was successful
        # The SDK usually returns a response object with status_code
        if response.status_code == 200:
            print(f"Successfully deleted organization: {org_id}")
            
            # Write the deleted organization ID to output.log
            with open("/home/user/project/output.log", "w") as f:
                f.write(org_id)
        else:
            print(f"Failed to delete organization. Status code: {response.status_code}")
            print(f"Response: {response}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
