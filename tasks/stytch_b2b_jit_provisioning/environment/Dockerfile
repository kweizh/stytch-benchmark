FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages requests

RUN mkdir -p /home/user/stytch_project && chmod 0755 /home/user/stytch_project

LABEL Author="any-task-builder"
LABEL Description="Environment for Stytch B2B JIT Provisioning task."

# Container contents:
#   - python3, pip3, pytest, requests installed
#   - /home/user/stytch_project created

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
