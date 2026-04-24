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
LABEL Description="Express app configured with Stytch Node.js SDK for B2B MFA step-up."

RUN mkdir -p /home/user/app && cd /home/user/app && \
    npm init -y && \
    npm install express cookie-parser dotenv stytch && \
    cat > package.json <<'EOF'
{
  "name": "app",
  "version": "1.0.0",
  "description": "",
  "main": "server.js",
  "scripts": {
    "start": "node server.js"
  },
  "dependencies": {
    "cookie-parser": "^1.4.6",
    "dotenv": "^16.4.5",
    "express": "^4.19.2",
    "stytch": "^10.7.0"
  }
}
EOF

RUN cd /home/user/app && cat > server.js <<'EOF'
const express = require('express');
const cookieParser = require('cookie-parser');
const stytch = require('stytch');

const app = express();
app.use(express.json());
app.use(cookieParser());

const stytchClient = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

// Implement POST /sensitive-action here

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
EOF

# Container contents:
#   - Node.js v24 installed
#   - /home/user/app: Express app with stytch, cookie-parser, and dotenv
#   - /home/user/app/server.js: Skeleton server file waiting for POST /sensitive-action implementation

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
