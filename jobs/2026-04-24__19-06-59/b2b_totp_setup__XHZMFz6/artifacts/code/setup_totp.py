import os
import sys
import json
import stytch
import pyotp

# Setup logging
LOG_FILE = "/home/user/stytch_project/output.log"

def log(message):
    print(message)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(message + "\n")
    except Exception as e:
        print(f"Failed to write to log file: {e}")

def main():
    if len(sys.argv) < 3:
        log("Usage: python setup_totp.py <organization_id> <member_id>")
        sys.exit(1)

    organization_id = sys.argv[1]
    member_id = sys.argv[2]

    project_id = os.getenv("STYTCH_B2B_PROJECT_ID")
    secret_key = os.getenv("STYTCH_B2B_SECRET")

    if not project_id or not secret_key:
        log("STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET environment variables must be set")
        sys.exit(1)

    # Initialize Stytch B2B client
    # The SDK automatically determines the environment based on the project_id prefix (project-test- or project-live-)
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret_key
    )

    try:
        log(f"Creating TOTP for member {member_id} in organization {organization_id}...")
        # 3. Create a new TOTP instance
        create_resp = client.totps.create(
            organization_id=organization_id,
            member_id=member_id
        )
        
        # Extract the TOTP secret and other info
        totp_secret = create_resp.secret
        recovery_codes = create_resp.recovery_codes
        totp_registration_id = create_resp.totp_registration_id

        log(f"TOTP instance created. Registration ID: {totp_registration_id}")

        # 5. Generate a valid 6-digit TOTP code
        totp = pyotp.TOTP(totp_secret)
        code = totp.now()
        log(f"Generated TOTP code: {code}")

        # 6. Authenticate the TOTP instance
        log("Authenticating TOTP instance...")
        auth_resp = client.totps.authenticate(
            organization_id=organization_id,
            member_id=member_id,
            totp_code=code
        )

        log("TOTP authentication successful.")

        # 7. Write JSON file
        totp_info = {
            "totp_registration_id": totp_registration_id,
            "recovery_code": recovery_codes[0] if recovery_codes else None
        }

        info_path = "/home/user/stytch_project/totp_info.json"
        with open(info_path, "w") as f:
            json.dump(totp_info, f, indent=2)
        
        log(f"Saved TOTP info to {info_path}")

    except Exception as e:
        log(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
