const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

app.post('/api/discovery/organizations', async (req, res) => {
  const { intermediate_session_token } = req.body;

  if (!intermediate_session_token) {
    return res.status(400).json({
      error_type: 'missing_parameter',
      error_message: 'intermediate_session_token is required'
    });
  }

  try {
    const response = await client.discovery.organizations.list({
      intermediate_session_token,
    });
    res.status(200).json(response);
  } catch (error) {
    // Propagate the error from Stytch
    const statusCode = error.status_code || 400;
    res.status(statusCode).json(error);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
