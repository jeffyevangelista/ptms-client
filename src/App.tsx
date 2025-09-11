import { Route, Routes } from "react-router";
import RootLayout from "@/components/root-layout";
import LoginPage from "@/pages/auth/LoginPage";
import DashboardLayout from "@/components/dashboard-layout";
import DashboardPage from "@/pages/DashboardPage";
import PersistAuth from "@/features/auth/PersistAuth";
import RedirectAuth from "@/features/auth/RedirectAuth";
import RequireAuth from "@/features/auth/RequireAuth";
import { accountRoles } from "./lib/roles";
import FundsPage from "./pages/funds/FundsPage";
import CompaniesPage from "./pages/companies/CompaniesPage";
import UsersPage from "./pages/users/UsersPage";
import ClusteringPage from "./pages/clustering/ClusteringPage";

function App() {
  return (
    <Routes>
      <Route element={<PersistAuth />}>
        <Route path="/" element={<RootLayout />}>
          <Route index element={<LoginPage />} />
          <Route
            element={
              <RequireAuth allowedRoles={[...Object.values(accountRoles)]} />
            }
          >
            {/* Dashboard Layout */}
            <Route element={<DashboardLayout />}>
              <Route path="dashboard" element={<DashboardPage />} />
              <Route path="companies" element={<CompaniesPage />} />
              <Route path="users" element={<UsersPage />} />
              <Route path="funds" element={<FundsPage />} />
              <Route path="clustering" element={<ClusteringPage />} />

              {/* rest of routes */}
            </Route>
          </Route>
        </Route>
      </Route>
    </Routes>
  );
}

export default App;
