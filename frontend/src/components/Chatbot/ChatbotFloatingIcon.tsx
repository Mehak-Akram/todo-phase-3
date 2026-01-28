import React, { useState } from 'react';
import { ChatWindow } from './ChatWindow';

interface ChatbotFloatingIconProps {
  userId?: string;
  onTodoChange?: () => void;
}

export const ChatbotFloatingIcon: React.FC<ChatbotFloatingIconProps> = ({ userId, onTodoChange }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-30 backdrop-blur-sm z-40" onClick={closeChat}></div>
      )}

      {isOpen && (
        <div className="fixed bottom-20 right-6 w-full max-w-md h-[500px] bg-white rounded-lg shadow-xl border border-gray-200 z-50 transform transition-transform duration-300 ease-in-out">
          <div className="flex flex-col h-full">
            {/* Header */}
            <div className="flex justify-between items-center p-4 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-t-lg">
              <h3 className="font-semibold">AI Assistant</h3>
              <button
                onClick={closeChat}
                className="text-white hover:text-gray-200 focus:outline-none"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
              </button>
            </div>

            {/* Chat Window */}
            <div className="flex-1 overflow-hidden">
              <ChatWindow userId={userId} onTodoChange={onTodoChange} />
            </div>
          </div>
        </div>
      )}

      {/* Floating Icon */}
      <button
        onClick={toggleChat}
        className={`w-16 h-16 rounded-full flex items-center justify-center shadow-lg transform transition-all duration-300 ease-in-out ${
          isOpen
            ? 'bg-red-500 rotate-90'
            : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700'
        }`}
        aria-label={isOpen ? "Close chat" : "Open chat"}
      >
        {isOpen ? (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        ) : (
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
          </svg>
        )}
      </button>
    </div>
  );
};