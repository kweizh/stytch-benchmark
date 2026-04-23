const express = require("express");
const stytch = require("stytch");

const app = express();
app.use(express.json());

const projectId = process.env.STYTCH_PROJECT_ID;
const secret = process.env.STYTCH_SECRET;

if (!projectId || !secret) {
  throw new Error("STYTCH_PROJECT_ID and STYTCH_SECRET must be set");
}

const client = new stytch.B2CClient({
  project_id: projectId,
  secret,
  env: stytch.envs.test,
});

app.post("/transfer", async (req, res) => {
  const { session_token: sessionToken } = req.body || {};

  if (!sessionToken) {
    return res.status(400).json({ error: "session_token is required" });
  }

  try {
    const response = await client.sessions.authenticate({
      session_token: sessionToken,
    });
    const session = response.session || {};
    const factors = session.authentication_factors || [];

    if (factors.length < 2) {
      return res.status(403).json({ error: "Step-up MFA required" });
    }

    return res.status(200).json({ success: true });
  } catch (error) {
    return res.status(401).json({ error: "Unauthorized" });
  }
});

app.listen(3000, () => {
  console.log("Server listening on port 3000");
});
