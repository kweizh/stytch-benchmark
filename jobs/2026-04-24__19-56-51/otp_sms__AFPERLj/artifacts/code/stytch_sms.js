const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const [, , command, ...args] = process.argv;

async function send(phone_number) {
  const response = await client.otps.sms.loginOrCreate({ phone_number });
  process.stdout.write(response.phone_id + '\n');
}

async function authenticate(method_id, code) {
  const response = await client.otps.authenticate({ method_id, code });
  process.stdout.write(response.user_id + '\n');
}

(async () => {
  if (command === 'send') {
    const phone_number = args[0];
    await send(phone_number);
  } else if (command === 'authenticate') {
    const method_id = args[0];
    const code = args[1];
    await authenticate(method_id, code);
  } else {
    process.stderr.write('Usage:\n');
    process.stderr.write('  node stytch_sms.js send <phone_number>\n');
    process.stderr.write('  node stytch_sms.js authenticate <phone_id> <code>\n');
    process.exit(1);
  }
})();
