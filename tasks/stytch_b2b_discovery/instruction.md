# Implement Stytch B2B Discovery and Onboarding Flow

## Background
You are building a B2B SaaS application using Next.js (App Router) and Stytch for authentication. You need to implement a B2B Discovery and Onboarding flow so that users can log in, join an existing organization, or create a new one.

## Requirements
- The project is an existing Next.js application located at `/home/user/app`.
- Install the necessary Stytch SDKs: `@stytch/nextjs` and `@stytch/vanilla-js`.
- In `app/layout.tsx`, wrap the application with the `StytchB2BProvider` initialized with the public token `public-token-test-11111111-1111-1111-1111-111111111111`.
- Create a new page at `app/login/page.tsx` that renders the `StytchB2B` component with a configuration for the Discovery flow.
- The configuration must set `authFlowType` to `AuthFlowType.Discovery`.
- The configuration must enable `emailMagicLinks` in the `products` array.
- The configuration must set `loginRedirectURL` and `signupRedirectURL` inside `emailMagicLinksOptions` to `http://localhost:3000/authenticate`.

## Implementation Guide
1. `cd /home/user/app` and run `npm install @stytch/nextjs @stytch/vanilla-js`.
2. Update `app/layout.tsx` to include the `StytchB2BProvider` from `@stytch/nextjs/b2b` and `createStytchB2BUIClient` from `@stytch/nextjs/b2b/ui`.
3. Create `app/login/page.tsx` and implement the `StytchB2B` component with the required configuration.

## Constraints
- Project path: `/home/user/app`
- Start command: `npm run build && npm start`
- Port: `3000`