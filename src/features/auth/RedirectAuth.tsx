import useStore from "@/store";

import { Navigate, useLocation } from "react-router";

const RedirectAuth = ({
  children,
  fallbackPath = "/",
}: {
  children: React.ReactNode;
  fallbackPath?: string;
}) => {
  const { isAuthenticated } = useStore();
  const location = useLocation();

  if (isAuthenticated) {
    const comingFrom = location.state?.from?.pathname || fallbackPath;
    return <Navigate to={comingFrom} replace />;
  }
  return children;
};

export default RedirectAuth;
