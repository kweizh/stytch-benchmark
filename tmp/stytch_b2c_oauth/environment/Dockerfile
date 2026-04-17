FROM node:20-slim

# Create a non-root user
RUN useradd -m -s /bin/bash user

# Create app directory
RUN mkdir -p /home/user/app && chown -R user:user /home/user/app

USER user
WORKDIR /home/user
