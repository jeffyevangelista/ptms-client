import { useMutation } from "@tanstack/react-query";
import { login } from "./auth.api";
import type { AuthCredentials } from "./auth.type";
import useStore from "@/store";

export const useLoginMutation = () => {
  const { setCredentials } = useStore.getState();

  return useMutation({
    mutationKey: ["login"],
    mutationFn: (credentials: AuthCredentials) => login({ credentials }),
    onSuccess: (data) => {
      setCredentials(data.access);
    },
  });
};
