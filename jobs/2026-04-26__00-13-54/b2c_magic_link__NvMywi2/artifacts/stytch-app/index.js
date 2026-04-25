const express = require("express");
const stytch = require("stytch");

const app = express();
app.use(express.json());

const stytchClient = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
  env: stytch.envs.test,
});

app.post("/login", async (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.status(400).json({ success: false, error: "Email is required" });
  }

  try {
    await stytchClient.magicLinks.email.loginOrCreate({
      email,
      login_magic_link_url: "http://localhost:3000/authenticate",
      signup_magic_link_url: "http://localhost:3000/authenticate",
    });

    return res.json({ success: true });
  } catch (error) {
    return res.status(500).json({
      success: false,
      error: "Failed to send magic link",
    });
  }
});

app.get("/authenticate", async (req, res) => {
  const { token } = req.query;

  if (!token) {
    return res.status(400).json({ success: false, error: "Token is required" });
  }

  try {
    const response = await stytchClient.magicLinks.authenticate({ token });

    return res.json({ success: true, user_id: response.user_id });
  } catch (error) {
    return res.status(401).json({ success: false });
  }
});

app.listen(3000, () => {
  console.log("Stytch magic link server running on port 3000");
});
