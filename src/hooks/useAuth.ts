import type { DecodedToken } from "@/features/auth/auth.type";
import useStore from "@/store";
import { jwtDecode } from "jwt-decode";
import { useMemo } from "react";

const useAuth = () => {
  const token = useStore((state) => state.token);

  return useMemo(() => {
    if (!token) {
      return {
        email: null,
        roles: [],
        status: "Guest",
        isAdmin: false,
        isUser: false,
      };
    }

    try {
      const decoded: DecodedToken = jwtDecode(token);
      const { email, roles } = decoded.user;

      const isAdmin = roles.includes("admin");
      const isUser = roles.includes("user");

      return {
        email,
        roles,
        status: isAdmin ? "Admin" : "User",
        isAdmin,
        isUser,
      };
    } catch {
      return {
        email: null,
        roles: [],
        status: "Invalid",
        isAdmin: false,
        isUser: false,
      };
    }
  }, [token]);
};

export default useAuth;
