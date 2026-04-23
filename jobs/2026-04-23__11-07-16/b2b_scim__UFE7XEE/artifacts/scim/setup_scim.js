"use strict";

/**
 * setup_scim.js
 *
 * Provisions a new Stytch B2B Organization and creates a SCIM connection for it.
 *
 * Required environment variables:
 *   STYTCH_PROJECT_ID  – your Stytch B2B project ID  (e.g. project-live-…)
 *   STYTCH_SECRET      – your Stytch B2B secret key   (e.g. secret-live-…)
 *
 * Output:
 *   /home/user/app/scim_output.json – contains organization_id, connection_id,
 *                                     base_url, and bearer_token
 */

const fs = require("fs");
const path = require("path");
const stytch = require("stytch");

// ── Validate environment variables ──────────────────────────────────────────
const PROJECT_ID = process.env.STYTCH_PROJECT_ID;
const SECRET = process.env.STYTCH_SECRET;

if (!PROJECT_ID || !SECRET) {
  console.error(
    "ERROR: Both STYTCH_PROJECT_ID and STYTCH_SECRET environment variables must be set."
  );
  process.exit(1);
}

// ── Stytch B2B client ───────────────────────────────────────────────────────
const client = new stytch.B2BClient({
  project_id: PROJECT_ID,
  secret: SECRET,
});

// ── Unique organisation slug based on current timestamp ─────────────────────
const timestamp = Date.now();
const orgSlug = `acme-scim-org-${timestamp}`;

// ── Output file path ─────────────────────────────────────────────────────────
const OUTPUT_PATH = path.join(__dirname, "scim_output.json");

async function main() {
  // ── Step 1: Create the B2B Organisation ─────────────────────────────────
  console.log(`Creating organization with slug "${orgSlug}" …`);
  let orgResponse;
  try {
    orgResponse = await client.organizations.create({
      organization_name: "Acme SCIM Org",
      organization_slug: orgSlug,
    });
  } catch (err) {
    console.error("Failed to create organization:", err?.error_message ?? err);
    process.exit(1);
  }

  const organization_id = orgResponse.organization.organization_id;
  console.log(`  ✓ Organization created  → organization_id: ${organization_id}`);

  // ── Step 2: Create the SCIM connection ───────────────────────────────────
  console.log("Creating SCIM connection …");
  let scimResponse;
  try {
    scimResponse = await client.scim.connection.create({
      organization_id,
      display_name: "Acme SCIM Connection",
      identity_provider: "okta",
    });
  } catch (err) {
    console.error("Failed to create SCIM connection:", err?.error_message ?? err);
    process.exit(1);
  }

  const { connection_id, base_url, bearer_token } = scimResponse.connection;
  console.log(`  ✓ SCIM connection created → connection_id: ${connection_id}`);

  // ── Step 3: Write output JSON ────────────────────────────────────────────
  const output = {
    organization_id,
    connection_id,
    base_url,
    bearer_token,
  };

  fs.writeFileSync(OUTPUT_PATH, JSON.stringify(output, null, 2), "utf8");
  console.log(`\nOutput written to ${OUTPUT_PATH}`);
  console.log(JSON.stringify(output, null, 2));
}

main();
