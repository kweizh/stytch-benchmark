const stytch = require('stytch');

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const args = process.argv.slice(2);
const command = args[0];

if (command === 'send') {
  const phone_number = args[1];
  client.otps.sms.loginOrCreate({ phone_number })
    .then(resp => {
      console.log(resp.phone_id);
    })
    .catch(err => {
      console.error(err);
      process.exit(1);
    });
} else if (command === 'authenticate') {
  const method_id = args[1]; // phone_id
  const code = args[2];
  client.otps.authenticate({ method_id, code })
    .then(resp => {
      console.log(resp.user_id);
    })
    .catch(err => {
      console.error(err);
      process.exit(1);
    });
} else {
  console.error("Unknown command");
  process.exit(1);
}
