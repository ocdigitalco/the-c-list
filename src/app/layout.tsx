import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Inter, Inter_Tight, JetBrains_Mono } from "next/font/google";
import Script from "next/script";
import { Header } from "@/components/Header";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

const interTight = Inter_Tight({
  variable: "--font-inter-tight",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700", "800", "900"],
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains",
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
});

export const metadata: Metadata = {
  title: "Checklist2",
  description: "Sports card set explorer for collectors",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" data-theme="light">
      <head />
      <body
        className={`${geistSans.variable} ${geistMono.variable} ${inter.variable} ${interTight.variable} ${jetbrainsMono.variable} antialiased bg-zinc-950 text-zinc-100 h-screen flex flex-col overflow-hidden`}
      >
        <Header />
        <main className="flex-1 overflow-hidden">{children}</main>
        <Script
          src="https://www.googletagmanager.com/gtag/js?id=G-3T45WWZ64Y"
          strategy="afterInteractive"
        />
        <Script id="google-analytics" strategy="afterInteractive">
          {`window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-3T45WWZ64Y');`}
        </Script>
      </body>
    </html>
  );
}
