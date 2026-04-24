FROM ubuntu:22.04

RUN apt-get update && apt-get install -y curl wget unzip python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.x
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    npm install -g npm@latest

RUN useradd -m -s /bin/bash user
USER user
WORKDIR /home/user

RUN mkdir -p /home/user/app
WORKDIR /home/user/app

# Initialize a basic package.json
RUN npm init -y && \
    npm install express stytch

# Setup the start script
RUN npm pkg set scripts.start="node index.js"

ENV STYTCH_B2B_PROJECT_ID=""
ENV STYTCH_B2B_SECRET=""
