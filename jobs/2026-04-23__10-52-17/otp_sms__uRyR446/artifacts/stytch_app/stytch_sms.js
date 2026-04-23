const stytch = require('stytch');

const { STYTCH_PROJECT_ID, STYTCH_SECRET } = process.env;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  console.error('Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.');
  process.exit(1);
}

const client = new stytch.Client({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
});

async function sendOtp(phoneNumber) {
  const response = await client.otps.sms.loginOrCreate({
    phone_number: phoneNumber,
  });
  process.stdout.write(response.phone_id);
}

async function authenticateOtp(phoneId, code) {
  const response = await client.otps.authenticate({
    method_id: phoneId,
    code,
  });
  process.stdout.write(response.user_id);
}

async function main() {
  const [, , command, ...args] = process.argv;

  if (command === 'send') {
    const [phoneNumber] = args;
    if (!phoneNumber) {
      console.error('Usage: node stytch_sms.js send <phone_number>');
      process.exit(1);
    }
    await sendOtp(phoneNumber);
    return;
  }

  if (command === 'authenticate') {
    const [phoneId, code] = args;
    if (!phoneId || !code) {
      console.error('Usage: node stytch_sms.js authenticate <phone_id> <code>');
      process.exit(1);
    }
    await authenticateOtp(phoneId, code);
    return;
  }

  console.error('Usage: node stytch_sms.js <send|authenticate> [args]');
  process.exit(1);
}

main().catch((error) => {
  console.error(error?.message || String(error));
  process.exit(1);
});
