FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Express.js project with Stytch Node.js SDK installed for integrating Device Fingerprinting."

RUN mkdir -p /home/user/app && \
    cd /home/user/app && \
    cat >package.json <<'EOF'
{
  "name": "stytch-dfp-demo",
  "version": "1.0.0",
  "description": "Stytch Device Fingerprinting demo",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.19.2",
    "stytch": "^10.0.0"
  }
}
EOF

RUN cd /home/user/app && \
    cat >index.js <<'EOF'
const express = require('express');
const app = express();
const port = 3000;

app.use(express.json());

app.post('/login', (req, res) => {
    // TODO: Integrate Stytch Device Fingerprinting
    // 1. Initialize Stytch Client
    // 2. Extract X-Telemetry-ID header
    // 3. Call client.fraud.fingerprint.lookup
    // 4. Handle verdict (ALLOW, CHALLENGE, BLOCK)
    
    // For now, just allow login
    res.status(200).json({ success: true });
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
EOF

RUN cd /home/user/app && npm install

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - Node.js v24
#   - /home/user/app: Express.js application with stytch SDK installed
#   - /home/user/app/index.js: basic login endpoint to be protected

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
