const stytch = require('stytch');
const client = new stytch.B2BClient({
  project_id: "project-test-00000000-0000-0000-0000-000000000000",
  secret: "secret-test-11111111-1111-1111-1111-111111111111",
});
console.log(Object.getOwnPropertyNames(Object.getPrototypeOf(client.fraud.fingerprint)));
