import { Toaster } from "@/components/ui/sonner";

const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      {children} <Toaster richColors position="top-center" />
    </>
  );
};

export default ToastProvider;
