const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.B2BClient({
  project_id: process.env.STYTCH_B2B_PROJECT_ID,
  secret: process.env.STYTCH_B2B_SECRET,
});

app.post('/api/discovery/organizations', async (req, res) => {
  try {
    const { intermediate_session_token } = req.body;
    
    const response = await client.discovery.organizations.list({
      intermediate_session_token
    });
    
    res.status(200).json(response);
  } catch (error) {
    if (error.status_code) {
      return res.status(error.status_code).json({
        status_code: error.status_code,
        request_id: error.request_id,
        error_type: error.error_type,
        error_message: error.error_message,
        error_url: error.error_url
      });
    }
    
    return res.status(400).json({ error: error.message || 'Unknown error' });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
