import { Toaster } from "@/components/ui/sonner";

const ToastProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      {children} <Toaster position="bottom-center" />
    </>
  );
};

export default ToastProvider;
