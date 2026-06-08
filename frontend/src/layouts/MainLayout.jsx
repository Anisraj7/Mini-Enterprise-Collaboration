import { Outlet } from "react-router-dom";

import Navbar from "../components/Navbar";

export default function MainLayout() {
  return (
    <div className="min-h-screen bg-slate-100">
      <Navbar />

      <main className="p-6">
        <Outlet />
      </main>
    </div>
  );
}