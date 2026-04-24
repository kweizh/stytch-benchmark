const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID || 'project-test-00000000-0000-0000-0000-000000000000',
  secret: process.env.STYTCH_B2B_SECRET || 'secret-test-00000000-0000-0000-0000-000000000000',
});

app.post('/validate', async (req, res) => {
  const { session_jwt } = req.body;

  if (!session_jwt) {
    return res.status(401).json({ error: 'Missing session_jwt' });
  }

  try {
    const session = await client.sessions.authenticateJwtLocal({
      session_jwt,
    });

    if (session && session.member_id) {
      return res.status(200).json({ member_id: session.member_id });
    } else {
      return res.status(401).json({ error: 'Invalid session' });
    }
  } catch (error) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
