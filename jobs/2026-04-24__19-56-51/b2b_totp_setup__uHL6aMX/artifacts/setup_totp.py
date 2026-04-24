#!/usr/bin/env python3
"""
Stytch B2B TOTP Setup Script

Usage:
    python setup_totp.py <organization_id> <member_id>

Environment Variables:
    STYTCH_B2B_PROJECT_ID  - Stytch B2B project ID
    STYTCH_B2B_SECRET      - Stytch B2B secret key
"""

import argparse
import json
import logging
import os
import sys

import pyotp
import stytch

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/home/user/stytch_project/output.log"),
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger(__name__)

TOTP_INFO_PATH = "/home/user/stytch_project/totp_info.json"


def parse_args():
    parser = argparse.ArgumentParser(description="Set up TOTP for a Stytch B2B member.")
    parser.add_argument("organization_id", help="The Stytch B2B organization ID.")
    parser.add_argument("member_id", help="The Stytch B2B member ID.")
    return parser.parse_args()


def main():
    args = parse_args()
    organization_id = args.organization_id
    member_id = args.member_id

    # Read credentials from environment
    project_id = os.environ.get("STYTCH_B2B_PROJECT_ID")
    secret = os.environ.get("STYTCH_B2B_SECRET")

    if not project_id or not secret:
        logger.error(
            "Missing required environment variables: "
            "STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET must be set."
        )
        sys.exit(1)

    logger.info("Initializing Stytch B2B client.")
    client = stytch.B2BClient(
        project_id=project_id,
        secret=secret,
    )

    # Step 1: Create a new TOTP instance for the member
    logger.info(
        "Creating TOTP instance for member_id=%s in organization_id=%s.",
        member_id,
        organization_id,
    )
    create_response = client.totps.create(
        organization_id=organization_id,
        member_id=member_id,
    )
    logger.info(
        "TOTP created successfully. totp_registration_id=%s",
        create_response.totp_registration_id,
    )

    totp_secret = create_response.secret
    totp_registration_id = create_response.totp_registration_id
    recovery_codes = create_response.recovery_codes

    # Step 2: Generate the current TOTP code using pyotp
    logger.info("Generating TOTP code using pyotp.")
    totp_code = pyotp.TOTP(totp_secret).now()
    logger.info("Generated TOTP code: %s", totp_code)

    # Step 3: Authenticate the TOTP instance to complete enrollment
    logger.info("Authenticating TOTP instance to complete enrollment.")
    client.totps.authenticate(
        organization_id=organization_id,
        member_id=member_id,
        code=totp_code,
    )
    logger.info("TOTP authenticated successfully.")

    # Step 4: Write TOTP info to JSON file
    first_recovery_code = recovery_codes[0]
    totp_info = {
        "totp_registration_id": totp_registration_id,
        "recovery_code": first_recovery_code,
    }

    with open(TOTP_INFO_PATH, "w") as f:
        json.dump(totp_info, f, indent=2)
    logger.info("TOTP info written to %s.", TOTP_INFO_PATH)

    print(json.dumps(totp_info, indent=2))


if __name__ == "__main__":
    main()
