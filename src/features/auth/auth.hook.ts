import { useMutation } from "@tanstack/react-query";
import { login, refresh } from "./auth.api";
import type { AuthCredentials } from "./auth.type";
import useStore from "@/store";
import { useNavigate } from "react-router";

export const useLoginMutation = () => {
  const { setCredentials } = useStore.getState();
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

export const useRefreshMutation = () => {
  const { setCredentials } = useStore.getState();

  return useMutation({
    mutationKey: ["refresh"],
    mutationFn: refresh,

    onSuccess: (data) => {
      console.log(data.access);
      
      setCredentials(data.access);
    },
    onError: (error, variables, context) => {
      console.log({ error, variables, context });
    },
  });
};
