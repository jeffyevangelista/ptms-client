import React from "react";

const RootLayout = ({ children }: { children: React.ReactNode }) => {
  return <div className="min-h-svh">{children}</div>;
};

export default RootLayout;
