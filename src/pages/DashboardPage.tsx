import { Button } from "@/components/ui/button";
import { useRefreshMutation } from "@/features/auth/auth.hook";

const DashboardPage = () => {
  const { mutateAsync: refresh, isPending } = useRefreshMutation();

  return (
    <div>
      <Button disabled={isPending} onClick={() => refresh()}>Refresh token</Button>
    </div>
  );
};

export default DashboardPage;
