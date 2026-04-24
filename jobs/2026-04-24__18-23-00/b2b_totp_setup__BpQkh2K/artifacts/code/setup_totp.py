import sys
import os
import json
import stytch
import pyotp

def main():
    if len(sys.argv) != 3:
        print("Usage: python setup_totp.py <organization_id> <member_id>")
        sys.exit(1)
        
    organization_id = sys.argv[1]
    member_id = sys.argv[2]
    
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")
    
    if not project_id or not secret:
        print("STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET must be set")
        sys.exit(1)
        
    client = stytch.B2BClient(project_id=project_id, secret=secret)
    
    # 3. Create a new TOTP instance for the member using the Stytch B2B API.
    create_resp = client.totps.create(
        organization_id=organization_id,
        member_id=member_id
    )
    
    # 4. Extract the TOTP secret from the response.
    totp_secret = create_resp.secret
    totp_registration_id = create_resp.totp_registration_id
    recovery_code = create_resp.recovery_codes[0] if create_resp.recovery_codes else None
    
    # 5. Use the pyotp library to generate a valid 6-digit TOTP code based on the secret.
    totp = pyotp.TOTP(totp_secret)
    code = totp.now()
    
    # 6. Authenticate the TOTP instance using the generated code to complete the enrollment process.
    auth_resp = client.totps.authenticate(
        organization_id=organization_id,
        member_id=member_id,
        code=code
    )
    
    # 7. Write a JSON file to /home/user/stytch_project/totp_info.json containing the totp_registration_id and the first recovery code.
    output_data = {
        "totp_registration_id": totp_registration_id,
        "recovery_code": recovery_code
    }
    
    with open("/home/user/stytch_project/totp_info.json", "w") as f:
        json.dump(output_data, f, indent=2)
        
    print("TOTP setup complete.")

if __name__ == "__main__":
    main()
