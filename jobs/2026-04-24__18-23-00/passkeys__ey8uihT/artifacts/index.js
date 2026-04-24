const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const userId = process.argv[2];

if (!userId) {
  console.error("Please provide a user_id as the first argument.");
  process.exit(1);
}

async function registerStart() {
  try {
    const response = await client.webauthn.registerStart({
      user_id: userId,
      domain: 'example.com',
      return_passkey_credential_options: true,
    });
    
    console.log(JSON.stringify(response.public_key_credential_creation_options));
  } catch (error) {
    console.error("Error starting WebAuthn registration:", error);
    process.exit(1);
  }
}

registerStart();
