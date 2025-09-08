import api from "@/lib/axios";
import type { AuthCredentials } from "./auth.type";

export const login = async ({
  credentials,
}: {
  credentials: AuthCredentials;
}): Promise<{ access: string }> => {
  return (await api.post("/auth/login/", credentials)).data;
};

export const refresh = async (): Promise<{ access: string }> => {
  return (await api.get("/auth/refresh/")).data;
};
