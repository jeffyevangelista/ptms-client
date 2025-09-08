import useStore from "@/store";
import { useEffect, useState } from "react";
import { useRefreshMutation } from "./auth.hook";
import { Loader } from "lucide-react";
import { Outlet } from "react-router";

const PersistAuth = () => {
  const { token } = useStore();
  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const { mutateAsync: refresh, isPending } = useRefreshMutation();

  useEffect(() => {
    let isMounted = true;

    const verifyRefreshToken = async () => {
      console.log("verifying refresh token");
      try {
        await refresh();
      } catch (err) {
        console.log("Error verifying token", token);
        // navigate("/", { replace: true }); // Redirect to login if refresh fails
      } finally {
        if (isMounted) setIsCheckingAuth(false); // Allow rendering to continue
      }
    };

    if (!token) {
      verifyRefreshToken();
    } else {
      setIsCheckingAuth(false);
    }

    return () => {
      isMounted = false;
    };
  }, []);

  if (isCheckingAuth || isPending)
    return (
      <div className="flex h-screen items-center">
        <Loader className="mx-auto animate-spin" />
      </div>
    );

  return <Outlet />;
};

export default PersistAuth;
