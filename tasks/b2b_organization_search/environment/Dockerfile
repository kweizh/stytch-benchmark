FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest python3-requests bash && \
    curl -fsSL https://deb.nodesource.com/setup_24.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages requests

RUN mkdir -p /home/user/project && chmod 0755 /home/user/project

LABEL Author="any-task-builder"
LABEL Description="Node.js environment for Stytch B2B Discovery API task."

# Container contents:
#   - Node.js v24 installed
#   - python3, pytest, requests installed for verification
#   - /home/user/project empty directory created

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]