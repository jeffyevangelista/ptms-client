import { useGetFunds } from "./funds.hooks";

const FundsList = () => {
  const { data, isLoading, isError, error } = useGetFunds();

  if (isLoading) return <p>loading...</p>;

  if (isError) {
    console.log(error);
    return <p>{error.message}</p>;
  }

  return <div>{JSON.stringify(data)}</div>;
};

export default FundsList;
