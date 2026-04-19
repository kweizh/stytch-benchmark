# Stytch MCP Auth Layer

## Background
You are building an MCP (Model Context Protocol) server that requires authentication. You will use Stytch as the identity provider. The server needs a Node.js script to verify incoming B2B session JWTs.

## Requirements
- Implement a function `verifyAgentToken(jwt)` in `/home/user/mcp_server/mcp_auth.js`.
- The function should use the `stytch` Node.js SDK (`stytch.B2BClient`).
- It must authenticate a `session_jwt`.
- Return the `member_session` object if successful, or throw an error if invalid.
- Read `STYTCH_PROJECT_ID` and `STYTCH_SECRET` from environment variables.

## Implementation Guide
1. Initialize a Node.js project in `/home/user/mcp_server`.
2. Install the `stytch` package.
3. Create `/home/user/mcp_server/mcp_auth.js` and implement the `verifyAgentToken` function.
4. Export the function using `module.exports = { verifyAgentToken };`.

## Constraints
- Project path: `/home/user/mcp_server`
- Use `stytch` SDK version 10 or later.

## Integrations
- None