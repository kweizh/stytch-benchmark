const express = require("express");
const stytch = require("stytch");

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

app.post("/api/discovery/organizations", async (req, res) => {
  const { intermediate_session_token } = req.body;

  if (!intermediate_session_token) {
    return res.status(400).json({
      error_type: "missing_intermediate_session_token",
      error_message: "intermediate_session_token is required in the request body",
    });
  }

  try {
    const response = await client.discovery.organizations.list({
      intermediate_session_token,
    });

    return res.status(200).json(response);
  } catch (err) {
    const statusCode = err.status_code || 400;
    return res.status(statusCode).json({
      error_type: err.error_type || "unknown_error",
      error_message: err.error_message || err.message || "An error occurred",
      error_url: err.error_url,
      request_id: err.request_id,
    });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
