import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/app"
TEST_SCRIPT_PATH = os.path.join(PROJECT_DIR, "test_fraud_login.js")

def test_app_file_exists():
    assert os.path.isfile(os.path.join(PROJECT_DIR, "app.js")), "app.js not found in project directory."

def test_express_app_endpoints():
    test_script_content = """
const request = require('supertest');
const nock = require('nock');
const assert = require('assert');

// Set dummy environment variables for Stytch client
process.env.STYTCH_PROJECT_ID = 'project-test-00000000-0000-0000-0000-000000000000';
process.env.STYTCH_SECRET = 'secret-test-11111111-1111-1111-1111-111111111111';

const app = require('./app.js');

describe('POST /login', function() {
  beforeEach(function() {
    nock.cleanAll();
  });

  it('should return 200 OK when verdict action is ALLOW', async function() {
    ['https://test.stytch.com', 'https://api.stytch.com', 'https://telemetry.stytch.com'].forEach(url => {
      nock(url)
        .persist()
        .post('/v1/fingerprint/lookup', { telemetry_id: 'allow-id' })
        .reply(200, { verdict: { action: 'ALLOW' } });
      nock(url)
        .persist()
        .post('/v1/fraud/fingerprint/lookup', { telemetry_id: 'allow-id' })
        .reply(200, { verdict: { action: 'ALLOW' } });
    });

    const response = await request(app)
      .post('/login')
      .send({ telemetry_id: 'allow-id' })
      .expect(200);

    assert.deepStrictEqual(response.body, { message: 'Login successful' });
  });

  it('should return 401 Unauthorized when verdict action is CHALLENGE', async function() {
    ['https://test.stytch.com', 'https://api.stytch.com', 'https://telemetry.stytch.com'].forEach(url => {
      nock(url)
        .persist()
        .post('/v1/fingerprint/lookup', { telemetry_id: 'challenge-id' })
        .reply(200, { verdict: { action: 'CHALLENGE' } });
      nock(url)
        .persist()
        .post('/v1/fraud/fingerprint/lookup', { telemetry_id: 'challenge-id' })
        .reply(200, { verdict: { action: 'CHALLENGE' } });
    });

    const response = await request(app)
      .post('/login')
      .send({ telemetry_id: 'challenge-id' })
      .expect(401);

    assert.deepStrictEqual(response.body, { error: 'MFA required' });
  });

  it('should return 403 Forbidden when verdict action is BLOCK', async function() {
    ['https://test.stytch.com', 'https://api.stytch.com', 'https://telemetry.stytch.com'].forEach(url => {
      nock(url)
        .persist()
        .post('/v1/fingerprint/lookup', { telemetry_id: 'block-id' })
        .reply(200, { verdict: { action: 'BLOCK' } });
      nock(url)
        .persist()
        .post('/v1/fraud/fingerprint/lookup', { telemetry_id: 'block-id' })
        .reply(200, { verdict: { action: 'BLOCK' } });
    });

    const response = await request(app)
      .post('/login')
      .send({ telemetry_id: 'block-id' })
      .expect(403);

    assert.deepStrictEqual(response.body, { error: 'Access denied' });
  });
});
"""
    with open(TEST_SCRIPT_PATH, "w") as f:
        f.write(test_script_content)

    # Install necessary dev dependencies
    subprocess.run(["npm", "install", "nock", "supertest", "mocha"], cwd=PROJECT_DIR, check=True)

    # Run the mocha test
    result = subprocess.run(
        ["npx", "mocha", "test_fraud_login.js"],
        cwd=PROJECT_DIR,
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0, f"Mocha test failed: {result.stdout}\\n{result.stderr}"
