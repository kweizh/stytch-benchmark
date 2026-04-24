# Stytch B2B Fraud-Aware Login CLI

## Overview
`login.js` is a Node.js CLI script that integrates Stytch Device Fingerprinting to evaluate a user's risk level before granting login access.

## Setup

```bash
cd /home/user/project
npm install
```

## Usage

```bash
export STYTCH_B2B_PROJECT_ID="your-project-id"
export STYTCH_B2B_SECRET="your-secret"

node login.js <telemetry_id>
```

## Behavior

| Verdict    | Output                  | Exit Code |
|------------|-------------------------|-----------|
| `ALLOW`    | `Login Successful`      | 0         |
| `BLOCK`    | `Access Denied: Blocked`| 1         |
| `CHALLENGE`| `MFA Required`          | 1         |
| API Error  | `Access Denied: Blocked`| 1         |

## Implementation Details

- Initializes `stytch.B2BClient` using `STYTCH_B2B_PROJECT_ID` and `STYTCH_B2B_SECRET` env vars.
- Calls `client.fraud.fingerprint.lookup({ telemetry_id })` which posts to the Stytch Device Fingerprinting API.
- Reads `response.verdict.action` and prints the appropriate message.
- On API errors (including 404 "telemetry_id_not_found"), defaults to `BLOCK` per Stytch's security recommendation.
