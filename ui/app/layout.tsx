import type { Metadata } from "next";
import Sidebar from "@/components/Sidebar";
import "./globals.css";

export const metadata: Metadata = {
  title: "CrossSystemEval",
  description:
    "Measuring professional-standard fidelity across roles in LLM deployment",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="flex min-h-screen bg-surface font-sans text-ink antialiased">
        <Sidebar />
        {children}
      </body>
    </html>
  );
}
