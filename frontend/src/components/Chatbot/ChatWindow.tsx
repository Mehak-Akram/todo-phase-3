import React, { useState, useEffect, useRef } from 'react';
import { Message } from './Message';
import { InputArea } from './InputArea';
import { chatApi } from '../../services/api/chatApi';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

interface ChatWindowProps {
  userId?: string;
  onTodoChange?: () => void;
}

export const ChatWindow: React.FC<ChatWindowProps> = ({ userId, onTodoChange }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Get user ID from localStorage if not provided as prop
  const effectiveUserId = userId || (() => {
    try {
      const userData = localStorage.getItem('user');
      if (userData) {
        const parsed = JSON.parse(userData);
        return parsed.id;
      }
    } catch (e) {
      console.warn('Could not parse user data from localStorage:', e);
    }
    return undefined;
  })();

  // Load conversation history on component mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        // Load recent conversation if available
        // For now, we'll start with an empty conversation
        setMessages([
          {
            id: 'welcome-1',
            role: 'assistant',
            content: 'Hello! I\'m your AI assistant for managing todos. You can ask me to create, retrieve, update, or delete your todos using natural language.',
            timestamp: new Date().toISOString()
          }
        ]);
      } catch (err) {
        setError('Failed to load conversation history');
      }
    };

    loadHistory();
  }, []);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (messageText: string) => {
    if (!messageText.trim() || isLoading) return;

    try {
      setIsLoading(true);
      setError(null);

      // Add user message to UI immediately
      const userMessage: Message = {
        id: `temp-${Date.now()}`,
        role: 'user',
        content: messageText,
        timestamp: new Date().toISOString()
      };

      setMessages(prev => [...prev, userMessage]);

      // Send message to backend
      const response = await chatApi.sendMessage(messageText);

      // Add AI response to messages
      const aiMessage: Message = {
        id: response.message_id,
        role: 'assistant',
        content: response.response,
        timestamp: response.timestamp
      };

      setMessages(prev => [...prev, aiMessage]);

      // Trigger UI refresh after chat interaction
      // Since we want to be more aggressive, we'll refresh on any response that mentions todos
      if (onTodoChange) {
        // Check if the AI response indicates a todo action was performed
        const isTodoAction = checkIfTodoAction(response.response);

        // Always trigger refresh if it looks like a todo was created/modified, regardless of certainty
        if (isTodoAction || response.response.toLowerCase().includes('todo')) {
          // Retry mechanism to ensure the todo is saved before refreshing
          const refreshWithRetry = async (retriesLeft: number) => {
            try {
              await onTodoChange();
            } catch (error) {
              if (retriesLeft > 0) {
                setTimeout(() => refreshWithRetry(retriesLeft - 1), 1500); // Shorter delay between retries
              } else {
                console.error('Failed to refresh todos after multiple attempts', error);
              }
            }
          };

          // Wait for backend to process, then refresh with retry
          setTimeout(() => refreshWithRetry(2), 1000); // Shorter initial delay
        }
      }
    } catch (err) {
      setError('Failed to send message. Please try again.');
      console.error('Error sending message:', err);

      // Remove the temporary user message if there was an error
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to detect if the AI response mentions todo changes
  const checkIfTodoAction = (aiResponse: string): boolean => {
    const lowerResponse = aiResponse.toLowerCase();

    // Look for any indication that a todo was created/modified regardless of specific wording
    const todoCreationIndicators = [
      'todo', 'task', 'to-do', 'to do', 'add', 'create', 'make', 'new',
      'buy', 'get', 'purchase', 'pick up', 'complete', 'done', 'finished',
      'created', 'added', 'made', 'completed', 'deleted', 'removed', 'updated',
      'successfully', 'for you', 'in your list', 'to your list'
    ];

    // Check if any of the indicators appear in the response
    const hasTodoIndicator = todoCreationIndicators.some(indicator =>
      lowerResponse.includes(indicator)
    );

    // Look for specific success patterns that indicate a todo operation completed
    const successPatterns = [
      /created.*(?:todo|task|item)/i,
      /added.*(?:todo|task|item)/i,
      /made.*(?:todo|task|item)/i,
      /successfully.*(create|add|make)/i,
      /(?:todo|task).*created/i,
      /in.*list/i,
      /for you/i
    ];

    const hasSuccessPattern = successPatterns.some(pattern =>
      pattern.test(aiResponse)
    );

    // Be more aggressive in detecting todo actions - if there's any hint, return true
    return hasTodoIndicator || hasSuccessPattern;
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-lg shadow-md">
      <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
        {error && (
          <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
            {error}
          </div>
        )}

        {messages.map((message) => (
          <Message
            key={message.id}
            role={message.role}
            content={message.content}
            timestamp={message.timestamp}
          />
        ))}

        {isLoading && (
          <div className="flex items-center mb-4">
            <div className="ml-2 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white p-3 rounded-lg max-w-xs md:max-w-md lg:max-w-lg">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-75"></div>
                <div className="w-2 h-2 bg-white rounded-full animate-bounce delay-150"></div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="border-t p-4 bg-white">
        <InputArea onSend={handleSendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};