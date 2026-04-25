const stytch = require('stytch');

async function main() {
  const telemetry_id = process.argv[2];

  if (!telemetry_id) {
    console.error('Error: telemetry_id is required');
    process.exit(1);
  }

  const project_id = process.env.STYTCH_B2B_PROJECT_ID;
  const secret = process.env.STYTCH_B2B_SECRET;

  if (!project_id || !secret) {
    console.error('Error: STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET must be set');
    process.exit(1);
  }

  try {
    const client = new stytch.B2BClient({
      project_id: project_id,
      secret: secret,
    });

    const response = await client.fraud.fingerprint.lookup({
      telemetry_id: telemetry_id,
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
      console.error(`Unknown action: ${action}`);
      process.exit(1);
    }
  } catch (error) {
    console.error('Error looking up fingerprint:', error.message || error);
    process.exit(1);
  }
}

main();