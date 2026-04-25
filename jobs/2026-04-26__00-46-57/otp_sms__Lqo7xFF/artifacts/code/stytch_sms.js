const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

async function run() {
  const [,, command, ...args] = process.argv;

  if (command === 'send') {
    const phoneNumber = args[0];
    try {
      const response = await client.otps.sms.loginOrCreate({
        phone_number: phoneNumber,
      });
      process.stdout.write(response.phone_id);
    } catch (error) {
      console.error(error);
      process.exit(1);
    }
  } else if (command === 'authenticate') {
    const [phoneId, code] = args;
    try {
      const response = await client.otps.authenticate({
        method_id: phoneId,
        code: code,
      });
      process.stdout.write(response.user_id);
    } catch (error) {
      console.error(error);
      process.exit(1);
    }
  } else {
    console.error('Usage: node stytch_sms.js send <phone_number> OR node stytch_sms.js authenticate <phone_id> <code>');
    process.exit(1);
  }
}

run();
