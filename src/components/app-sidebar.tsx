import { NavProjects } from "@/components/nav-projects";
import { Sidebar, SidebarContent } from "@/components/ui/sidebar";
import {
  Building,
  CircleDollarSign,
  Group,
  LayoutDashboard,
  UsersRound,
} from "lucide-react";

const data = {
  projects: [
    {
      name: "Dashboard",
      url: "/dashboard",
      icon: LayoutDashboard,
    },
    {
      name: "Companies",
      url: "/companies",
      icon: Building,
    },
    {
      name: "Users",
      url: "/users",
      icon: UsersRound,
    },
    {
      name: "Funds",
      url: "/funds",
      icon: CircleDollarSign,
    },
    {
      name: "Clustering",
      url: "/clustering",
      icon: Group,
    },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  return (
    <Sidebar
      className="top-(--header-height) h-[calc(100svh-var(--header-height))]!"
      {...props}
    >
      <SidebarContent>
        <NavProjects projects={data.projects} />
      </SidebarContent>
    </Sidebar>
  );
}
