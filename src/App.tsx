import { Route, Routes } from "react-router";
import RootLayout from "./components/root-layout";
import LoginPage from "./pages/auth/LoginPage";
function App() {
  return (
    <Routes>
      <Route path="/" element={<RootLayout />}>
        <Route index element={<LoginPage />} />
      </Route>
    </Routes>
  );
}

export default App;
