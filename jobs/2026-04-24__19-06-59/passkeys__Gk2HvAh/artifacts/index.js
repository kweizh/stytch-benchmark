const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: stytch.envs.test,
});

const userId = process.argv[2];

if (!userId) {
  process.exit(1);
}

async function startRegistration() {
  try {
    const response = await client.webauthn.registerStart({
      user_id: userId,
      domain: 'example.com',
      return_passkey_credential_options: true,
    });
    console.log(JSON.stringify(response.public_key_credential_creation_options));
  } catch (error) {
    console.error(error);
    process.exit(1);
  }
}

startRegistration();
