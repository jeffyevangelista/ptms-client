import axiosInstance from ".";

export const login = async () => {
  return (await axiosInstance.get("")).data;
};
