"use strict";

const express = require("express");
const stytch = require("stytch");

// ---------------------------------------------------------------------------
// Stytch B2B client
// ---------------------------------------------------------------------------
const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

// ---------------------------------------------------------------------------
// Express app
// ---------------------------------------------------------------------------
const app = express();
app.use(express.json());

// ---------------------------------------------------------------------------
// POST /api/discovery/send
// Body: { email }
// Sends a Discovery Magic Link to the provided email address.
// ---------------------------------------------------------------------------
app.post("/api/discovery/send", async (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ error: "email is required" });
  }

  try {
    const response = await client.magicLinks.email.discovery.send({
      email_address: email,
    });
    return res.status(200).json(response);
  } catch (err) {
    console.error("Error in /api/discovery/send:", err);
    const status = err.status_code ?? 500;
    return res.status(status).json({ error: err.error_message ?? err.message });
  }
});

// ---------------------------------------------------------------------------
// POST /api/discovery/authenticate
// Body: { discovery_magic_links_token }
// Authenticates the Discovery Magic Link token and returns an intermediate
// session token plus the list of discovered organizations.
// ---------------------------------------------------------------------------
app.post("/api/discovery/authenticate", async (req, res) => {
  const { discovery_magic_links_token } = req.body;

  if (!discovery_magic_links_token) {
    return res
      .status(400)
      .json({ error: "discovery_magic_links_token is required" });
  }

  try {
    const response = await client.magicLinks.discovery.authenticate({
      discovery_magic_links_token,
    });

    return res.status(200).json({
      intermediate_session_token: response.intermediate_session_token,
      discovered_organizations: response.discovered_organizations,
    });
  } catch (err) {
    console.error("Error in /api/discovery/authenticate:", err);
    const status = err.status_code ?? 500;
    return res.status(status).json({ error: err.error_message ?? err.message });
  }
});

// ---------------------------------------------------------------------------
// POST /api/discovery/exchange
// Body: { intermediate_session_token, organization_id }
// Exchanges the intermediate session for a full member session in the
// specified organization.
// ---------------------------------------------------------------------------
app.post("/api/discovery/exchange", async (req, res) => {
  const { intermediate_session_token, organization_id } = req.body;

  if (!intermediate_session_token) {
    return res
      .status(400)
      .json({ error: "intermediate_session_token is required" });
  }
  if (!organization_id) {
    return res.status(400).json({ error: "organization_id is required" });
  }

  try {
    const response = await client.discovery.intermediateSessions.exchange({
      intermediate_session_token,
      organization_id,
    });

    return res.status(200).json({ member_session: response.member_session });
  } catch (err) {
    console.error("Error in /api/discovery/exchange:", err);
    const status = err.status_code ?? 500;
    return res.status(status).json({ error: err.error_message ?? err.message });
  }
});

// ---------------------------------------------------------------------------
// POST /api/discovery/create
// Body: { intermediate_session_token, organization_name }
// Creates a new organization using the intermediate session and returns the
// new organization and member session.
// ---------------------------------------------------------------------------
app.post("/api/discovery/create", async (req, res) => {
  const { intermediate_session_token, organization_name } = req.body;

  if (!intermediate_session_token) {
    return res
      .status(400)
      .json({ error: "intermediate_session_token is required" });
  }
  if (!organization_name) {
    return res.status(400).json({ error: "organization_name is required" });
  }

  try {
    const response = await client.discovery.organizations.create({
      intermediate_session_token,
      organization_name,
    });

    return res.status(200).json({
      organization: response.organization,
      member_session: response.member_session,
    });
  } catch (err) {
    console.error("Error in /api/discovery/create:", err);
    const status = err.status_code ?? 500;
    return res.status(status).json({ error: err.error_message ?? err.message });
  }
});

// ---------------------------------------------------------------------------
// Start server
// ---------------------------------------------------------------------------
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Stytch B2B Discovery API listening on port ${PORT}`);
});
