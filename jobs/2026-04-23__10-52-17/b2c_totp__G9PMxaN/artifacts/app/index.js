const express = require("express");
const stytch = require("stytch");

const { STYTCH_PROJECT_ID, STYTCH_SECRET } = process.env;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  throw new Error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables.");
}

const env = STYTCH_PROJECT_ID.includes("test")
  ? stytch.envs.test
  : stytch.envs.live;

const stytchClient = new stytch.Client({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
  env,
});

const app = express();
app.use(express.json());

app.post("/users", async (req, res) => {
  try {
    const { email } = req.body;
    if (!email) {
      return res.status(400).json({ error: "email is required" });
    }

    const response = await stytchClient.users.create({ email });
    return res.json({ user_id: response.user_id });
  } catch (error) {
    console.error("/users error:", error);
    return res.status(500).json({ error: "Failed to create user" });
  }
});

app.post("/totp/enroll", async (req, res) => {
  try {
    const { user_id } = req.body;
    if (!user_id) {
      return res.status(400).json({ error: "user_id is required" });
    }

    const response = await stytchClient.totps.create({ user_id });
    return res.json({
      totp_id: response.totp_id,
      secret: response.secret,
    });
  } catch (error) {
    console.error("/totp/enroll error:", error);
    return res.status(500).json({ error: "Failed to enroll TOTP" });
  }
});

app.post("/totp/verify", async (req, res) => {
  try {
    const { user_id, totp_code } = req.body;
    if (!user_id || !totp_code) {
      return res.status(400).json({ error: "user_id and totp_code are required" });
    }

    const response = await stytchClient.totps.authenticate({
      user_id,
      totp_code,
      session_duration_minutes: 60,
    });

    return res.json({ session_token: response.session_token });
  } catch (error) {
    console.error("/totp/verify error:", error);
    return res.status(500).json({ error: "Failed to verify TOTP" });
  }
});

const port = 3000;
app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
