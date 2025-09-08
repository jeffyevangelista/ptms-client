import { memo } from "react";
import { useLocation, Navigate, Outlet } from "react-router";
import useAuth from "@/hooks/useAuth";

const RequireAuth = ({ allowedRoles }: { allowedRoles: string[] }) => {
  const location = useLocation();
  const { roles } = useAuth();

  // Convert allowedRoles to a Set for faster lookup
  const allowedSet = new Set(allowedRoles);

  const isAuthorized = roles?.some((role) => allowedSet.has(role));

  if (isAuthorized) {
    return <Outlet />;
  }

  return <Navigate to="/dashboard" state={{ from: location }} replace />;
};

export default memo(RequireAuth);
