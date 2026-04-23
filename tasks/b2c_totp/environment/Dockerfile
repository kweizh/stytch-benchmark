FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app && chmod 0755 -R /home/user

LABEL Author="any-task-builder"
LABEL Description="Node.js v24 environment for Stytch B2C TOTP implementation."

# Container contents:
#   - Node.js v24 installed.
#   - Python3, pip, pytest.
#   - /home/user/app - empty project directory for the task.

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
