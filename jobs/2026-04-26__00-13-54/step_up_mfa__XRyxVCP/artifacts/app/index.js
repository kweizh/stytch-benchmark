const express = require("express");
const stytch = require("stytch");

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

app.post("/transfer", async (req, res) => {
  const { session_token: sessionToken } = req.body || {};

  if (!sessionToken) {
    return res.status(400).json({ error: "session_token is required" });
  }

  try {
    const { session } = await client.sessions.authenticate({
      session_token: sessionToken,
    });

    const factorCount = Array.isArray(session.authentication_factors)
      ? session.authentication_factors.length
      : 0;

    if (factorCount < 2) {
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
