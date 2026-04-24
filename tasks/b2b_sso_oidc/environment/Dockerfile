FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages stytch==10.1.0 requests

RUN mkdir -p /home/user/project && chmod 0755 /home/user/project

LABEL Author="any-task-builder"
LABEL Description="Environment for configuring Stytch B2B OIDC connection using Python."

# Container contents:
#   - stytch Python SDK installed.
#   - /home/user/project - empty project directory

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]