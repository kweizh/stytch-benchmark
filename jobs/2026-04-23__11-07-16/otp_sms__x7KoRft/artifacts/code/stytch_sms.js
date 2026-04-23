const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const [, , command, ...args] = process.argv;

async function send(phoneNumber) {
  const response = await client.otps.sms.loginOrCreate({ phone_number: phoneNumber });
  process.stdout.write(response.phone_id + '\n');
}

async function authenticate(phoneId, code) {
  const response = await client.otps.authenticate({ method_id: phoneId, code });
  process.stdout.write(response.user_id + '\n');
}

(async () => {
  if (command === 'send') {
    const phoneNumber = args[0];
    await send(phoneNumber);
  } else if (command === 'authenticate') {
    const phoneId = args[0];
    const code = args[1];
    await authenticate(phoneId, code);
  } else {
    process.stderr.write('Usage:\n  node stytch_sms.js send <phone_number>\n  node stytch_sms.js authenticate <phone_id> <code>\n');
    process.exit(1);
  }
})().catch((err) => {
  process.stderr.write((err.message || String(err)) + '\n');
  process.exit(1);
});
