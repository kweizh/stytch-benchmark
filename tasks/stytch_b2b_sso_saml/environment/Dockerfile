FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages stytch pytest

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Stytch B2B SSO SAML task environment."

RUN mkdir -p /home/user/stytch_sso

# Container contents:
#   - Python 3 and pip installed
#   - stytch Python SDK installed
#   - /home/user/stytch_sso initialized as project directory

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
