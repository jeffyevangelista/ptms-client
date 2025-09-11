import { DropdownMenuItem } from "@/components/ui/dropdown-menu";
import { LogOut } from "lucide-react";
import { useLogout } from "./auth.hooks";

const LogoutButton = () => {
  const { isPending, mutateAsync: logout } = useLogout();

  return (
    <DropdownMenuItem
      disabled={isPending}
      onClick={() => logout()}
      variant="destructive"
    >
      Logout
      <LogOut className="ml-auto" />
    </DropdownMenuItem>
  );
};

export default LogoutButton;
