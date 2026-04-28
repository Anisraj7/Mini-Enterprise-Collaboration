import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";


export default function Register() {
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "employee",
  });

  const handleChange = (event) => {
    setForm((current) => ({ ...current, [event.target.name]: event.target.value }));
  };

  const handleSubmit = async () => {
    setError("");
    try {
      await API.post("/auth/register", form);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to register user.");
    }
  };

  return (
    <div className="flex justify-center items-center h-screen bg-gray-100">
      <div className="bg-white p-6 shadow rounded w-96">
        <h2 className="text-xl mb-4">Register User</h2>

        <input
          name="name"
          placeholder="Name"
          className="border p-2 w-full mb-3"
          value={form.name}
          onChange={handleChange}
        />

        <input
          name="email"
          placeholder="Email"
          className="border p-2 w-full mb-3"
          value={form.email}
          onChange={handleChange}
        />

        <input
          name="password"
          type="password"
          placeholder="Password"
          className="border p-2 w-full mb-3"
          value={form.password}
          onChange={handleChange}
        />

        <select
          name="role"
          className="border p-2 w-full mb-3"
          value={form.role}
          onChange={handleChange}
        >
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
          <option value="admin">Admin</option>
        </select>

        {error && <p className="text-sm text-red-600 mb-3">{error}</p>}

        <button
          onClick={handleSubmit}
          className="bg-green-500 text-white w-full py-2"
        >
          Create User
        </button>
      </div>
    </div>
  );
}
