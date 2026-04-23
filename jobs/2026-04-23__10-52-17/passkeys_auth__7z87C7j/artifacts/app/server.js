const express = require("express");
const stytch = require("stytch");

const app = express();
app.use(express.json());

const stytchClient = new stytch.B2CClient({
  project_id: process.env.STYTCH_PROJECT_ID,
  secret: process.env.STYTCH_SECRET,
});

const sendStytchResponse = async (res, callback) => {
  try {
    const response = await callback();
    res.json(response);
  } catch (error) {
    res.json(error);
  }
};

app.post("/webauthn/register/start", (req, res) => {
  const { user_id, domain } = req.body;
  return sendStytchResponse(res, () =>
    stytchClient.webauthn.registerStart({
      user_id,
      domain,
      use_base64_url_encoding: true,
    })
  );
});

app.post("/webauthn/register", (req, res) => {
  const { user_id, public_key_credential } = req.body;
  return sendStytchResponse(res, () =>
    stytchClient.webauthn.register({
      user_id,
      public_key_credential,
    })
  );
});

app.post("/webauthn/authenticate/start", (req, res) => {
  const { domain } = req.body;
  return sendStytchResponse(res, () =>
    stytchClient.webauthn.authenticateStart({
      domain,
    })
  );
});

app.post("/webauthn/authenticate", (req, res) => {
  const { public_key_credential } = req.body;
  return sendStytchResponse(res, () =>
    stytchClient.webauthn.authenticate({
      public_key_credential,
    })
  );
});

app.listen(3000, () => {
  console.log("Server listening on port 3000");
});
