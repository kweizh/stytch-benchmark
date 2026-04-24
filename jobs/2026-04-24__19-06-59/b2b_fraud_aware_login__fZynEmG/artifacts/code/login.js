const stytch = require('stytch');

const STYTCH_B2B_PROJECT_ID = process.env.STYTCH_B2B_PROJECT_ID;
const STYTCH_B2B_SECRET = process.env.STYTCH_B2B_SECRET;

if (!STYTCH_B2B_PROJECT_ID || !STYTCH_B2B_SECRET) {
  console.error('Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables');
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: STYTCH_B2B_PROJECT_ID,
  secret: STYTCH_B2B_SECRET,
});

const telemetry_id = process.argv[2];

if (!telemetry_id) {
  console.error('Please provide a telemetry_id as the first argument');
  process.exit(1);
}

async function run() {
  try {
    const response = await client.fraud.fingerprint.lookup({ telemetry_id });
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
      console.error(`Unexpected verdict action: ${action}`);
      process.exit(1);
    }
  } catch (error) {
    console.error('Error looking up telemetry ID:', error.message || error);
    process.exit(1);
  }
}

run();
