# Stytch B2C Magic Link Implementation Report

## Overview
Implemented a passwordless authentication flow using Stytch Email Magic Links with Express.js.

## Components
- **Express Server**: Listens on port 3000.
- **POST /login**: Sends a magic link to the provided email using `stytch.magicLinks.email.loginOrCreate`.
- **GET /authenticate**: Authenticates the magic link token using `stytch.magicLinks.authenticate`.

## Configuration
- Uses `STYTCH_PROJECT_ID` and `STYTCH_SECRET` environment variables.
- Environment is automatically determined based on the Project ID prefix.

## Files
- `/home/user/stytch-app/index.js`: Main application logic.
- `/home/user/stytch-app/package.json`: Project dependencies.
