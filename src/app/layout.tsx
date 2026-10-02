import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Carter_One, Inter, JetBrains_Mono } from "next/font/google";
import localFont from "next/font/local";
import { Header } from "@/components/Header";
import { AppShell } from "@/components/AppShell";
import { CookieConsent } from "@/components/CookieConsent";
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

// Self-hosted Inter Tight (latin variable woff2) — no next/font/google network
// fetch at build time. Same CSS variable so globals.css / components are unchanged.
const interTight = localFont({
  src: "../../public/fonts/inter-tight-latin.woff2",
  variable: "--font-inter-tight",
  weight: "400 900",
  display: "swap",
});

const carterOne = Carter_One({
  variable: "--font-carter-one",
  subsets: ["latin"],
  weight: ["400"],
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
    <html
      lang="en"
      data-theme="light"
      className={`${geistSans.variable} ${geistMono.variable} ${inter.variable} ${interTight.variable} ${carterOne.variable} ${jetbrainsMono.variable}`}
    >
      <head />
      <body
        className="antialiased bg-zinc-950 text-zinc-100 h-screen flex flex-col overflow-hidden"
      >
        <Header />
        <AppShell>{children}</AppShell>
        {/* Google Analytics is loaded by CookieConsent only after Analytics
            consent (Consent Mode v2, denied defaults). No unconditional load. */}
        <CookieConsent />
      </body>
    </html>
  );
}
