const stytch = require('stytch');

const STYTCH_PROJECT_ID = process.env.STYTCH_PROJECT_ID;
const STYTCH_SECRET = process.env.STYTCH_SECRET;
const organization_id = process.argv[2];

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  console.error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.");
  process.exit(1);
}

if (!organization_id) {
  console.error("Missing organization_id as the first command-line argument.");
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
});

async function updateOrganization() {
  try {
    await client.organizations.update({
      organization_id,
      auth_methods: 'RESTRICTED',
      allowed_auth_methods: ['sso', 'magic_link'],
      email_jit_provisioning: 'RESTRICTED',
    });
    console.log("Organization updated successfully");
  } catch (error) {
    console.error("Error updating organization:", error);
    process.exit(1);
  }
}

updateOrganization();
