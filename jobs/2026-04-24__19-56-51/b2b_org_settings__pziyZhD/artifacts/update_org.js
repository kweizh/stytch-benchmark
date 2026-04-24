const stytch = require('stytch');

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;
const organizationId = process.argv[2];

if (!projectId || !secret) {
  console.error('Error: STYTCH_PROJECT_ID and STYTCH_SECRET environment variables must be set.');
  process.exit(1);
}

if (!organizationId) {
  console.error('Error: organization_id must be provided as the first command-line argument.');
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: projectId,
  secret: secret,
});

client.organizations
  .update({
    organization_id: organizationId,
    auth_methods: 'RESTRICTED',
    allowed_auth_methods: ['sso', 'magic_link'],
    email_jit_provisioning: 'RESTRICTED',
  })
  .then(() => {
    console.log('Organization updated successfully');
  })
  .catch((err) => {
    console.error('Error updating organization:', err);
    process.exit(1);
  });
