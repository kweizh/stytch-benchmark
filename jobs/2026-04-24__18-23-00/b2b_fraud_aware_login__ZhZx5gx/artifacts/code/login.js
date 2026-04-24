const stytch = require('stytch');

const projectId = process.env.STYTCH_B2B_PROJECT_ID;
const secret = process.env.STYTCH_B2B_SECRET;

if (!projectId || !secret) {
  console.error('Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET');
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: projectId,
  secret: secret,
  env: stytch.envs.test, // Using test environment
});

const telemetry_id = process.argv[2];

if (!telemetry_id) {
  console.error('Missing telemetry_id argument');
  process.exit(1);
}

async function run() {
  try {
    const response = await client.fraud.fingerprints.lookup({
      telemetry_id: telemetry_id
    });

    const action = response.verdict?.action;

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
      console.log('Unknown action:', action);
      process.exit(1);
    }
  } catch (error) {
    console.error('Error looking up fingerprint:', error.message || error);
    process.exit(1);
  }
}

run();
