import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'InfraIndex | GPU Scanner',
  description: 'Global GPU Rental Price Intelligence Platform',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
