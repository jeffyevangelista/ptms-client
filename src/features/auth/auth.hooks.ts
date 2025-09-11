import { useMutation, useQuery } from "@tanstack/react-query";
import { getUserDetails, login, logout, refresh } from "./auth.apis";
import type { AuthCredentials } from "./auth.types";
import useStore from "@/store";
import { useNavigate } from "react-router";
import { toast } from "sonner";

export const useLogin = () => {
  const setCredentials = useStore((state) => state.setCredentials);
  const navigate = useNavigate();
  return useMutation({
    mutationKey: ["login"],
    mutationFn: (credentials: AuthCredentials) => login({ credentials }),
    onSuccess: (data) => {
      setCredentials(data.access);
      navigate("/dashboard");
    },
  });
};

export const useRefresh = () => {
  return useMutation({
    mutationKey: ["refresh"],
    mutationFn: () => refresh(),
  });
};

export const useLogout = () => {
  const navigate = useNavigate();

  return useMutation({
    mutationKey: ["logout"],
    mutationFn: () => logout(),
    onSuccess: () => {
      navigate("/");
      toast.success("Logged out");
    },
  });
};

export const useGetUserDetails = () => {
  return useQuery({
    queryKey: ["get-user-details"],
    queryFn: () => getUserDetails(),
  });
};
