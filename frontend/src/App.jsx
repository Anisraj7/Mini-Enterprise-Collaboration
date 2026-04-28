import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import CreateTask from "./pages/CreateTask";
import ProtectedRoute from "./components/ProtectedRoute";
import AssignTask from "./pages/AssignTask";
import EditTask from "./pages/EditTask";
import Register from "./pages/Register";
import Users from "./pages/Users";
import KanbanBoard from "./pages/KanbanBoard";


function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />

        <Route
          path="/create-task"
          element={
            <ProtectedRoute>
              <CreateTask />
            </ProtectedRoute>
          }
        />
        <Route path="/" element={<Login />} />
        <Route
          path="/tasks/:id/assign"
          element={
            <ProtectedRoute>
              <AssignTask />
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks/:id/edit"
          element={
            <ProtectedRoute>
              <EditTask />
            </ProtectedRoute>
          }
        />  
        <Route path="/register" element={<Register />} />
        <Route
          path="/users"
          element={
            <ProtectedRoute>
              <Users />
            </ProtectedRoute>
          }
        />
         <Route path="/kanban" element={<KanbanBoard />} />

        

      </Routes>
    </BrowserRouter>

    
  );
}

export default App;
