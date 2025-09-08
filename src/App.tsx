import { Route, Routes } from "react-router";
import RootLayout from "@/components/root-layout";
import LoginPage from "@/pages/auth/LoginPage";
import DashboardLayout from "@/components/dashboard-layout";
import DashboardPage from "@/pages/DashboardPage";
import PersistAuth from "@/features/auth/PersistAuth";
import RedirectAuth from "@/features/auth/RedirectAuth";

function App() {
  return (
    <Routes>
      <Route element={<PersistAuth />}>
      <Route path="/" element={<RootLayout />}>
        <Route index element={<LoginPage />} />
        {/* <Route element={<RequireAuth allowedRoles={[]} />}> */}
        {/* Dashboard Layout */}
        <Route element={<DashboardLayout />}>
          <Route path="dashboard" element={<DashboardPage />} />
          {/* rest of routes */}
        </Route>
        {/* </Route> */}
      </Route>
      </Route>
    </Routes>
  );
}

export default App;
