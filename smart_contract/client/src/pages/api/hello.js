import axios from 'axios';

export default async function auth(wallet_address) {
  try {
    // Define headers
    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': 'http://localhost:3000',
    };

    // Define request body
    const requestBody = {
      wallet_address: wallet_address,
    };

    // Make POST request using Axios
    const response = await axios.post('/api/proxy/'
      'http://localhost:8000/api/v1/users/auth',
      requestBody,
      {
        headers: headers,
      }
    );

    return(response.data); // Set fetched data to state variable
  } catch (err) {
    console.log(err);
  }
}
