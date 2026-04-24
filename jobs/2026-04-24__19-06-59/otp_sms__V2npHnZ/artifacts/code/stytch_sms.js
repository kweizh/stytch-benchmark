const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

async function run() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    if (command === 'send') {
      const phoneNumber = args[1];
      const response = await client.otps.sms.loginOrCreate({
        phone_number: phoneNumber,
      });
      process.stdout.write(response.phone_id);
    } else if (command === 'authenticate') {
      const phoneId = args[1];
      const code = args[2];
      const response = await client.otps.authenticate({
        method_id: phoneId,
        code: code,
      });
      process.stdout.write(response.user_id);
    }
  } catch (err) {
    process.exit(1);
  }
}

run();
