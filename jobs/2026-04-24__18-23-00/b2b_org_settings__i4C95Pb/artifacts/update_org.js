const stytch = require('stytch');

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const organization_id = process.argv[2];

if (!organization_id) {
  console.error("Please provide an organization_id as the first argument.");
  process.exit(1);
}

client.organizations.update({
  organization_id: organization_id,
  auth_methods: 'RESTRICTED',
  allowed_auth_methods: ['sso', 'magic_link'],
  email_jit_provisioning: 'RESTRICTED'
}).then(() => {
  console.log("Organization updated successfully");
}).catch((err) => {
  console.error("Error updating organization:", err);
});
