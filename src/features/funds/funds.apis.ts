import api from "@/lib/axios";

export const getFunds = async () => {
  return (await api.get("/Fund_view/")).data;
};

export const createFund = async (fundData: any) => {
  return (await api.post("/Fund_view/", fundData)).data;
};
