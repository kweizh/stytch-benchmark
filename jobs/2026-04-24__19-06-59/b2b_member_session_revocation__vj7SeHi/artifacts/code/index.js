const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

// Initialize Stytch B2B Client
// In a real application, these would be provided via environment variables
const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID || 'project-test-00000000-0000-0000-0000-000000000000',
  secret: process.env.STYTCH_SECRET || 'secret-test-00000000-0000-0000-0000-000000000000',
});

app.post('/revoke', async (req, res) => {
  const { session_token } = req.body;

  if (!session_token) {
    return res.status(400).json({ error: 'session_token is required' });
  }

  try {
    await client.sessions.revoke({ session_token });
    return res.status(200).send();
  } catch (error) {
    console.error('Error revoking session:', error);
    const statusCode = error.status_code || 500;
    return res.status(statusCode).json(error);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
