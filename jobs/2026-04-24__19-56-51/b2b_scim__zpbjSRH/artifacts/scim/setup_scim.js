"use strict";

/**
 * setup_scim.js
 *
 * Provisions a new Stytch B2B Organization and creates a SCIM connection for it.
 *
 * Required environment variables:
 *   STYTCH_PROJECT_ID  – your Stytch B2B project ID  (e.g. project-test-…)
 *   STYTCH_SECRET      – your Stytch B2B secret key  (e.g. secret-test-…)
 *
 * Output:
 *   /home/user/app/scim_output.json  – organization_id, connection_id, base_url, bearer_token
 */

const fs = require("fs");
const path = require("path");
const stytch = require("stytch");

// ---------------------------------------------------------------------------
// Validate environment variables early so errors are clear.
// ---------------------------------------------------------------------------
const PROJECT_ID = process.env.STYTCH_PROJECT_ID;
const SECRET = process.env.STYTCH_SECRET;

if (!PROJECT_ID || !SECRET) {
  console.error(
    "Error: STYTCH_PROJECT_ID and STYTCH_SECRET environment variables must be set."
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Build a unique slug using the current Unix timestamp (milliseconds).
// ---------------------------------------------------------------------------
const timestamp = Date.now();
const orgSlug = `acme-scim-org-${timestamp}`;

// ---------------------------------------------------------------------------
// Instantiate the Stytch B2B client.
// ---------------------------------------------------------------------------
const client = new stytch.B2BClient({
  project_id: PROJECT_ID,
  secret: SECRET,
});

async function main() {
  // -------------------------------------------------------------------------
  // Step 1 – Create the organization.
  // -------------------------------------------------------------------------
  console.log(`Creating organization with slug "${orgSlug}"…`);

  let orgResponse;
  try {
    orgResponse = await client.organizations.create({
      organization_name: "Acme SCIM Org",
      organization_slug: orgSlug,
    });
  } catch (err) {
    console.error("Failed to create organization:", err);
    process.exit(1);
  }

  const organizationId = orgResponse.organization.organization_id;
  console.log(`✓ Organization created: ${organizationId}`);

  // -------------------------------------------------------------------------
  // Step 2 – Create the SCIM connection for this organization.
  // -------------------------------------------------------------------------
  console.log("Creating SCIM connection…");

  let scimResponse;
  try {
    scimResponse = await client.scim.connection.create({
      organization_id: organizationId,
      display_name: "Acme SCIM Connection",
      identity_provider: "okta",
    });
  } catch (err) {
    console.error("Failed to create SCIM connection:", err);
    process.exit(1);
  }

  const connection = scimResponse.connection;
  const connectionId = connection.connection_id;
  const baseUrl = connection.base_url;
  const bearerToken = connection.bearer_token;

  console.log(`✓ SCIM connection created: ${connectionId}`);
  console.log(`  Base URL     : ${baseUrl}`);
  console.log(`  Bearer token : ${bearerToken}`);

  // -------------------------------------------------------------------------
  // Step 3 – Write results to scim_output.json.
  // -------------------------------------------------------------------------
  const output = {
    organization_id: organizationId,
    connection_id: connectionId,
    base_url: baseUrl,
    bearer_token: bearerToken,
  };

  const outputPath = path.join(__dirname, "scim_output.json");
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2), "utf8");
  console.log(`\n✓ Output written to ${outputPath}`);
  console.log(JSON.stringify(output, null, 2));
}

main();
