"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

interface AuthState {
  token: string | null;
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthState>({
  token: null,
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const storedToken = localStorage.getItem('infraindex_token');
    if (storedToken) {
      setToken(storedToken);
    }
  }, []);

  const login = (newToken: string) => {
    localStorage.setItem('infraindex_token', newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem('infraindex_token');
    setToken(null);
  };

  const isAuthenticated = !!token;

  if (!mounted) {
    return <>{children}</>;
  }

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
