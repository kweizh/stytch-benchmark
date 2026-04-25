const stytch = require('stytch');

async function run() {
  const telemetry_id = process.argv[2];

  if (!telemetry_id) {
    console.error('Usage: node login.js <telemetry_id>');
    process.exit(1);
  }

  const client = new stytch.B2BClient({
    project_id: process.env.STYTCH_B2B_PROJECT_ID,
    secret: process.env.STYTCH_B2B_SECRET,
  });

  try {
    const response = await client.fraud.fingerprints.lookup({
      telemetry_id: telemetry_id,
    });

    const action = response.verdict.action;

    if (action === 'BLOCK') {
      console.log('Access Denied: Blocked');
      process.exit(1);
    } else if (action === 'CHALLENGE') {
      console.log('MFA Required');
      process.exit(1);
    } else if (action === 'ALLOW') {
      console.log('Login Successful');
      process.exit(0);
    } else {
      console.error('Unknown action:', action);
      process.exit(1);
    }
  } catch (error) {
    console.error('Error looking up fingerprint:', error.message || error);
    process.exit(1);
  }
}

run();
