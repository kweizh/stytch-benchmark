const stytch = require('stytch');

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  console.error('Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.');
  process.exit(1);
}

const client = new stytch.Client({
  project_id: projectId,
  secret: secret,
});

async function sendOtp(phoneNumber) {
  const response = await client.otps.sms.loginOrCreate({
    phone_number: phoneNumber,
  });

  if (!response.phone_id) {
    throw new Error('No phone_id returned from Stytch.');
  }

  process.stdout.write(response.phone_id);
}

async function authenticateOtp(phoneId, code) {
  const response = await client.otps.authenticate({
    method_id: phoneId,
    code: code,
  });

  if (!response.user_id) {
    throw new Error('No user_id returned from Stytch.');
  }

  process.stdout.write(response.user_id);
}

async function main() {
  const [, , command, ...args] = process.argv;

  try {
    if (command === 'send') {
      if (args.length !== 1) {
        console.error('Usage: node stytch_sms.js send <phone_number>');
        process.exit(1);
      }
      await sendOtp(args[0]);
      return;
    }

    if (command === 'authenticate') {
      if (args.length !== 2) {
        console.error('Usage: node stytch_sms.js authenticate <phone_id> <code>');
        process.exit(1);
      }
      await authenticateOtp(args[0], args[1]);
      return;
    }

    console.error('Usage: node stytch_sms.js <send|authenticate> ...');
    process.exit(1);
  } catch (error) {
    console.error(error && error.message ? error.message : String(error));
    process.exit(1);
  }
}

main();
