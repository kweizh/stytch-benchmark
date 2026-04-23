const stytch = require('stytch');

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;
const organization_id = process.argv[2];

if (!projectId || !secret) {
  console.error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET");
  process.exit(1);
}

if (!organization_id) {
  console.error("Please provide an organization_id");
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: projectId,
  secret: secret,
});

async function updateOrg() {
  try {
    await client.organizations.update({
      organization_id: organization_id,
      auth_methods: 'RESTRICTED',
      allowed_auth_methods: ['sso', 'magic_link'],
      email_jit_provisioning: 'RESTRICTED'
    });
    console.log("Organization updated successfully");
  } catch (error) {
    console.error("Error updating organization:", error);
    process.exit(1);
  }
}

updateOrg();
