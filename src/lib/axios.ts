import { refresh } from "@/features/auth/auth.apis";
import { API_URL } from "@/lib/env";
import useStore from "@/store";
import axios from "axios";

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

api.interceptors.request.use(
  (config) => {
    const { token } = useStore.getState();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const { token, setCredentials, clearCredentials } = useStore.getState();

    if (
      (error.response?.status === 401 || error.response?.status === 403) &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      if (token) {
        try {
          const refreshedToken = await refresh();
          setCredentials(refreshedToken.access);
          originalRequest.headers.Authorization = `Bearer ${refreshedToken.access}`;
          return api(originalRequest);
        } catch (err) {
          console.log("Session expired, clearing credentials");
          clearCredentials();
          return Promise.reject(err);
        }
      }
    }

    if (error.response) {
      error.message = error.response.data.message ?? error.message;
    }
    return Promise.reject(error);
  },
);

export default api;
