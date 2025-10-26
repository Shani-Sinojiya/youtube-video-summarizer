"use client";


import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import Link from "next/link";
import useSWR from "swr";

type items = {
  name: string;
  url: string;
}[];

type ChatHistory = {
  chat_id: string;
  video_id: string;
  created_at: string; // ISO timestamp
};

type ChatsResponse = ChatHistory[];

const fetcher = (url: string): Promise<ChatsResponse> =>
  fetch(url).then((res) => res.json());

export function NavChatList() {
  const { data, isLoading, error } = useSWR<ChatsResponse>(
    "/api/chats",
    fetcher,
    {
      refreshInterval: 1000 * 60 * 1,
    }
  );

  // console.log("Chat data:", dat);

  // Ensure data is an array before trying to map over it
  const chatData = Array.isArray(data) ? data : [];

  return (
    <SidebarGroup className="group-data-[collapsible=icon]:hidden">
      <SidebarGroupLabel>Chat History</SidebarGroupLabel>
      <SidebarMenu>
        {isLoading && <div className="text-muted">Loading...</div>}
        {error ? (
          <div className="text-red-500">Error loading chats</div>
        ) : chatData.length > 0 ? (
          chatData.map((item) => (
            <SidebarMenuItem key={item.chat_id}>
              <SidebarMenuButton asChild>
                <Link href={"/chat/" + item.video_id + "/" + item.chat_id}>
                  <span>{item.chat_id}</span>
                </Link>
              </SidebarMenuButton>
              {/* <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <SidebarMenuAction
                  showOnHover
                  className="data-[state=open]:bg-accent rounded-sm"
                >
                  <IconDots />
                  <span className="sr-only">More</span>
                </SidebarMenuAction>
              </DropdownMenuTrigger>
              <DropdownMenuContent
                className="w-24 rounded-lg"
                side={isMobile ? "bottom" : "right"}
                align={isMobile ? "end" : "start"}
              >
                <DropdownMenuItem>
                  <IconFolder />
                  <span>Open</span>
                </DropdownMenuItem>
                <DropdownMenuItem>
                  <IconShare3 />
                  <span>Share</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem variant="destructive">
                  <IconTrash />
                  <span>Delete</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu> */}
            </SidebarMenuItem>
          ))
        ) : (
          !isLoading && (
            <div className="text-muted-foreground text-sm">No chats yet</div>
          )
        )}
        {/* <SidebarMenuItem>
          <SidebarMenuButton className="text-sidebar-foreground/70">
            <IconDots className="text-sidebar-foreground/70" />
            <span>More</span>
          </SidebarMenuButton>
        </SidebarMenuItem> */}
      </SidebarMenu>
    </SidebarGroup>
  );
}
