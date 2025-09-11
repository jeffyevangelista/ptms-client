import { Button } from "@/components/ui/button";
import { useSidebar } from "@/components/ui/sidebar";
import UserAvatar from "@/features/auth/UserAvatar";
import { SidebarIcon } from "lucide-react";
import { ModeToggle } from "./mode-toggle";
import { Separator } from "./ui/separator";

export function SiteHeader() {
  const { toggleSidebar } = useSidebar();

  return (
    <header className="bg-background sticky top-0 z-50 flex w-full items-center border-b">
      <div className="flex h-(--header-height) w-full items-center justify-between gap-2 px-4">
        <Button
          className="h-8 w-8"
          variant="ghost"
          size="icon"
          onClick={toggleSidebar}
        >
          <SidebarIcon />
        </Button>

        <div className="flex items-center gap-1">
          <ModeToggle />
          <Separator orientation="vertical" className="h-auto w-1" />
          <UserAvatar />
        </div>
      </div>
    </header>
  );
}
