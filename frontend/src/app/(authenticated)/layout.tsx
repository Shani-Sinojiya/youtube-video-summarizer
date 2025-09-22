"use client";

import { AppSidebar } from "@/components/app-sidebar";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import VideoListProvider from "@/contexts/videolist";
import VideoModelProvider from "@/contexts/videomodel";
import { SessionProvider } from "next-auth/react";

import { PropsWithChildren } from "react";

export default function Layout({ children }: PropsWithChildren) {
  return (
    <SessionProvider>
      <VideoListProvider>
        <SidebarProvider
          style={
            {
              "--sidebar-width": "calc(var(--spacing) * 72)",
              "--header-height": "calc(var(--spacing) * 12)",
            } as React.CSSProperties
          }
        >
          <VideoModelProvider>
            <AppSidebar variant="inset" />
            <SidebarInset>{children}</SidebarInset>
          </VideoModelProvider>
        </SidebarProvider>
      </VideoListProvider>
    </SessionProvider>
  );
}
