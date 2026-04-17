FROM python:3.11-slim

RUN useradd -m -s /bin/bash user
USER user
WORKDIR /home/user

RUN pip install --no-cache-dir stytch

ENV STYTCH_PROJECT_ID="project-test-00000000-0000-1234-abcd-abcdef1234"
ENV STYTCH_SECRET="secret-test-12345678901234567890abcdabcd"

CMD ["/bin/bash"]
