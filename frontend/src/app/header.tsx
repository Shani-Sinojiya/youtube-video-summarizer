import { NavActions } from "@/components/nav-actions";
import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbPage,
} from "@/components/ui/breadcrumb";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@radix-ui/react-separator";
import React from "react";

interface Props {
  title: string;
}

const Header = ({ title }: Props) => {
  return (
    <header className="flex h-12 sm:h-14 shrink-0 items-center gap-2 border-b">
      <div className="flex flex-1 items-center gap-2 px-2 sm:px-3">
        <SidebarTrigger className="h-6 w-6 sm:h-8 sm:w-8" />
        <Separator
          orientation="vertical"
          className="mr-2 data-[orientation=vertical]:h-3 sm:data-[orientation=vertical]:h-4"
        />
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem>
              <BreadcrumbPage className="line-clamp-1">
                <span className="text-sm sm:text-lg font-semibold">
                  {title}
                </span>
              </BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </div>
      <div className="ml-auto px-2 sm:px-3">
        <NavActions />
      </div>
    </header>
  );
};

export default Header;
