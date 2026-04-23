const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

async function main() {
  const user_id = process.argv[2];
  
  if (!user_id) {
    console.error('Please provide a user_id');
    process.exit(1);
  }

  try {
    const response = await client.webauthn.registerStart({
      user_id: user_id,
      domain: 'example.com',
      return_passkey_credential_options: true
    });

    console.log(JSON.stringify(response.public_key_credential_creation_options));
  } catch (error) {
    console.error('Error:', error);
    process.exit(1);
  }
}

main();
