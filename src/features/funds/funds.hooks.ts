import { useMutation, useQuery } from "@tanstack/react-query";
import { createFund, getFunds } from "./funds.apis";
import useStore from "@/store";
import { queryClient } from "@/providers/QueryProvider";

export const useGetFunds = () => {
  const { token } = useStore.getState();
  return useQuery({
    queryKey: ["get-funds"],
    queryFn: () => getFunds(),
    enabled: !!token,
  });
};

export const useCreateFund = () => {
  return useMutation({
    mutationKey: ["create-fund"],
    mutationFn: (fundData: any) => createFund(fundData),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["get-funds"] });
    },
  });
};
