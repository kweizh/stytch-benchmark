const stytch = require('stytch');
const fs = require('fs');
const path = require('path');

async function setupSCIM() {
  const client = new stytch.B2BClient({
    project_id: process.env.STYTCH_PROJECT_ID,
    secret: process.env.STYTCH_SECRET,
  });

  const timestamp = Date.now();
  const organizationName = "Acme SCIM Org";
  const organizationSlug = `acme-scim-org-${timestamp}`;

  try {
    console.log(`Creating organization: ${organizationName} (${organizationSlug})...`);
    const orgResponse = await client.organizations.create({
      organization_name: organizationName,
      organization_slug: organizationSlug,
    });

    const organization_id = orgResponse.organization.organization_id;
    console.log(`Organization created: ${organization_id}`);

    console.log(`Creating SCIM connection for organization: ${organization_id}...`);
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
      bearer_token: scimResponse.bearer_token,
    };

    const outputPath = path.join(__dirname, 'scim_output.json');
    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
    console.log(`SCIM configuration saved to ${outputPath}`);

  } catch (error) {
    console.error('Error setting up SCIM:', error);
    process.exit(1);
  }
}

setupSCIM();
