import { Route, Routes } from "react-router";
import RootLayout from "./components/root-layout";
import LoginPage from "./pages/auth/LoginPage";
import DashboardLayout from "./components/dashboard-layout";
import DashboardPage from "./pages/DashboardPage";
function App() {
  return (
    <Routes>
      <Route path="/" element={<RootLayout />}>
        <Route index element={<LoginPage />} />
        {/* Dashboard Layout */}
        <Route element={<DashboardLayout />}>
          <Route path="dashboard" element={<DashboardPage />} />
          {/* rest of routes */}
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
