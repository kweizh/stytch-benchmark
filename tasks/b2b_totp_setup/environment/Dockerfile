FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages stytch pyotp requests

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Stytch B2B TOTP Setup environment with Python 3, stytch, and pyotp installed."

RUN mkdir -p /home/user/stytch_project

# Container contents:
#   - python3, pip, pytest, curl, git
#   - stytch, pyotp, requests python packages installed
#   - /home/user/stytch_project directory created

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
