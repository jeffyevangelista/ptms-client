import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useGetUserDetails } from "./auth.hooks";
import { Skeleton } from "@/components/ui/skeleton";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import LogoutButton from "./LogoutButton";

const UserAvatar = () => {
  const { isLoading, isError, error, data } = useGetUserDetails();

  if (isLoading) return <LoadingComponent />;

  if (isError) return <p className="text-destructive">{error.message}</p>;

  if (!data) return null;

  const firstNameInitial = data.first_name
    .trim()
    .split(" ")[0][0]
    .toUpperCase();
  const lastNameInitial = data.last_name.trim().split(" ")[0][0].toUpperCase();

  return (
    <DropdownMenu>
      <DropdownMenuTrigger>
        <div className="flex items-center gap-1">
          <Avatar>
            <AvatarFallback>
              {firstNameInitial}
              {lastNameInitial}
            </AvatarFallback>
          </Avatar>
          <div className="hidden flex-col items-start md:flex">
            <p className="text-md">
              {data.first_name} {data.last_name}
            </p>
            <p className="text-muted-foreground text-[10px]">{data.roles[0]}</p>
          </div>
        </div>
      </DropdownMenuTrigger>
      <DropdownMenuContent className="w-56" align="end">
        <div className="flex flex-col items-center py-2.5 md:hidden">
          <p className="text-lg">
            {data.first_name} {data.last_name}
          </p>
          <p className="text-muted-foreground text-[10px]">{data.roles[0]}</p>
        </div>
        <LogoutButton />
      </DropdownMenuContent>
    </DropdownMenu>
  );
};

const LoadingComponent = () => {
  return (
    <div className="flex items-center space-x-1">
      <Skeleton className="h-8 w-8 rounded-full" />
      <div className="space-y-1">
        <Skeleton className="h-4 w-36" />
        <Skeleton className="h-2 w-20" />
      </div>
    </div>
  );
};

export default UserAvatar;
