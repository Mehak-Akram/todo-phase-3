import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { message, conversation_id } = req.body;
    const token = req.headers.authorization;

    // Determine the backend URL and API path based on environment
    const baseUrl = process.env.NODE_ENV === 'development'
      ? 'http://localhost:8000'  // Local backend
      : process.env.NEXT_PUBLIC_API_URL; // Production backend

    // Both local and deployed versions use the same API path structure
    const apiPath = '/api/v1/chat';  // Consistent path for both environments

    console.log('Chat proxy: Forwarding request to:', `${baseUrl}${apiPath}`);
    console.log('Chat proxy: Headers being sent:', {
      'Content-Type': 'application/json',
      'Authorization': token ? 'BEARER_TOKEN_PRESENT' : 'NO_TOKEN'
    });
    console.log('Chat proxy: Request body:', { message, conversation_id });

    // Forward the request to the backend chat API
    const backendRes = await axios.post(
      `${baseUrl}${apiPath}`,
      { message, conversation_id },
      {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': token || '',
        },
        timeout: 30000, // 30 second timeout
      }
    );

    res.status(200).json(backendRes.data);
  } catch (error: any) {
    console.error('Chat proxy error details:');
    console.error('- Original error:', error.message);
    console.error('- Error code:', error.code);
    console.error('- Error response:', error.response?.data);
    console.error('- Error status:', error.response?.status);
    console.error('- Requested URL:', `${baseUrl}${apiPath}`);

    // Handle different types of errors
    if (error.code === 'ECONNREFUSED') {
      console.error('- Backend server may not be running on:', baseUrl);
      return res.status(500).json({
        error: `Backend server not reachable at ${baseUrl}. Please ensure the backend server is running.`,
        status: 500
      });
    } else if (error.response) {
      // Server responded with error status
      return res.status(error.response.status || 500).json({
        error: error.response.data?.detail || error.response.data || 'Backend server error',
        status: error.response.status || 500
      });
    } else if (error.request) {
      // Request was made but no response received
      return res.status(500).json({
        error: `No response from backend server at ${baseUrl}. Check if server is running and accessible.`,
        status: 500
      });
    } else {
      // Something else happened
      return res.status(500).json({
        error: `Request error: ${error.message}`,
        status: 500
      });
    }
  }
}