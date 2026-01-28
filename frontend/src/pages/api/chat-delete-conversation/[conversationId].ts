import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'DELETE') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  // Extract parameters from request
  const { conversationId } = req.query;

  // Determine the backend URL and API path based on environment
  const baseUrl = process.env.NODE_ENV === 'development'
    ? 'http://localhost:8000'  // Local backend
    : process.env.NEXT_PUBLIC_API_URL; // Production backend

  // Both local and deployed versions use the same API path structure
  const apiPath = '/api/v1/chat/conversations';  // Consistent path for both environments

  try {
    const token = req.headers.authorization;

    console.log('Delete conversation proxy: Forwarding request to:', `${baseUrl}${apiPath}/${conversationId}`);
    console.log('Delete conversation proxy: Headers being sent:', {
      'Content-Type': 'application/json',
      'Authorization': token ? 'BEARER_TOKEN_PRESENT' : 'NO_TOKEN'
    });

    // Forward the request to the backend chat API
    const backendRes = await axios.delete(
      `${baseUrl}${apiPath}/${conversationId}`,
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
    console.error('Delete conversation proxy error details:');
    console.error('- Original error:', error.message);
    console.error('- Error code:', error.code);
    console.error('- Error response:', error.response?.data);
    console.error('- Error status:', error.response?.status);
    console.error('- Requested URL:', `${baseUrl}${apiPath}/${conversationId}`);

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