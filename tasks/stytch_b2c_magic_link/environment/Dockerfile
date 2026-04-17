FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages requests

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js environment for Stytch B2C Magic Link task."

RUN mkdir -p /home/user/stytch-app

# Container contents:
#   - Node.js v24 for the Express app
#   - python3-pytest and requests for testing
#   - /home/user/stytch-app: empty directory for the project

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
