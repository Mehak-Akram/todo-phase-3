import axios, { AxiosResponse } from 'axios';
import { AuthResponse, TodoResponse, User, Todo } from '../types';

// Base URL for the main backend API (both todo and auth endpoints are on the same backend)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const USE_API_PREFIX = process.env.NEXT_PUBLIC_USE_API_PREFIX === 'true';

// Create axios instance for main API (todos and auth)
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

// Auth API functions
export const authAPI = {
  signup: (email: string, password: string): Promise<AxiosResponse<AuthResponse>> => {
    return api.post('/api/signup', { email, password });
  },

  signin: (email: string, password: string): Promise<AxiosResponse<AuthResponse>> => {
    return api.post('/api/signin', { email, password });
  },

  signout: (): Promise<AxiosResponse<{ message: string }>> => {
    return api.post('/api/signout');
  },
};

// Todo API functions
export const todoAPI = {
  getTodos: (): Promise<AxiosResponse<Todo[]>> => {
    return api.get('/api/todos');
  },

  createTodo: (content: string): Promise<AxiosResponse<Todo>> => {
    return api.post('/api/todos', { content });
  },

  updateTodo: (id: string, content: string): Promise<AxiosResponse<Todo>> => {
    return api.put(`/api/todos/${id}`, { content });
  },

  deleteTodo: (id: string): Promise<AxiosResponse<{ message: string }>> => {
    return api.delete(`/api/todos/${id}`);
  },

  toggleTodoComplete: (id: string, completed: boolean): Promise<AxiosResponse<Todo>> => {
    return api.patch(`/api/todos/${id}/complete`, { completed });
  },
};

export default api;