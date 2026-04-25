const stytch = require('stytch');
const fs = require('fs');
const path = require('path');

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

async function run() {
  try {
    const timestamp = Date.now();
    const slug = `acme-scim-org-${timestamp}`;

    const orgResponse = await client.organizations.create({
      organization_name: "Acme SCIM Org",
      organization_slug: slug,
    });

    const organization_id = orgResponse.organization.organization_id;

    const scimResponse = await client.scim.connection.create({
      organization_id: organization_id,
      display_name: "Acme SCIM Connection",
      identity_provider: "okta",
    });

    const connection = scimResponse.connection;

    const output = {
      organization_id: organization_id,
      connection_id: connection.connection_id,
      base_url: connection.base_url,
      bearer_token: connection.bearer_token,
    };

    fs.writeFileSync(
      path.join(__dirname, 'scim_output.json'),
      JSON.stringify(output, null, 2)
    );

    console.log("SCIM setup completed successfully.");
  } catch (error) {
    console.error("Error setting up SCIM:", error);
    process.exit(1);
  }
}

run();
