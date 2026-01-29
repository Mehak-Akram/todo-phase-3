import axios from 'axios';

const CHAT_API_BASE_URL = process.env.NEXT_PUBLIC_CHAT_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL;

interface SendMessageParams {
  message: string;
  conversation_id?: string;
}

interface SendMessageResponse {
  conversation_id: string;
  message_id: string;
  response: string;
  timestamp: string;
  tool_calls: any[];
  error: string | null;
}

// Create axios instance for direct API calls to HuggingFace backend
const api = axios.create({
  baseURL: `${CHAT_API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json'
  }
});

class ChatApi {
  async sendMessage(
    message: string,
    conversationId?: string
  ): Promise<SendMessageResponse> {
    try {
      const token = localStorage.getItem('token');

      const response = await api.post<SendMessageResponse>(
        '/chat/',  // Direct route to HuggingFace backend
        {
          message,
          conversation_id: conversationId
        },
        {
          headers: {
            Authorization: token ? `Bearer ${token}` : undefined
          }
        }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          (error.response?.data as any)?.detail || 'Failed to send message'
        );
      }
      throw new Error('Network error occurred while sending message');
    }
  }

  async getConversations(): Promise<any[]> {
    try {
      const token = localStorage.getItem('token');

      const response = await api.get<any[]>(
        '/chat/conversations',  // Direct route to HuggingFace backend
        {
          headers: {
            Authorization: token ? `Bearer ${token}` : undefined
          }
        }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          (error.response?.data as any)?.detail || 'Failed to fetch conversations'
        );
      }
      throw new Error('Network error occurred while fetching conversations');
    }
  }

  async getConversationMessages(conversationId: string): Promise<any> {
    try {
      const token = localStorage.getItem('token');

      const response = await api.get<any>(
        `/chat/conversations/${conversationId}/messages`,  // Direct route to HuggingFace backend
        {
          headers: {
            Authorization: token ? `Bearer ${token}` : undefined
          }
        }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          (error.response?.data as any)?.detail ||
            'Failed to fetch conversation messages'
        );
      }
      throw new Error('Network error occurred while fetching conversation messages');
    }
  }

  async deleteConversation(
    conversationId: string
  ): Promise<{ success: boolean; deleted_messages_count: number }> {
    try {
      const token = localStorage.getItem('token');

      const response = await api.delete<{
        success: boolean;
        deleted_messages_count: number;
      }>(
        `/chat/conversations/${conversationId}`,  // Direct route to HuggingFace backend
        {
          headers: {
            Authorization: token ? `Bearer ${token}` : undefined
          }
        }
      );

      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        throw new Error(
          (error.response?.data as any)?.detail ||
            'Failed to delete conversation'
        );
      }
      throw new Error('Network error occurred while deleting conversation');
    }
  }
}

export const chatApi = new ChatApi();
