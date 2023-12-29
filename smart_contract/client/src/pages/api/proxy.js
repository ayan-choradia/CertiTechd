// pages/api/proxy.js
import axios from 'axios';

export default async function handler(req, res) {
  try {
    const { wallet_address } = req.body;

    const headers = {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
    };

    const response = await axios.post('http://localhost:8000/api/v1/', {
      wallet_address,
    }, {
      headers: headers,
    });

    res.status(response.status).json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json(error.response?.data || { message: 'Internal server error' });
  }
}
