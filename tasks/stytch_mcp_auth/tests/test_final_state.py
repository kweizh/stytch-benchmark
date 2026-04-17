import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/mcp_server"
AUTH_FILE = os.path.join(PROJECT_DIR, "mcp_auth.js")

def test_mcp_auth_file_exists():
    assert os.path.isfile(AUTH_FILE), f"mcp_auth.js not found at {AUTH_FILE}"

def test_exports_verifyAgentToken():
    # Write a small script to test if the module exports verifyAgentToken
    test_script = os.path.join(PROJECT_DIR, "test_export.js")
    script_content = """
    try {
        const auth = require('./mcp_auth.js');
        if (typeof auth.verifyAgentToken !== 'function') {
            console.error('verifyAgentToken is not exported as a function');
            process.exit(1);
        }
        process.exit(0);
    } catch (e) {
        console.error(e.message);
        process.exit(1);
    }
    """
    with open(test_script, "w") as f:
        f.write(script_content)

    env = os.environ.copy()
    env["STYTCH_PROJECT_ID"] = "project-test-123"
    env["STYTCH_SECRET"] = "secret-test-123"

    result = subprocess.run(["node", "test_export.js"], cwd=PROJECT_DIR, env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"mcp_auth.js does not export verifyAgentToken: {result.stderr}"

def test_verifyAgentToken_uses_stytch():
    with open(AUTH_FILE, "r") as f:
        content = f.read()
    
    assert "stytch" in content, "The script does not seem to require or import 'stytch'"
    assert "B2BClient" in content, "The script does not use Stytch B2BClient"
    assert "verifyAgentToken" in content, "The script does not define verifyAgentToken"

def test_verifyAgentToken_throws_on_invalid_token():
    # Write a test script to call verifyAgentToken with an invalid token
    test_script = os.path.join(PROJECT_DIR, "test_invalid_token.js")
    script_content = """
    const auth = require('./mcp_auth.js');
    async function runTest() {
        try {
            await auth.verifyAgentToken('invalid_jwt_token');
            // If it doesn't throw, we exit with 1
            process.exit(1);
        } catch (e) {
            // It threw an error as expected
            process.exit(0);
        }
    }
    runTest();
    """
    with open(test_script, "w") as f:
        f.write(script_content)

    # We need STYTCH_PROJECT_ID and STYTCH_SECRET to be set for the client to initialize
    env = os.environ.copy()
    env["STYTCH_PROJECT_ID"] = "project-test-123"
    env["STYTCH_SECRET"] = "secret-test-123"

    result = subprocess.run(["node", "test_invalid_token.js"], cwd=PROJECT_DIR, env=env, capture_output=True, text=True)
    assert result.returncode == 0, f"verifyAgentToken did not throw an error for an invalid token: {result.stderr}"
