FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages requests stytch

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Environment for updating a Stytch B2B organization using Python"

RUN mkdir -p /home/user/stytch_project

# Container contents:
#   - python3, pip, pytest, and bash installed
#   - requests and stytch python libraries installed
#   - /home/user/stytch_project: base directory for the user script

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]