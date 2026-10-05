import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HelaCare",
  description: "Source-grounded Sri Lankan traditional health knowledge assistant",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
