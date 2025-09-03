import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { ThemeProvider } from "./components/theme-provider.tsx";
import RootLayout from "./components/root-layout.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider>
      <RootLayout>
        <App />
      </RootLayout>
    </ThemeProvider>
  </StrictMode>
);
