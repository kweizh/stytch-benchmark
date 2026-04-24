const stytch = require('stytch');
const fs = require('fs');
const path = require('path');

async function setupScim() {
  const client = new stytch.B2BClient({
    project_id: process.env.STYTCH_PROJECT_ID,
    secret: process.env.STYTCH_SECRET,
  });

  try {
    // 1. Create a new B2B Organization
    const slug = `acme-scim-org-${Date.now()}`;
    console.log(`Creating organization with slug: ${slug}`);
    
    const orgResponse = await client.organizations.create({
      organization_name: 'Acme SCIM Org',
      organization_slug: slug,
    });
    
    const organization_id = orgResponse.organization.organization_id;
    console.log(`Organization created with ID: ${organization_id}`);

    // 2. Create a SCIM connection
    console.log(`Creating SCIM connection for organization: ${organization_id}`);
    const scimResponse = await client.scim.connection.create({
      organization_id: organization_id,
      display_name: 'Acme SCIM Connection',
      identity_provider: 'okta',
    });

    // Extract connection info
    const connection = scimResponse.connection;
    const connection_id = connection.connection_id;
    const base_url = connection.base_url;
    const bearer_token = connection.bearer_token;

    console.log(`SCIM connection created with ID: ${connection_id}`);

    const output = {
      organization_id,
      connection_id,
      base_url,
      bearer_token,
    };

    const outputPath = path.join(__dirname, 'scim_output.json');
    fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));
    console.log(`Successfully wrote SCIM setup output to ${outputPath}`);
    
    // Also save artifacts
    const artifactsDir = '/logs/artifacts/code';
    if (!fs.existsSync(artifactsDir)) {
      fs.mkdirSync(artifactsDir, { recursive: true });
    }
    fs.copyFileSync(__filename, path.join(artifactsDir, 'setup_scim.js'));
    fs.copyFileSync(outputPath, path.join('/logs/artifacts', 'scim_output.json'));
    
  } catch (error) {
    console.error('Error setting up SCIM:');
    if (error.response) {
      console.error(error.response.data || error.response);
    } else {
      console.error(error.message);
    }
    process.exit(1);
  }
}

setupScim();
