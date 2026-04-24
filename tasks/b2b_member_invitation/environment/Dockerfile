FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages stytch requests

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Stytch B2B Member Invitation task environment with Python and Stytch SDK installed."

RUN mkdir -p /home/user/project

# Container contents:
#   - always required libs: curl ca-certificates git python3 python3-pip python3-pytest bash
#   - stytch Python SDK installed
#   - /home/user/project: empty directory for the task

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
