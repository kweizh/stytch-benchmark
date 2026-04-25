"use strict";

const { B2BClient } = require("stytch");

const telemetry_id = process.argv[2];

if (!telemetry_id) {
  console.error("Usage: node login.js <telemetry_id>");
  process.exit(1);
}

const projectId = process.env.STYTCH_B2B_PROJECT_ID;
const secret = process.env.STYTCH_B2B_SECRET;

if (!projectId || !secret) {
  console.error(
    "Error: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET environment variables must be set."
  );
  process.exit(1);
}

const client = new B2BClient({
  project_id: projectId,
  secret: secret,
});

async function main() {
  try {
    const response = await client.fraud.fingerprint.lookup({ telemetry_id });

    const action = response?.verdict?.action;

    if (action === "BLOCK") {
      console.log("Access Denied: Blocked");
      process.exit(1);
    } else if (action === "CHALLENGE") {
      console.log("MFA Required");
      process.exit(1);
    } else if (action === "ALLOW") {
      console.log("Login Successful");
      process.exit(0);
    } else {
      console.error(`Unexpected verdict action: ${action}`);
      process.exit(1);
    }
  } catch (err) {
    // Handle Stytch API errors (e.g., telemetry_id not found / expired → treat as BLOCK)
    if (err?.status_code === 404 || err?.error_type === "telemetry_id_not_found") {
      console.log("Access Denied: Blocked");
      process.exit(1);
    }

    console.error("Error calling Stytch Fingerprint API:", err?.message ?? err);
    process.exit(1);
  }
}

main();
