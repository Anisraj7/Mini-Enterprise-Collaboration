import api from "../../api/axios";
import { getPageItems } from "../../api/pagination";

export const getOrganizationUsers =
  async () => {
    const { data } =
      await api.get(
        "/users"
      );

    return getPageItems(data);
  };

export const getOrganizationUser =
  async (userId) => {
    const { data } =
      await api.get(
        `/users/${userId}`
      );

    return data;
  };

export const createOrganizationUser =
  async (payload) => {
    const { data } =
      await api.post(
        "/users",
        payload
      );

    return data;
  };

export const updateOrganizationUser =
  async (
    userId,
    payload
  ) => {
    const { data } =
      await api.put(
        `/users/${userId}`,
        payload
      );

    return data;
  };

export const activateUser =
  async (userId) => {
    const { data } =
      await api.patch(
        `/users/${userId}/activate`
      );

    return data;
  };

export const deactivateUser =
  async (userId) => {
    const { data } =
      await api.patch(
        `/users/${userId}/deactivate`
      );

    return data;
  };