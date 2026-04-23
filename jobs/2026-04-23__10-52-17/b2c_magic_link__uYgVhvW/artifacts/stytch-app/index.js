const express = require("express");
const stytch = require("stytch");

const { STYTCH_PROJECT_ID, STYTCH_SECRET, STYTCH_ENV } = process.env;

if (!STYTCH_PROJECT_ID || !STYTCH_SECRET) {
  throw new Error("STYTCH_PROJECT_ID and STYTCH_SECRET must be set");
}

const env = STYTCH_ENV === "live" ? stytch.envs.live : stytch.envs.test;

const stytchClient = new stytch.Client({
  project_id: STYTCH_PROJECT_ID,
  secret: STYTCH_SECRET,
  env,
});

const app = express();
app.use(express.json());

app.post("/login", async (req, res) => {
  const { email } = req.body || {};

  if (!email) {
    return res.status(400).json({ error: "email is required" });
  }

  try {
    await stytchClient.magicLinks.email.loginOrCreate({
      email,
      login_magic_link_url: "http://localhost:3000/authenticate",
      signup_magic_link_url: "http://localhost:3000/authenticate",
    });

    return res.json({ success: true });
  } catch (error) {
    return res.status(500).json({ error: "Failed to send magic link" });
  }
});

app.get("/authenticate", async (req, res) => {
  const { token } = req.query || {};

  if (!token) {
    return res.status(400).json({ error: "token is required" });
  }

  try {
    const response = await stytchClient.magicLinks.authenticate({
      token,
    });

    return res.json({ success: true, user_id: response.user_id });
  } catch (error) {
    return res.status(401).json({ success: false });
  }
});

app.listen(3000, () => {
  console.log("Stytch app listening on http://localhost:3000");
});
