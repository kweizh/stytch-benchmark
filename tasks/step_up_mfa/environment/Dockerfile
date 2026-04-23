FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages stytch pyotp requests

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js 24 environment for Express.js step-up MFA task."

RUN mkdir -p /home/user/app

# Container contents:
#   - Node.js v24 for the Express.js app
#   - /home/user/app empty directory for the user to initialize their project

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]