FROM node:20-bullseye

RUN useradd -m -s /bin/bash user

USER user
WORKDIR /home/user

RUN mkdir -p /home/user/stytch_pkce && \
    cd /home/user/stytch_pkce && \
    npm init -y

ENV NODE_ENV=development
