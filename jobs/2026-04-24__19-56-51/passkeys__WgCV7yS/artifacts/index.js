const stytch = require("stytch");

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const user_id = process.argv[2];

client.webauthn
  .registerStart({
    user_id,
    domain: "example.com",
    return_passkey_credential_options: true,
  })
  .then((response) => {
    console.log(JSON.stringify(response.public_key_credential_creation_options));
  })
  .catch((err) => {
    console.error(err);
    process.exit(1);
  });
