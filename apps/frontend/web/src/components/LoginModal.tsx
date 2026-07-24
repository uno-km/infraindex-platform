"use client";

import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';

export default function LoginModal() {
  const [isOpen, setIsOpen] = useState(false);
  const [isAdminMode, setIsAdminMode] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();

  useEffect(() => {
    const handleOpen = () => setIsOpen(true);
    window.addEventListener('open-login-modal', handleOpen);
    return () => window.removeEventListener('open-login-modal', handleOpen);
  }, []);

  if (!isOpen) return null;

  const handleClose = () => {
    setIsOpen(false);
    setIsAdminMode(false);
    setError('');
    setUsername('');
    setPassword('');
  };

  const handleAdminLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);

    try {
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);

      // Using NEXT_PUBLIC_API_URL or fallback
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${apiUrl}/api/v1/login/admin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Invalid credentials');
      }

      const data = await response.json();
      login(data.access_token);
      handleClose();
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSocialLogin = async (provider: string) => {
    setError('');
    setIsLoading(true);

    try {
      // Mock logic: Use provider name as oauth_id and a mock email
      const oauth_id = `mock_${provider}_id_123`;
      const email = `user@${provider}.com`;
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      
      const response = await fetch(`${apiUrl}/api/v1/login/social/${provider}?oauth_id=${oauth_id}&email=${email}`, {
        method: 'POST',
      });

      if (!response.ok) {
        throw new Error(`${provider} login failed`);
      }

      const data = await response.json();
      login(data.access_token);
      handleClose();
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-300">
      <div className="relative w-full max-w-md p-8 glass-panel border border-white/10 rounded-2xl shadow-2xl">
        <button
          onClick={handleClose}
          className="absolute top-4 right-4 text-white/50 hover:text-white transition-colors"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <div className="text-center mb-8">
          <h2 className="text-2xl font-bold text-white mb-2">
            Infra<span className="text-neon">Index</span>
          </h2>
          <p className="text-white/60 text-sm">
            {isAdminMode ? 'Admin Login' : 'Sign in to access premium features'}
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200 text-sm text-center">
            {error}
          </div>
        )}

        {isAdminMode ? (
          <form onSubmit={handleAdminLogin} className="space-y-4">
            <div>
              <input
                type="text"
                placeholder="Admin ID"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder:text-white/30 focus:outline-none focus:border-white/30 transition-colors"
                required
              />
            </div>
            <div>
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder:text-white/30 focus:outline-none focus:border-white/30 transition-colors"
                required
              />
            </div>
            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-3 bg-white/10 hover:bg-white/20 text-white font-medium rounded-lg transition-colors disabled:opacity-50"
            >
              {isLoading ? 'Logging in...' : 'Sign In as Admin'}
            </button>
            <div className="text-center mt-4">
              <button
                type="button"
                onClick={() => setIsAdminMode(false)}
                className="text-sm text-white/50 hover:text-white/80"
              >
                Back to User Login
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-3">
            <button
              onClick={() => handleSocialLogin('google')}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 bg-white hover:bg-gray-100 text-gray-900 font-medium rounded-lg transition-colors"
            >
              Continue with Google
            </button>
            <button
              onClick={() => handleSocialLogin('naver')}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 bg-[#03C75A] hover:bg-[#02b350] text-white font-medium rounded-lg transition-colors"
            >
              Continue with Naver
            </button>
            <button
              onClick={() => handleSocialLogin('kakao')}
              className="w-full flex items-center justify-center gap-3 px-4 py-3 bg-[#FEE500] hover:bg-[#e5ce00] text-gray-900 font-medium rounded-lg transition-colors"
            >
              Continue with Kakao
            </button>

            <div className="mt-6 pt-6 border-t border-white/10 text-center">
              <button
                onClick={() => setIsAdminMode(true)}
                className="text-sm text-white/50 hover:text-white/80 transition-colors"
              >
                Admin Login
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
