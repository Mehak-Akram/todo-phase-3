// Test script to verify proxy routes are working
// This would normally be run in a testing environment

import axios from 'axios';

// Test the proxy route
async function testProxyRoute() {
  try {
    // This would be tested when the Next.js app is running
    const response = await axios.post('http://localhost:3000/api/chat-proxy', {
      message: 'Hello, test message',
      conversation_id: null
    }, {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Proxy route test failed:', error);
  }
}

// Run the test
testProxyRoute();