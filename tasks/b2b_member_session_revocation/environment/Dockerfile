FROM node:20-bullseye

# Install basic dependencies
RUN apt-get update && apt-get install -y curl python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Install requests and pytest for the verifier
RUN pip3 install requests pytest

# Set up the workspace
WORKDIR /home/user
RUN mkdir -p /home/user/project
WORKDIR /home/user/project

# Initialize a basic Node.js project
RUN npm init -y
RUN npm install express stytch

# Default command
CMD ["bash"]