const stytch = require('stytch');

const organizationId = process.argv[2];

if (!organizationId) {
  console.error('Usage: node update_org.js <organization_id>');
  process.exit(1);
}

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  console.error('Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variable');
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: projectId,
  secret,
});

async function updateOrganization() {
  await client.organizations.update({
    organization_id: organizationId,
    auth_methods: 'RESTRICTED',
    allowed_auth_methods: ['sso', 'magic_link'],
    email_jit_provisioning: 'RESTRICTED',
  });

  console.log('Organization updated successfully');
}

updateOrganization().catch((error) => {
  console.error('Failed to update organization:', error);
  process.exit(1);
});
