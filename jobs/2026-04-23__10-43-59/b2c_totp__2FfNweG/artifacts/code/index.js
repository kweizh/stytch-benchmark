const express = require('express');
const stytch = require('stytch');

const app = express();
app.use(express.json());

const client = new stytch.Client({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

app.post('/users', async (req, res) => {
  try {
    const { email } = req.body;
    const response = await client.users.create({
      email: email,
    });
    res.json({ user_id: response.user_id });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/totp/enroll', async (req, res) => {
  try {
    const { user_id } = req.body;
    const response = await client.totps.create({
      user_id: user_id,
    });
    res.json({ totp_id: response.totp_id, secret: response.secret });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.post('/totp/verify', async (req, res) => {
  try {
    const { user_id, totp_code } = req.body;
    const response = await client.totps.authenticate({
      user_id: user_id,
      totp_code: totp_code,
      session_duration_minutes: 60
    });
    res.json({ session_token: response.session_token });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
