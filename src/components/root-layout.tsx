import { Outlet } from "react-router";

const RootLayout = () => {
  return (
    <div className="min-h-svh">
      <Outlet />
    </div>
  );
};

export default RootLayout;
