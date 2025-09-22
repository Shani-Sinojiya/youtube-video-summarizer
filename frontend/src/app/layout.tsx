import type { Metadata } from "next";
import { ThemeProvider } from "@/components/theme-provider";
import { WEB_APP_BASENAME, WEB_APP_DESCRIPTION } from "@/constants/web";
import "./globals.css";
import { Fragment } from "react";
import { Toaster } from "@/components/ui/sonner";

export const metadata: Metadata = {
  title: WEB_APP_BASENAME,
  description: WEB_APP_DESCRIPTION,
  openGraph: {
    title: WEB_APP_BASENAME,
    description: WEB_APP_DESCRIPTION,
  },
  twitter: {
    title: WEB_APP_BASENAME,
    description: WEB_APP_DESCRIPTION,
  },
};

interface RootLayoutProps {
  children: React.ReactNode;
}

export default function RootLayout({ children }: RootLayoutProps) {
  return (
    <Fragment>
      <html lang="en" suppressHydrationWarning>
        <head>
          <link
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap"
            rel="stylesheet"
          />
          <link
            rel="stylesheet"
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
          />
        </head>
        <body>
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
            {children}
            <Toaster position={"top-center"} />
          </ThemeProvider>
        </body>
      </html>
    </Fragment>
  );
}
