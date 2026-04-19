import os
import subprocess
import json
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import pytest

PROJECT_DIR = "/home/user/stytch_pkce"

@pytest.fixture(scope="module")
def mock_server():
    class MockServerRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
                if data.get('client_id') == 'client_live_12345' and data.get('grant_type') == 'authorization_code' and 'code_verifier' in data:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"access_token": "mock_token"}).encode('utf-8'))
                    return
            except Exception:
                pass
            self.send_response(400)
            self.end_headers()

        def log_message(self, format, *args):
            pass

    server = HTTPServer(('localhost', 8080), MockServerRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    yield
    server.shutdown()
    server.server_close()

def test_pkce_file_exists():
    pkce_file = os.path.join(PROJECT_DIR, "pkce.js")
    assert os.path.exists(pkce_file), f"pkce.js not found at {pkce_file}"

def test_pkce_implementation(mock_server):
    test_script = """
const { generatePKCE, buildAuthorizeUrl, exchangeToken } = require('./pkce.js');
const crypto = require('crypto');

async function runTests() {
    const { codeVerifier, codeChallenge } = generatePKCE();
    if (!codeVerifier || codeVerifier.length < 43) throw new Error("Invalid codeVerifier length");
    
    const expectedChallenge = crypto.createHash('sha256').update(codeVerifier).digest('base64url');
    if (codeChallenge !== expectedChallenge) throw new Error("Invalid codeChallenge");

    const url = buildAuthorizeUrl('https://app.example.com/authorize', 'client_live_12345', 'https://client.example.com/callback', ['read:profile'], codeChallenge);
    if (!url.includes('response_type=code')) throw new Error("Missing response_type");
    if (!url.includes('code_challenge_method=S256')) throw new Error("Missing code_challenge_method");
    if (!url.includes('client_id=client_live_12345')) throw new Error("Missing client_id");
    if (!url.includes(encodeURIComponent('https://client.example.com/callback'))) throw new Error("Missing encoded redirect_uri");

    const res = await exchangeToken('http://localhost:8080/token', 'client_live_12345', 'auth_code_xyz', codeVerifier, 'https://client.example.com/callback');
    if (res.access_token !== 'mock_token') throw new Error("Token exchange failed");
    
    console.log("SUCCESS");
}

runTests().catch(e => {
    console.error(e.message);
    process.exit(1);
});
"""
    test_file_path = os.path.join(PROJECT_DIR, "test_runner.js")
    with open(test_file_path, "w") as f:
        f.write(test_script)

    result = subprocess.run(["node", "test_runner.js"], cwd=PROJECT_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"Node.js tests failed: {result.stderr.strip()}"
    assert "SUCCESS" in result.stdout, f"Node.js tests did not output SUCCESS: {result.stdout.strip()}"
