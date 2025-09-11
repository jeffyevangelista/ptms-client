import type { DecodedToken } from "@/features/auth/auth.types";
import { jwtDecode } from "jwt-decode";
import type { StateCreator } from "zustand";

type AuthState = {
  authUser: null | any;
  token: null | string;
  isAuthenticated: boolean;
};

type AuthAction = {
  setCredentials: (token: string) => void;
  clearCredentials: () => void;
  setAuthUser: (authUser: any) => void;
};

export type AuthSlice = AuthState & AuthAction;

const initialState: AuthState = {
  authUser: null,
  token: null,
  isAuthenticated: false,
};

const createAuthSlice: StateCreator<AuthSlice> = (set) => ({
  ...initialState,
  setCredentials: (token: string) => {
    const { user: authUser } = jwtDecode<DecodedToken>(token);
    set({
      authUser,
      token,
      isAuthenticated: true,
    });
  },
  setAuthUser: (authUser) => set({ authUser }),
  clearCredentials: () => set(initialState),
});

export default createAuthSlice;
