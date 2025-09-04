import { useMutation } from "@tanstack/react-query";
import { login } from "./auth.api";
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
