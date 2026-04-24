#!/usr/bin/env node
"use strict";

const stytch = require("stytch");

async function main() {
  // Read telemetry_id from the first CLI argument
  const telemetryId = process.argv[2];

  if (!telemetryId) {
    console.error("Usage: node login.js <telemetry_id>");
    process.exit(1);
  }

  // Read credentials from environment variables
  const projectId = process.env.STYTCH_B2B_PROJECT_ID;
  const secret = process.env.STYTCH_B2B_SECRET;

  if (!projectId || !secret) {
    console.error(
      "Error: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET environment variables must be set."
    );
    process.exit(1);
  }

  // Initialize the Stytch B2B client
  const client = new stytch.B2BClient({
    project_id: projectId,
    secret: secret,
  });

  let verdict;

  try {
    // Call the Device Fingerprinting Lookup API
    const response = await client.fraud.fingerprint.lookup({
      telemetry_id: telemetryId,
    });

    verdict = response.verdict && response.verdict.action;
  } catch (err) {
    // If the telemetry_id is not found (404) or any other API error, treat as BLOCK
    // per Stytch's recommendation: 404 errors should be treated as BLOCK
    // since it could indicate an attacker trying to bypass DFP protections.
    const statusCode =
      err.status_code || (err.response && err.response.status);

    if (statusCode === 404) {
      console.error(
        "Error: telemetry_id not found or expired. Treating as BLOCK."
      );
    } else {
      console.error(
        "Error: Failed to look up fingerprint:",
        err.error_message || err.message || err
      );
    }

    console.log("Access Denied: Blocked");
    process.exit(1);
  }

  // Evaluate the verdict and respond accordingly
  switch (verdict) {
    case "BLOCK":
      console.log("Access Denied: Blocked");
      process.exit(1);
      break;

    case "CHALLENGE":
      console.log("MFA Required");
      process.exit(1);
      break;

    case "ALLOW":
      console.log("Login Successful");
      process.exit(0);
      break;

    default:
      // Unknown or missing verdict — deny by default
      console.error(
        `Error: Unknown verdict action "${verdict}". Denying access.`
      );
      console.log("Access Denied: Blocked");
      process.exit(1);
  }
}

main();
