const stytch = require('stytch');
const fs = require('fs');
const path = require('path');

if (!process.env.STYTCH_PROJECT_ID || !process.env.STYTCH_SECRET) {
  console.error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.");
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

async function run() {
  try {
    const timestamp = Date.now();
    const organizationName = "Acme SCIM Org";
    const organizationSlug = `acme-scim-org-${timestamp}`;

    console.log(`Creating organization: ${organizationName} (${organizationSlug})...`);
    const orgResponse = await client.organizations.create({
      organization_name: organizationName,
      organization_slug: organizationSlug,
    });

    const organizationId = orgResponse.organization.organization_id;
    console.log(`Organization created with ID: ${organizationId}`);

    console.log(`Creating SCIM connection for organization: ${organizationId}...`);
    const scimResponse = await client.scim.connection.create({
      organization_id: organizationId,
      display_name: "Acme SCIM Connection",
      identity_provider: "okta",
    });

    const connection = scimResponse.connection;
    const output = {
      organization_id: organizationId,
      connection_id: connection.connection_id,
      base_url: connection.base_url,
      bearer_token: connection.bearer_token,
    };

    const outputPath = path.join(__dirname, 'scim_output.json');
    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
    console.log(`SCIM connection details saved to ${outputPath}`);

  } catch (error) {
    console.error("Error setting up SCIM:", error);
    process.exit(1);
  }
}

run();
