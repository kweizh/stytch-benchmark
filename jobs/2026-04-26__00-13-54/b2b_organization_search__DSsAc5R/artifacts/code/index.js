const express = require("express");
const stytch = require("stytch");

const app = express();
app.use(express.json());

const projectId = process.env.STYTCH_B2B_PROJECT_ID;
const secret = process.env.STYTCH_B2B_SECRET;

if (!projectId || !secret) {
  throw new Error(
    "Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables."
  );
}

const env = projectId.includes("live") ? stytch.envs.live : stytch.envs.test;
const stytchClient = new stytch.B2BClient({
  project_id: projectId,
  secret,
  env,
});

app.post("/api/discovery/organizations", async (req, res) => {
  try {
    const { intermediate_session_token: intermediateSessionToken } = req.body || {};

    const response = await stytchClient.discovery.organizations.list({
      intermediate_session_token: intermediateSessionToken,
    });

    res.status(200).json({ organizations: response.organizations });
  } catch (error) {
    const statusCode = error?.status_code || 500;
    res.status(statusCode).json(error);
  }
});

app.listen(3000, () => {
  console.log("Server listening on port 3000");
});
