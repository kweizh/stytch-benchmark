const express = require('express');
const { B2BClient } = require('stytch');

const app = express();
app.use(express.json());

const client = new B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

app.post('/api/discovery/organizations', async (req, res) => {
  const { intermediate_session_token } = req.body;

  if (!intermediate_session_token) {
    return res.status(400).json({ error: 'intermediate_session_token is required' });
  }

  try {
    const response = await client.discovery.organizations.list({
      intermediate_session_token,
    });
    return res.status(200).json(response);
  } catch (error) {
    return res.status(400).json(error);
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
