import type { Metadata } from "next";
import localFont from "next/font/local";
import { Header } from "@/components/Header";
import { AppShell } from "@/components/AppShell";
import { CookieConsent } from "@/components/CookieConsent";
import "./globals.css";

// All fonts self-hosted via next/font/local (latin woff2 in public/fonts/) — no
// next/font/google network fetch at build time. CSS variable names + weights are
// unchanged, so globals.css and all components are untouched. Geist, Geist Mono,
// Inter and JetBrains Mono are variable fonts (one woff2 per weight range).
const geistSans = localFont({
  src: "../../public/fonts/geist-latin.woff2",
  variable: "--font-geist-sans",
  weight: "100 900",
  display: "swap",
});

const geistMono = localFont({
  src: "../../public/fonts/geist-mono-latin.woff2",
  variable: "--font-geist-mono",
  weight: "100 900",
  display: "swap",
});

const inter = localFont({
  src: "../../public/fonts/inter-latin.woff2",
  variable: "--font-inter",
  weight: "400 700",
  display: "swap",
});

// Self-hosted Inter Tight (latin variable woff2) — no next/font/google network
// fetch at build time. Same CSS variable so globals.css / components are unchanged.
const interTight = localFont({
  src: "../../public/fonts/inter-tight-latin.woff2",
  variable: "--font-inter-tight",
  weight: "400 900",
  display: "swap",
});

const carterOne = localFont({
  src: "../../public/fonts/carter-one-latin.woff2",
  variable: "--font-carter-one",
  weight: "400",
  display: "swap",
});

const jetbrainsMono = localFont({
  src: "../../public/fonts/jetbrains-mono-latin.woff2",
  variable: "--font-jetbrains",
  weight: "400 700",
  display: "swap",
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
