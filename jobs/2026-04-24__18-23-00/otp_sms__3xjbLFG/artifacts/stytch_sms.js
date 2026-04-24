const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === 'send') {
    const phoneNumber = args[1];
    try {
      const response = await client.otps.sms.loginOrCreate({
        phone_number: phoneNumber,
      });
      console.log(response.phone_id);
    } catch (error) {
      console.error('Error sending OTP:', error);
      process.exit(1);
    }
  } else if (command === 'authenticate') {
    const phoneId = args[1];
    const code = args[2];
    try {
      const response = await client.otps.authenticate({
        method_id: phoneId,
        code: code,
      });
      console.log(response.user_id);
    } catch (error) {
      console.error('Error authenticating OTP:', error);
      process.exit(1);
    }
  } else {
    console.error('Unknown command');
    process.exit(1);
  }
}

main();
