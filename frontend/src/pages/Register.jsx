import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";

function getErrorMessage(error) {
  const detail = error.response?.data?.detail;

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        const field = Array.isArray(item.loc)
          ? item.loc[item.loc.length - 1]
          : "field";

        return `${field}: ${item.msg}`;
      })
      .join(" | ");
  }

  if (typeof detail === "string") {
    return detail;
  }

  if (detail && typeof detail === "object") {
    return detail.msg || JSON.stringify(detail);
  }

  return "Unable to register user.";
}

export default function Register() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [showPassword, setShowPassword] = useState(false);

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    role: "employee",
    organization_name: "",
  });

  const handleChange = (event) => {
    setForm((current) => ({
      ...current,
      [event.target.name]: event.target.value,
    }));
  };

  // Password validations
  const passwordChecks = {
    length: form.password.length >= 6,
    // uppercase: /[A-Z]/.test(form.password),
    // lowercase: /[a-z]/.test(form.password),
    // number: /[0-9]/.test(form.password),
  };

  const passwordStrength = Object.values(passwordChecks).filter(Boolean).length;

  const getStrengthLabel = () => {
    if (passwordStrength <= 1) return "Weak";
    if (passwordStrength <= 3) return "Medium";
    return "Strong";
  };

  const getStrengthColor = () => {
    if (passwordStrength <= 1) return "bg-red-500";
    if (passwordStrength <= 3) return "bg-yellow-500";
    return "bg-green-500";
  };

  const validateForm = () => {
    if (!form.name.trim()) {
      return "Name is required.";
    }

    if (!form.email.trim()) {
      return "Email is required.";
    }

    if (!form.password.trim()) {
      return "Password is required.";
    }

    // if (!passwordChecks.length) {
    //   return "Password must contain at least 8 characters.";
    // }

    // if (!passwordChecks.uppercase) {
    //   return "Password must contain an uppercase letter.";
    // }

    // if (!passwordChecks.lowercase) {
    //   return "Password must contain a lowercase letter.";
    // }

    // if (!passwordChecks.number) {
    //   return "Password must contain a number.";
    // }

    return null;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    const validationError = validateForm();

    if (validationError) {
      return setError(validationError);
    }

    try {
      setLoading(true);

      const payload = {
        ...form,
        organization_name:
          form.organization_name.trim() || undefined,
      };

      await API.post("/auth/register", payload);

      setSuccess("User registered successfully.");

      setTimeout(() => {
        navigate("/");
      }, 1200);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-white to-emerald-100 flex justify-center items-center px-4 py-10">
      
      <div className="w-full max-w-md">
        
        {/* Card */}
        <div className="bg-white shadow-2xl rounded-3xl overflow-hidden">
          
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-600 to-emerald-500 px-8 py-7 text-white">
            <h1 className="text-3xl font-bold">
              Create Account
            </h1>

            <p className="text-sm text-indigo-100 mt-2">
              Register new users and manage organization access.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-8">
            
            {/* Error */}
            {error && (
              <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded-xl mb-5 text-sm">
                {error}
              </div>
            )}

            {/* Success */}
            {success && (
              <div className="bg-green-100 border border-green-300 text-green-700 px-4 py-3 rounded-xl mb-5 text-sm">
                {success}
              </div>
            )}

            {/* Name */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Full Name
              </label>

              <input
                name="name"
                type="text"
                placeholder="Enter full name"
                value={form.name}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            {/* Email */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email Address
              </label>

              <input
                name="email"
                type="email"
                placeholder="Enter email address"
                value={form.email}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            {/* Password */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Password
              </label>

              <div className="relative">
                <input
                  name="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="Create strong password"
                  value={form.password}
                  onChange={handleChange}
                  className="w-full border border-gray-300 rounded-xl px-4 py-3 pr-16 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                />

                <button
                  type="button"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                  className="absolute right-4 top-3 text-sm text-indigo-600 font-medium"
                >
                  {showPassword ? "Hide" : "Show"}
                </button>
              </div>

              {/* Password Strength */}
              {form.password && (
                <div className="mt-4">
                  
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-medium text-gray-600">
                      Password Strength
                    </span>

                    <span className="text-xs font-bold text-gray-700">
                      {getStrengthLabel()}
                    </span>
                  </div>

                  <div className="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className={`h-full ${getStrengthColor()} transition-all duration-300`}
                      style={{
                        width: `${(passwordStrength / 4) * 100}%`,
                      }}
                    />
                  </div>

                  <div className="mt-3 space-y-1 text-xs">
                    <p
                      className={
                        passwordChecks.length
                          ? "text-green-600"
                          : "text-gray-500"
                      }
                    >
                      ✓ Minimum 8 characters
                    </p>

                    <p
                      className={
                        passwordChecks.uppercase
                          ? "text-green-600"
                          : "text-gray-500"
                      }
                    >
                      ✓ One uppercase letter
                    </p>

                    <p
                      className={
                        passwordChecks.lowercase
                          ? "text-green-600"
                          : "text-gray-500"
                      }
                    >
                      ✓ One lowercase letter
                    </p>

                    <p
                      className={
                        passwordChecks.number
                          ? "text-green-600"
                          : "text-gray-500"
                      }
                    >
                      ✓ One number
                    </p>
                  </div>
                </div>
              )}
            </div>

            {/* Role */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                User Role
              </label>

              <select
                name="role"
                value={form.role}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="employee">👨‍💻 Employee</option>
                <option value="manager">📋 Manager</option>
                <option value="admin">🛡️ Admin</option>
              </select>
            </div>

            {/* Organization */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Organization Name
              </label>

              <input
                name="organization_name"
                type="text"
                placeholder="Enter organization name"
                value={form.organization_name}
                onChange={handleChange}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            {/* Submit */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 to-emerald-500 hover:opacity-90 text-white font-semibold py-3 rounded-xl transition disabled:opacity-70"
            >
              {loading ? "Creating Account..." : "Create Account"}
            </button>

            {/* Footer */}
            <p className="text-center text-sm text-gray-500 mt-6">
              Already have an account?{" "}
              <button
                type="button"
                onClick={() => navigate("/")}
                className="text-indigo-600 font-semibold hover:underline"
              >
                Login
              </button>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}