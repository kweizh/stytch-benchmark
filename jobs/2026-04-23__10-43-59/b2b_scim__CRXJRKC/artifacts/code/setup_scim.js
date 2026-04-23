const stytch = require('stytch');
const fs = require('fs');

async function main() {
  const client = new stytch.B2BClient({
    project_id: process.env.STYTCH_PROJECT_ID,
    secret: process.env.STYTCH_SECRET,
  });

  try {
    const orgResponse = await client.organizations.create({
      organization_name: "Acme SCIM Org",
      organization_slug: `acme-scim-org-${Date.now()}`
    });

    const orgId = orgResponse.organization.organization_id;

    const scimResponse = await client.scim.connection.create({
      organization_id: orgId,
      display_name: "Acme SCIM Connection",
      identity_provider: "okta"
    });

    // Write to JSON
    const output = {
      organization_id: orgId,
      connection_id: scimResponse.connection.connection_id,
      base_url: scimResponse.connection.base_url,
      bearer_token: scimResponse.connection.bearer_token
    };

    fs.writeFileSync('/home/user/app/scim_output.json', JSON.stringify(output, null, 2));
    console.log("Successfully created SCIM connection.");
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
}

main();