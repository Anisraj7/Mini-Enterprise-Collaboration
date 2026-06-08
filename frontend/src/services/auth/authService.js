import api from "../../api/axios";

export const register = async (data) => {
  const response = await api.post(
    "/auth/register",
    data
  );

  return response.data;
};

export const login = async (
  email,
  password
) => {
  const formData =
    new URLSearchParams();

  formData.append(
    "username",
    email
  );

  formData.append(
    "password",
    password
  );

  const response = await api.post(
    "/auth/login",
    formData,
    {
      headers: {
        "Content-Type":
          "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
};

export const getMe =
  async () => {
    const response =
      await api.get(
        "/auth/me"
      );

    return response.data;
  };

export const refreshToken =
  async (refreshToken) => {
    const response =
      await api.post(
        "/auth/refresh",
        {
          refresh_token:
            refreshToken,
        }
      );

    return response.data;
  };