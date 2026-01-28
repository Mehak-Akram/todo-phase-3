import { User } from '../types';
import { authAPI } from './api';

class AuthService {
  private user: User | null = null;

  constructor() {
    this.loadUserFromStorage();
  }

  private loadUserFromStorage() {
    // Check if we're in the browser environment
    if (typeof window !== 'undefined') {
      const storedUser = localStorage.getItem('user');
      const token = localStorage.getItem('token');

      if (storedUser && token) {
        this.user = JSON.parse(storedUser);
      }
    }
  }

  async signup(email: string, password: string): Promise<{ user: User; token: string }> {
    try {
      const response = await authAPI.signup(email, password);
      const { user, token } = response.data;

      // Store user and token
      this.user = user;
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('token', token);
      }

      return { user, token };
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Signup failed');
    }
  }

  async signin(email: string, password: string): Promise<{ user: User; token: string }> {
    try {
      const response = await authAPI.signin(email, password);
      const { user, token } = response.data;

      // Store user and token
      this.user = user;
      if (typeof window !== 'undefined') {
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('token', token);
      }

      return { user, token };
    } catch (error: any) {
      throw new Error(error.response?.data?.error || 'Signin failed');
    }
  }

  signout(): void {
    this.user = null;
    if (typeof window !== 'undefined') {
      localStorage.removeItem('user');
      localStorage.removeItem('token');
    }
  }

  getCurrentUser(): User | null {
    return this.user;
  }

  isAuthenticated(): boolean {
    if (typeof window !== 'undefined') {
      return this.user !== null && localStorage.getItem('token') !== null;
    }
    return false; // Return false if not in browser environment
  }

  getToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('token');
    }
    return null; // Return null if not in browser environment
  }
}

export const authService = new AuthService();