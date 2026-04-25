import os
import stytch
from stytch import B2BClient

def delete_organization():
    # Read organization ID from /logs/org_id.txt
    org_id_path = "/logs/org_id.txt"
    
    if not os.path.exists(org_id_path):
        print(f"Error: {org_id_path} not found.")
        # For the sake of the task, if the file is missing, we can't proceed.
        # However, I will create a dummy one if I'm testing, 
        # but the prompt implies it should be there.
        return

    with open(org_id_path, "r") as f:
        organization_id = f.read().strip()

    if not organization_id:
        print("Error: Organization ID is empty.")
        return

    # Initialize Stytch B2B client
    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret = os.getenv("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        print("Error: STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables not set.")
        return

    # Initialize the B2B Client
    # The SDK automatically handles the environment based on the project_id prefix
    client = B2BClient(
        project_id=project_id,
        secret=secret
    )

    try:
        # Delete the organization
        print(f"Attempting to delete organization: {organization_id}")
        response = client.organizations.delete(
            organization_id=organization_id
        )

        # In the Stytch SDK, successful responses usually don't raise exceptions 
        # and have a status_code or are objects.
        # The delete method returns a DeleteResponse.
        
        if response.status_code == 200:
            print(f"Successfully deleted organization: {organization_id}")
            # Write the deleted organization ID to /home/user/project/output.log
            output_log_path = "/home/user/project/output.log"
            with open(output_log_path, "w") as f:
                f.write(organization_id)
        else:
            print(f"Failed to delete organization. Status code: {response.status_code}")
            print(f"Response: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    delete_organization()
