import axios, { AxiosResponse } from 'axios';
import { AuthResponse, TodoResponse, User, Todo } from '../types';

// Check if we should include the /api prefix based on environment variable
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://mehak-akram-todo-app-chatbot.hf.space';
const USE_API_PREFIX = process.env.NEXT_PUBLIC_USE_API_PREFIX === 'true';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Clear auth data and redirect to login
      if (typeof window !== 'undefined') {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/auth/signin';
      }
    }
    return Promise.reject(error);
  }
);

// Helper function to get the correct path based on API prefix configuration
function getApiPath(path: string): string {
  return USE_API_PREFIX ? `/api${path}` : path;
}

// Auth API functions
export const authAPI = {
  signup: (email: string, password: string): Promise<AxiosResponse<AuthResponse>> => {
    return api.post(getApiPath('/signup'), { email, password });
  },

  signin: (email: string, password: string): Promise<AxiosResponse<AuthResponse>> => {
    return api.post(getApiPath('/signin'), { email, password });
  },

  signout: (): Promise<AxiosResponse<{ message: string }>> => {
    return api.post(getApiPath('/signout'));
  },
};

// Todo API functions
export const todoAPI = {
  getTodos: (): Promise<AxiosResponse<{ todos: Todo[] }>> => {
    return api.get(getApiPath('/todos'));
  },

  createTodo: (content: string): Promise<AxiosResponse<Todo>> => {
    return api.post(getApiPath('/todos'), { content });
  },

  updateTodo: (id: string, content: string): Promise<AxiosResponse<Todo>> => {
    return api.put(getApiPath(`/todos/${id}`), { content });
  },

  deleteTodo: (id: string): Promise<AxiosResponse<{ message: string }>> => {
    return api.delete(getApiPath(`/todos/${id}`));
  },

  toggleTodoComplete: (id: string, completed: boolean): Promise<AxiosResponse<Todo>> => {
    return api.patch(getApiPath(`/todos/${id}/complete`), { completed });
  },
};

export default api;