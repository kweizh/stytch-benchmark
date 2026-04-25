#!/usr/bin/env node

const stytch = require("stytch");

const telemetryId = process.argv[2];

if (!telemetryId) {
  console.error("Missing telemetry_id argument.");
  process.exit(1);
}

const projectId = process.env.STYTCH_B2B_PROJECT_ID;
const secret = process.env.STYTCH_B2B_SECRET;

if (!projectId || !secret) {
  console.error("Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables.");
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: projectId,
  secret,
  env: stytch.envs.test,
});

async function run() {
  try {
    const response = await client.fraud.fingerprints.lookup({
      telemetry_id: telemetryId,
    });

    const action = response?.verdict?.action;

    if (action === "BLOCK") {
      console.log("Access Denied: Blocked");
      process.exit(1);
    }

    if (action === "CHALLENGE") {
      console.log("MFA Required");
      process.exit(1);
    }

    if (action === "ALLOW") {
      console.log("Login Successful");
      process.exit(0);
    }

    console.error("Unexpected verdict action.");
    process.exit(1);
  } catch (error) {
    const message = error?.message || "Unknown error";
    console.error(`Fingerprint lookup failed: ${message}`);
    process.exit(1);
  }
}

run();
