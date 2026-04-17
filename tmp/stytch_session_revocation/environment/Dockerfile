FROM node:20-slim

# Create user
RUN useradd -m -s /bin/bash user

# Setup project directory
WORKDIR /home/user/app

# Initialize Node.js project and install dependencies
RUN npm init -y && npm install express stytch dotenv

# Create the initial server.js
COPY server.js /home/user/app/server.js
RUN chown -R user:user /home/user/app

USER user

ENV PORT=3000
