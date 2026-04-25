const express = require("express");
const stytch = require("stytch");

const { STYTCH_B2B_PROJECT_ID, STYTCH_B2B_SECRET } = process.env;

if (!STYTCH_B2B_PROJECT_ID || !STYTCH_B2B_SECRET) {
  console.error("Missing STYTCH_B2B_PROJECT_ID or STYTCH_B2B_SECRET environment variables.");
  process.exit(1);
}

const client = new stytch.B2BClient({
  project_id: STYTCH_B2B_PROJECT_ID,
  secret: STYTCH_B2B_SECRET
});

const app = express();
app.use(express.json());

app.post("/validate", async (req, res) => {
  const { session_jwt: sessionJwt } = req.body ?? {};

  if (!sessionJwt || typeof sessionJwt !== "string") {
    return res.status(400).json({ error: "session_jwt is required" });
  }

  try {
    const memberSession = await client.sessions.authenticateJwtLocal({
      session_jwt: sessionJwt
    });

    return res.status(200).json({ member_id: memberSession.member_id });
  } catch (error) {
    return res.sendStatus(401);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Stytch B2B JWT validator listening on port ${PORT}`);
});
