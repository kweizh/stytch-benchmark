### 1. Library Overview
*   **Description**: Stytch is a developer-first identity and authentication platform specializing in passwordless authentication (Magic Links, OTP, Passkeys), B2B multi-tenancy, and secure connectivity for AI agents.
*   **Ecosystem Role**: It serves as a modern alternative to Auth0 or Firebase, focusing on reducing friction for users and providing robust infrastructure for B2B SaaS and agentic workflows.
*   **Project Setup**:
    1.  **Dashboard**: Create a project at [stytch.com](https://stytch.com/dashboard) to get a `PROJECT_ID`, `SECRET`, and `PUBLIC_TOKEN`.
    2.  **Frontend**: Install `@stytch/nextjs` (for Next.js) or `@stytch/vanilla-js`.
    3.  **Backend**: Install `stytch` (Node.js), `stytch-go`, `stytch-python`, etc.
    4.  **Configuration**: Set up redirect URLs in the Stytch dashboard for authentication callbacks.
### 2. Core Primitives & APIs
*   **B2C vs. B2B Primitives**:
    *   **B2C**: `User`, `Session`, `MagicLinks`, `OTP`, `OAuth`.
    *   **B2B**: `Organization`, `Member`, `MemberSession`, `RBAC`, `SCIM`, `SSO`.
*   **Session Management**:
    *   `session_token`: Opaque string, long-lived, requires API call to verify.
    *   `session_jwt`: 5-minute lifespan, can be verified locally using JWKS for low latency.
*   **Connected Apps & MCP**:
    *   Allows your app to act as an OAuth 2.0 Identity Provider (IdP).
    *   Specifically designed to give AI agents (like ChatGPT or Claude) scoped, revocable access to user data via the Model Context Protocol (MCP).
**Code Snippet: B2B Discovery Flow (Next.js)**
```jsx
import { AuthFlowType, StytchB2B, oauth, emailMagicLinks } from '@stytch/nextjs/b2b';
const Login = () => {
  const config = {
    authFlowType: AuthFlowType.Discovery, // Allows users to find their Org by email
    products: [oauth, emailMagicLinks],
    emailMagicLinksOptions: {
      loginRedirectURL: 'http://localhost:3000/authenticate',
      signupRedirectURL: 'http://localhost:3000/authenticate',
    },
  };
  return <StytchB2B config={config} />;
};
```
**Code Snippet: Backend Session Verification (Node.js)**
```javascript
import * as stytch from 'stytch';
const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});
// Middleware to protect routes
async function authMiddleware(req, res, next) {
  const sessionToken = req.cookies['stytch_session'];  try {
    const { member_session } = await client.sessions.authenticate({
      session_token: sessionToken,
    });
    req.session = member_session;
    next();
  } catch (err) {
    res.status(401).send('Unauthorized');
  }
}
```
*   **Links**: [B2B API Reference](https://stytch.com/docs/b2b/api), [Session Management Guide](https://stytch.com/docs/guides/sessions/overview), [Connected Apps Guide](https://stytch.com/docs/guides/connected-apps/overview).
### 3. Real-World Use Cases & Templates
*   **B2B SaaS Multi-tenancy**: Using "Discovery" to route users to different organizations based on their email domain (e.g., `user@acme.com` goes to the Acme Corp org).
*   **AI Agent Tooling**: Using Stytch as the auth layer for an MCP server, allowing a user to say "Claude, update my tasks in App X" while securely handling the OAuth consent.
*   **Templates**:
    *   [B2B Next.js SaaS Starter](https://github.com/stytchauth/stytch-b2b-nextjs-example)
    *   [Connected Apps AI Agent Demo](https://github.com/stytchauth/stytch-connected-apps-b2b-demo)
    *   [MCP OKR Manager Demo](https://github.com/stytchauth/mcp-stytch-b2b-okr-manager)
### 4. Developer Friction Points
*   **Local JWT Verification Drift**: The `session_jwt` expires every 5 minutes and must be refreshed. Developers often fail to handle the case where a session is revoked in the Stytch backend but the local JWT is still "valid" for the remainder of its 5-minute window.
*   **PKCE Implementation**: For Connected Apps and mobile flows, PKCE is mandatory. Manually generating the `code_challenge` and `code_verifier` correctly is a common source of bugs for those not using the pre-built SDK components.
*   **Organization JIT Provisioning**: Configuring "Allowed Tenants" and "Auth Methods" for B2B organizations can be complex, especially when mixing SAML, Google OAuth, and Magic Links.
### 5. Evaluation Ideas
*   **B2B Discovery & Onboarding**: Implement a flow where a user enters an email, joins an existing organization if a domain match exists, or creates a new one if not.
*   **RBAC Middleware**: Build a backend middleware that extracts a Stytch session and enforces a specific permission (e.g., `files:write`) based on the member's roles.
*   **Local JWT Validator**: Write a standalone service that fetches the JWKS from Stytch and validates incoming `session_jwt` tokens without making any external network calls.
*   **Step-up Authentication Logic**: Create a "sensitive action" route that requires the user to have a multi-factor session (e.g., they logged in with Magic Link but must verify an OTP to proceed).
*   **AI Agent Scoped Access**: Configure a Stytch Connected App so that an external agent can request a token with a `read:profile` scope but not `write:profile`.
*   **Fraud-Aware Login**: Integrate the Stytch Device Fingerprinting SDK and implement logic to challenge or block users with a "high" risk score.
### 6. Sources
1.  [Stytch llms.txt](https://stytch.com/llms.txt) - Structured overview of the entire site and documentation.
2.  [Stytch Docs - JWTs vs Session Tokens](https://stytch.com/docs/multi-tenant-auth/manage-sessions/jwts-and-tokens) - Technical breakdown of session types.
3.  [Stytch Blog - Agent-to-agent OAuth Guide](https://stytch.com/blog/agent-to-agent-oauth-guide/) - Details on MCP and AI agent auth.
4.  [Stytch GitHub Examples](https://github.com/stytchauth) - Reference implementations for B2B and Connected Apps.
5.  [Stytch Forum](https://forum.stytch.com) - Community discussions on common troubleshooting issues.