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
LABEL Description="Stytch Session Management task environment with Node.js v24 installed."

RUN mkdir -p /home/user/stytch-app && \
    cd /home/user/stytch-app && \
    npm init -y

# Container contents:
#   - Node.js v24 installed
#   - /home/user/stytch-app directory initialized with package.json

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
