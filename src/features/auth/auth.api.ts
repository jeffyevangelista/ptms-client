import axiosInstance from "@/lib/axios";
import type { AuthCredentials } from "./auth.type";

export const login = async ({
  credentials,
}: {
  credentials: AuthCredentials;
}): Promise<{ access: string }> => {
  return (await axiosInstance.post("/auth/login/", credentials)).data;
};
