import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'InfraIndex | GPU Scanner',
  description: 'Global GPU Rental Price Intelligence Platform',
};

import { AuthProvider } from '../context/AuthContext';
import LoginModal from '../components/LoginModal';

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <AuthProvider>
          {children}
          <LoginModal />
        </AuthProvider>
      </body>
    </html>
  );
}
