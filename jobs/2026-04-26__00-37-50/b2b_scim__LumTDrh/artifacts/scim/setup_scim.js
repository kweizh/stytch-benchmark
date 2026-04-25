"use strict";

/**
 * setup_scim.js
 *
 * Provisions a new Stytch B2B Organization and creates a SCIM connection for it.
 * Writes the key connection details to scim_output.json.
 *
 * Required environment variables:
 *   STYTCH_PROJECT_ID  – Your Stytch B2B project ID  (e.g. project-live-xxxx)
 *   STYTCH_SECRET      – Your Stytch B2B project secret
 */

const stytch = require("stytch");
const fs = require("fs");
const path = require("path");

// ---------------------------------------------------------------------------
// Validate environment variables up-front so errors are clear.
// ---------------------------------------------------------------------------
const { STYTCH_PROJECT_ID, STYTCH_SECRET } = process.env;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  console.error(
    "[ERROR] Both STYTCH_PROJECT_ID and STYTCH_SECRET environment variables must be set."
  );
  process.exit(1);
}

// ---------------------------------------------------------------------------
// Initialise the Stytch B2B client.
// ---------------------------------------------------------------------------
const client = new stytch.B2BClient({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
});

// ---------------------------------------------------------------------------
// Helper: produce a unique org slug using the current Unix timestamp (ms).
// ---------------------------------------------------------------------------
function uniqueSlug() {
  return `acme-scim-org-${Date.now()}`;
}

// ---------------------------------------------------------------------------
// Main provisioning flow.
// ---------------------------------------------------------------------------
async function main() {
  const slug = uniqueSlug();

  // 1. Create the organization.
  console.log(`[1/2] Creating organization with slug "${slug}" …`);
  let orgResponse;
  try {
    orgResponse = await client.organizations.create({
      organization_name: "Acme SCIM Org",
      organization_slug: slug,
    });
  } catch (err) {
    console.error("[ERROR] Failed to create organization:", err);
    process.exit(1);
  }

  const organization = orgResponse.organization;
  const organization_id = organization.organization_id;
  console.log(`       ✓ Organization created  (id: ${organization_id})`);

  // 2. Create the SCIM connection for the new organization.
  console.log(`[2/2] Creating SCIM connection for organization ${organization_id} …`);
  let scimResponse;
  try {
    scimResponse = await client.scim.connection.create({
      organization_id,
      display_name: "Acme SCIM Connection",
      identity_provider: "okta",
    });
  } catch (err) {
    console.error("[ERROR] Failed to create SCIM connection:", err);
    process.exit(1);
  }

  // The create endpoint returns a SCIMConnectionWithToken object, which is the
  // only time the full bearer_token is exposed by the API.
  const connection = scimResponse.connection;
  const { connection_id, base_url, bearer_token } = connection;
  console.log(`       ✓ SCIM connection created (id: ${connection_id})`);

  // 3. Write results to scim_output.json.
  const output = {
    organization_id,
    connection_id,
    base_url,
    bearer_token,
  };

  const outputPath = path.join(__dirname, "scim_output.json");
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
  console.log(`\n✅  Output written to ${outputPath}`);
  console.log(JSON.stringify(output, null, 2));
}

main();
