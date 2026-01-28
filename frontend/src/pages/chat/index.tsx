import React from 'react';
import { ChatWindow } from '../../components/Chatbot/ChatWindow';
import Head from 'next/head';

const ChatPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>AI Chatbot - Todo Manager</title>
        <meta name="description" content="Chat with AI assistant to manage your todos" />
      </Head>

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-800 mb-6">AI Todo Assistant</h1>

          <div className="h-[600px]">
            <ChatWindow />
          </div>
        </div>
      </main>
    </div>
  );
};

export default ChatPage;