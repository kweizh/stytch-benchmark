# Stytch Connected Apps PKCE Implementation

## Background
Stytch Connected Apps allows your application to act as an OAuth/OIDC Authorization Server. For public clients, the Authorization Code Flow with PKCE is mandatory. You need to implement the PKCE utilities and token exchange logic in Node.js.

## Requirements
1. Initialize a Node.js project in `/home/user/stytch_pkce`.
2. Create a file `pkce.js` that exports the following functions:
   - `generatePKCE()`: Returns `{ codeVerifier, codeChallenge }`. The `codeVerifier` must be a cryptographically random string (at least 43 chars). `codeChallenge` must be the base64url-encoded SHA-256 hash of the verifier.
   - `buildAuthorizeUrl(authEndpoint, clientId, redirectUri, scopes, codeChallenge)`: Constructs and returns the OAuth 2.0 authorization URL string. It must include `response_type=code`, `code_challenge_method=S256`, `client_id`, `redirect_uri`, `scope`, and `code_challenge`.
   - `exchangeToken(tokenEndpoint, clientId, code, codeVerifier, redirectUri)`: Makes a POST request to the token endpoint with a JSON body containing `client_id`, `grant_type: 'authorization_code'`, `code`, `code_verifier`, and `redirect_uri`. Returns the parsed JSON response.
3. The `exchangeToken` function must use the global `fetch` API (Node.js 18+).

## Constraints
- Project path: `/home/user/stytch_pkce`
- Use Node.js built-in `crypto` module for PKCE generation.
- Do not use external libraries for PKCE or HTTP requests.

## Integrations
- None