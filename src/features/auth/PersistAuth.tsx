import useStore from "@/store";
import { useEffect, useRef, useState } from "react";
import { useRefresh } from "./auth.hooks";
import { Loader } from "lucide-react";
import { Outlet, useNavigate } from "react-router";
import { NODE_ENV } from "@/lib/env";

const PersistAuth = () => {
  const { token, clearCredentials, setCredentials } = useStore();
  const { isPending, mutateAsync: refresh } = useRefresh();
  const effectRan = useRef(false);
  const [_, setTrueSuccess] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (effectRan.current === true || NODE_ENV !== "development") {
      const verifyRefreshToken = async () => {
        console.log("verifying refresh token");
        try {
          const data = await refresh();
          setCredentials(data.access);
          setTrueSuccess(true);
        } catch (error) {
          console.log(error);
          clearCredentials();
          navigate("/");
        }
      };

      if (!token) verifyRefreshToken();
    }
    return () => {
      effectRan.current = true;
    };
  }, []);

  // useEffect(() => {
  // if (isError) {
  //   console.log(error.message, isError);
  //   clearCredentials();
  //   navigate("/");
  // }
  // }, [isError, error]);

  // if (isError) {
  //   return (
  //     <div>
  //       <Alert className="mx-auto w-full max-w-screen-sm" variant="destructive">
  //         <CircleX />
  //         <AlertTitle>Error</AlertTitle>
  //         <AlertDescription>{error.message}</AlertDescription>
  //       </Alert>
  //       <Button onClick={() => navigate("/")}>Login in again</Button>
  //     </div>
  //   );
  // }

  if (isPending)
    return (
      <div className="flex h-screen items-center">
        <Loader className="mx-auto animate-spin" />
      </div>
    );

  return <Outlet />;
};

export default PersistAuth;
