import api from "@/lib/axios";
import type { AuthCredentials, UserType } from "./auth.types";

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

export const logout = async () => {
  return (await api.post("/auth/logout/")).data;
};

export const getUserDetails = async (): Promise<UserType> => {
  return (await api.get("/auth/me/")).data;
};
