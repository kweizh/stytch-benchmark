import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"

def test_step_up_auth_logic():
    """Priority 1: Use a Node script with supertest to verify the Express app logic."""
    
    test_script = """
const request = require('supertest');
const app = require('./app');

async function runTests() {
  let exitCode = 0;
  
  // Test 1: No session cookie
  const res1 = await request(app).post('/transfer');
  if (res1.status !== 401) {
    console.error(`Test 1 Failed: Expected 401, got ${res1.status}`);
    exitCode = 1;
  }

  // Mock Stytch Client
  app.locals.stytchClient.sessions.authenticate = async ({ session_token }) => {
    if (session_token === 'valid-no-totp') {
      return {
        session: {
          authentication_factors: [
            { type: 'magic_link' }
          ]
        }
      };
    } else if (session_token === 'valid-with-totp') {
      return {
        session: {
          authentication_factors: [
            { type: 'magic_link' },
            { type: 'totp' }
          ]
        }
      };
    }
    throw new Error('Invalid token');
  };

  // Test 2: Valid session, NO totp factor
  const res2 = await request(app)
    .post('/transfer')
    .set('Cookie', ['stytch_session=valid-no-totp']);
    
  if (res2.status !== 403 || res2.text !== 'Step-up authentication required') {
    console.error(`Test 2 Failed: Expected 403 and 'Step-up authentication required', got ${res2.status} ${res2.text}`);
    exitCode = 1;
  }

  // Test 3: Valid session, WITH totp factor
  const res3 = await request(app)
    .post('/transfer')
    .set('Cookie', ['stytch_session=valid-with-totp']);
    
  if (res3.status !== 200 || res3.text !== 'Transfer successful') {
    console.error(`Test 3 Failed: Expected 200 and 'Transfer successful', got ${res3.status} ${res3.text}`);
    exitCode = 1;
  }

  process.exit(exitCode);
}

runTests().catch(err => {
  console.error(err);
  process.exit(1);
});
"""
    
    test_script_path = os.path.join(PROJECT_DIR, "verify_step_up.js")
    with open(test_script_path, "w") as f:
        f.write(test_script)
        
    result = subprocess.run(
        ["node", "verify_step_up.js"],
        capture_output=True, text=True, cwd=PROJECT_DIR
    )
    
    assert result.returncode == 0, f"Step-up authentication verification failed:\\n{result.stderr}\\n{result.stdout}"
