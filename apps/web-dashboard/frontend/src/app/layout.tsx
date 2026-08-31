import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "PlanBee - Primavera P6 & Project Controls Suite",
  description: "Modern open-source web platform for Primavera P6 XER analytics, DCMA 14-Point audits, S-Curves, and Schedule Comparison",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased min-h-screen bg-slate-950 text-slate-100">
        {children}
      </body>
    </html>
  );
}
