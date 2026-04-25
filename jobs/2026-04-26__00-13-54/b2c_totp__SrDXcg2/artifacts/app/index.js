const express = require("express");
const stytch = require("stytch");

const { STYTCH_PROJECT_ID, STYTCH_SECRET } = process.env;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  throw new Error("Missing STYTCH_PROJECT_ID or STYTCH_SECRET environment variables");
}

const env = STYTCH_PROJECT_ID.includes("live")
  ? stytch.envs.live
  : stytch.envs.test;

const stytchClient = new stytch.B2CClient({
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

    const response = await stytchClient.users.create({
      email,
    });

    return res.json({ user_id: response.user_id });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

app.post("/totp/enroll", async (req, res) => {
  try {
    const { user_id: userId } = req.body;
    if (!userId) {
      return res.status(400).json({ error: "user_id is required" });
    }

    const response = await stytchClient.otps.totp.create({
      user_id: userId,
    });

    return res.json({
      totp_id: response.totp_id,
      secret: response.secret,
    });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

app.post("/totp/verify", async (req, res) => {
  try {
    const { user_id: userId, totp_code: totpCode } = req.body;
    if (!userId || !totpCode) {
      return res.status(400).json({ error: "user_id and totp_code are required" });
    }

    const response = await stytchClient.otps.totp.authenticate({
      user_id: userId,
      totp_code: totpCode,
      session_duration_minutes: 60,
    });

    return res.json({ session_token: response.session_token });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log("Server listening on port 3000");
});
