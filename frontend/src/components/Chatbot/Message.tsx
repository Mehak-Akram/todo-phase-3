import React from 'react';

interface MessageProps {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export const Message: React.FC<MessageProps> = ({ role, content, timestamp }) => {
  const isUser = role === 'user';

  // Format timestamp for display
  const formattedTime = new Date(timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  });

  return (
    <div className={`flex mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-xs md:max-w-md lg:max-w-lg rounded-lg p-3 ${
          isUser
            ? 'text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 rounded-br-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all duration-300 shadow-md'
            : 'bg-gray-200 text-gray-800 rounded-bl-none'
        }`}
      >
        <div className="whitespace-pre-wrap">{content}</div>
        <div
          className={`text-xs mt-1 ${
            isUser ? 'text-blue-200' : 'text-gray-500'
          }`}
        >
          {formattedTime}
        </div>
      </div>
    </div>
  );
};