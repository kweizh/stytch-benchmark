const express = require("express");
const stytch = require("stytch");

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID || "",
  secret: process.env.STYTCH_SECRET || "",
});

app.post("/revoke", async (req, res) => {
  const { session_token } = req.body;

  if (!session_token) {
    return res.status(400).json({ error: "session_token is required" });
  }

  try {
    await client.sessions.revoke({ session_token });
    return res.status(200).json({ message: "Session revoked successfully" });
  } catch (err) {
    const status = err.status_code || 500;
    return res.status(status).json({ error: err.error_message || "Failed to revoke session" });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
