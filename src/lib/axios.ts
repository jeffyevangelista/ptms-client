import { refresh } from "@/features/auth/auth.api";
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

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config; // failed request, allowing it to be retried after handling the error.
    const { token, setCredentials, clearCredentials } = useStore.getState();
    console.log(token);
    
    if (error.response?.status === 403 && !originalRequest._retry) {
      originalRequest._retry = true; // marks this request as already retried

      if (token) {
        try {
          const refreshedToken = await refresh();

          setCredentials(refreshedToken.access);
          originalRequest.headers.Authorization = `Bearer ${refreshedToken.access}`;

          // retry the original request
          return api(originalRequest);
        } catch (error) {
          console.log("Session expired");
          clearCredentials();
          return Promise.reject(error);
        }
      }
    }

    if (error.response) {
      error.message = error.response.data.message ?? error.message;
    }
    return Promise.reject(error);
  }
);

export default api;
