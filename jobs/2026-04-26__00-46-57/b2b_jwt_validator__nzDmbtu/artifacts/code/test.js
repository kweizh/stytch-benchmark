const axios = require('axios');

async function testValidation() {
  const testJwt = 'invalid-token-for-testing';
  
  try {
    const response = await axios.post('http://localhost:3000/validate', {
      session_jwt: testJwt
    });
    console.log('Response:', response.data);
  } catch (error) {
    if (error.response) {
      console.log('Status:', error.response.status);
      console.log('Data:', error.response.data);
    } else {
      console.error('Error:', error.message);
    }
  }
}

testValidation();
