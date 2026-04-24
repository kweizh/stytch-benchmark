FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://raw.githubusercontent.com/gofixpoint/amika/main/install.sh | bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --break-system-packages stytch==15.1.0 requests==2.31.0

RUN mkdir -p /home/user && chmod 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Stytch B2B organization deletion task environment with Python, stytch SDK, and amika installed."

RUN mkdir -p /home/user/project

# Container contents:
#   - python3, pip, pytest, curl, git
#   - stytch SDK and requests installed via pip
#   - amika CLI installed
#   - /home/user/project: empty directory for the task

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]