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
LABEL Description="Express.js project setup with Stytch SDK for RBAC middleware task."

RUN mkdir -p /home/user/stytch-app && \
    cd /home/user/stytch-app && \
    cat >package.json <<'EOF'
{
  "name": "stytch-app",
  "version": "1.0.0",
  "description": "Stytch RBAC App",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "dependencies": {
    "express": "^4.18.2",
    "stytch": "^10.0.0"
  }
}
EOF

RUN cd /home/user/stytch-app && \
    cat >index.js <<'EOF'
const express = require('express');
const app = express();
const port = 3000;

// Placeholder for middleware
// const authMiddleware = require('./middleware');

app.use(express.json());

app.post('/upload', (req, res) => {
    // Should be protected by authMiddleware
    res.json({ success: true, message: 'File uploaded' });
});

app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
EOF

RUN cd /home/user/stytch-app && \
    npm install

# Container contents:
#   - Node.js v24 installed
#   - /home/user/stytch-app — Express.js project with express and stytch installed
#   - index.js with a /upload route

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
