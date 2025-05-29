// api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8080', // Replace with your API base URL
  headers: {
    'Content-Type': 'application/json',
    // Add any additional headers you need here
  },
});

export default api;
