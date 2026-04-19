# Authenticate Google OAuth with Stytch

## Background
You are building a backend for a consumer application using Stytch B2C Python SDK. The user has completed the Google OAuth flow on the frontend, and the frontend has redirected to your backend with a `token` in the URL query string.

## Requirements
Write a Python script `authenticate.py` that takes this token and authenticates it with Stytch.

## Implementation Guide
1. Read `STYTCH_PROJECT_ID` and `STYTCH_SECRET` from environment variables.
2. Accept the OAuth token as the first command-line argument.
3. Initialize the Stytch B2C Client.
4. Authenticate the token using `client.oauth.authenticate(token=...)`.
5. Print the `user_id` from the authentication response to stdout.

## Constraints
- Project path: /home/user/myproject
- Script path: /home/user/myproject/authenticate.py
- Use the `stytch` Python package.