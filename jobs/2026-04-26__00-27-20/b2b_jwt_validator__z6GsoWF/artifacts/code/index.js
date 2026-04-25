const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
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
    
    return res.status(200).json({ member_id: session.member_id });
  } catch (error) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
