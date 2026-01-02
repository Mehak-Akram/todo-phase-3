import { useState } from 'react';
import { authService } from '../../services/auth';

interface LoginFormProps {
  onSuccess: () => void;
}

export default function LoginForm({ onSuccess }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      await authService.signin(email, password);
      onSuccess();
    } catch (err: any) {
      setError(err.message || 'An error occurred during sign in');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-gradient-to-b from-blue-400 to-indigo-600">
      {/* Animated background elements */}
      <div className="absolute inset-0 z-0">
        {/* Wavy background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -left-40 w-80 h-80 bg-white/10 rounded-full blur-3xl"></div>
          <div className="absolute -bottom-40 -right-40 w-80 h-80 bg-purple-500/20 rounded-full blur-3xl"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-blue-300/10 rounded-full blur-3xl"></div>
        </div>

        {/* Wavy lines */}
        <div className="absolute inset-0">
          <svg className="w-full h-full" viewBox="0 0 1200 600" preserveAspectRatio="none">
            <path
              d="M0,300 Q300,200 600,300 T1200,300 V600 H0 Z"
              fill="rgba(255,255,255,0.05)"
            />
            <path
              d="M0,400 Q300,300 600,400 T1200,400 V600 H0 Z"
              fill="rgba(255,255,255,0.03)"
            />
          </svg>
        </div>
      </div>

      {/* Bird logo in top-left corner */}
      <div className="absolute top-4 left-4 z-20">
        <div className="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-full flex items-center justify-center">
          <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C13.1 2 14 2.9 14 4C14 5.1 13.1 6 12 6C10.9 6 10 5.1 10 4C10 2.9 10.9 2 12 2ZM21 9V7L15 1L13.5 2.5L16.17 5.17C15.24 5.06 14.32 5 13.38 5C10.38 5 7.61 6.19 5.54 8.26L7 9.72C8.63 8.09 10.96 7 13.38 7C15.8 7 18.13 8.09 19.76 9.72L21 9ZM1 9L2.24 7.76C3.87 6.13 6.2 5 8.62 5C11.04 5 13.37 6.13 15 7.76L16.46 6.26C14.39 4.19 11.62 3 8.62 3C5.61 3 2.84 4.19 0.76 6.26L2.21 7.71L1 9ZM12 10C8.69 10 5.73 11.8 4.22 14.58L2.71 13.07C4.66 9.89 8.21 8 12 8C15.79 8 19.34 9.89 21.29 13.07L19.78 14.58C18.27 11.8 15.31 10 12 10ZM12 12C14.21 12 16 13.79 16 16C16 18.21 14.21 20 12 20C9.79 20 8 18.21 8 16C8 13.79 9.79 12 12 12Z"/>
          </svg>
        </div>
      </div>

      {/* Glassmorphism container */}
      <div className="max-w-md w-full space-y-8 p-8 rounded-3xl bg-white/10 backdrop-blur-lg border border-white/20 shadow-2xl relative z-10">
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white mb-2">
            Sign In
          </h2>
          <p className="text-white/80">
            Don't have an account?{' '}
            <a href="/signup" className="text-white hover:underline">
              Sign up
            </a>
          </p>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-6">
          {error && (
            <div className="rounded-lg bg-red-500/20 p-4 border border-red-500/30">
              <div className="flex items-center">
                <svg className="h-5 w-5 text-red-300 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span className="text-red-200 text-sm">{error}</span>
              </div>
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-white/80 mb-1">
                Email
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent backdrop-blur-sm"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-white/80 mb-1">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-white/10 border border-white/30 rounded-xl text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:border-transparent backdrop-blur-sm"
                placeholder="Enter your password"
              />
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                className="h-4 w-4 text-blue-500 focus:ring-blue-400 border-white/30 rounded bg-white/10"
              />
              <label htmlFor="remember-me" className="ml-2 block text-sm text-white/80">
                Remember me
              </label>
            </div>

            <div className="text-sm">
              <a href="#" className="text-white/80 hover:text-white">
                Forgot password?
              </a>
            </div>
          </div>

          {/* Circular sign in button */}
          <div className="flex justify-center mt-8">
            <button
              type="submit"
              className="w-16 h-16 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 flex items-center justify-center text-white font-bold text-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 border-4 border-white/20"
            >
              →
            </button>
          </div>
        </form>

        <div className="mt-8">
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-white/20"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-transparent text-white/60">
                Or continue with
              </span>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-3 gap-3">
            <a href="#" className="w-full flex justify-center py-3 border border-white/20 rounded-xl bg-white/10 hover:bg-white/20 transition-colors duration-300 backdrop-blur-sm">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12.24 10.285V14.4h6.806c-.275 1.765-2.056 5.174-6.806 5.174-4.095 0-7.439-3.389-7.439-7.574s3.345-7.574 7.439-7.574c2.33 0 3.891.989 4.785 1.849l3.254-3.138C18.189 1.186 15.479 0 12.24 0c-6.635 0-12 5.365-12 12s5.365 12 12 12c6.926 0 11.52-4.869 11.52-11.726 0-.788-.085-1.39-.189-1.989H12.24z"/>
              </svg>
            </a>

            <a href="#" className="w-full flex justify-center py-3 border border-white/20 rounded-xl bg-white/10 hover:bg-white/20 transition-colors duration-300 backdrop-blur-sm">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
              </svg>
            </a>

            <a href="#" className="w-full flex justify-center py-3 border border-white/20 rounded-xl bg-white/10 hover:bg-white/20 transition-colors duration-300 backdrop-blur-sm">
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}