const stytch = require('stytch');
require('dotenv').config();

const PROJECT_ID = process.env.STYTCH_B2B_PROJECT_ID;
const SECRET = process.env.STYTCH_B2B_SECRET;

if (!PROJECT_ID || !SECRET) {
  console.log('Environment variables STYTCH_B2B_PROJECT_ID and STYTCH_B2B_SECRET must be set to run this test.');
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: PROJECT_ID,
  secret: SECRET,
});

async function test() {
  console.log('Testing local JWT validation logic...');
  try {
    // This will fail because the JWT is invalid, but it confirms the client is initialized correctly
    await client.sessions.authenticateJwtLocal({
      session_jwt: 'invalid-token',
    });
  } catch (err) {
    if (err.code === 'jwt_invalid') {
      console.log('Test passed: Correctly identified invalid JWT.');
    } else {
      console.error('Test failed with unexpected error:', err);
    }
  }
}

test();
