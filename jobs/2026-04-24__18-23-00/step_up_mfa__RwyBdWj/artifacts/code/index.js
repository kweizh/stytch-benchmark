const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

app.post('/transfer', async (req, res) => {
  const { session_token } = req.body;
  
  if (!session_token) {
    return res.status(401).send('Unauthorized');
  }

  try {
    const response = await client.sessions.authenticate({ session_token });
    
    const factors = response.session?.authentication_factors || [];
    
    if (factors.length >= 2) {
      return res.status(200).json({ success: true });
    } else {
      return res.status(403).json({ error: 'Step-up MFA required' });
    }
  } catch (error) {
    return res.status(401).send('Unauthorized');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
