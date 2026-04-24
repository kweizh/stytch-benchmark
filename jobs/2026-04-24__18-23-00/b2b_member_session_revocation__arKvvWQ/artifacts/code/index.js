const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_PROJECT_ID || 'project-test-00000000-0000-0000-0000-000000000000',
  secret: process.env.STYTCH_SECRET || 'secret-test-11111111-1111-1111-1111-111111111111',
});

app.post('/revoke', async (req, res) => {
  const { session_token } = req.body;
  
  if (!session_token) {
    return res.status(400).json({ error: 'session_token is required' });
  }

  try {
    const response = await client.sessions.revoke({ session_token });
    res.status(200).json(response);
  } catch (error) {
    console.error('Error revoking session:', error);
    res.status(error.status_code || 500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
