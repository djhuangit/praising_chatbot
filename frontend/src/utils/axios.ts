import axios from 'axios';

// Set the base URL to your Render backend
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
axios.defaults.withCredentials = true;