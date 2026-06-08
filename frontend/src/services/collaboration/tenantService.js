import api from "../../api/axios";
import { getPageItems } from "../../api/pagination";

export const getOrganizations = async () => {
  const { data } = await api.get(
    "/organizations"
  );

  return getPageItems(data);
};

export const getOrganizationById = async (
  organizationId
) => {
  const { data } = await api.get(
    `/organizations/${organizationId}`
  );

  return data;
};

export const createOrganization = async (
  payload
) => {
  const { data } = await api.post(
    "/organizations",
    payload
  );

  return data;
};

export const updateOrganization = async (
  organizationId,
  payload
) => {
  const { data } = await api.put(
    `/organizations/${organizationId}`,
    payload
  );

  return data;
};

export const suspendOrganization =
  async (organizationId) => {
    const { data } = await api.patch(
      `/organizations/${organizationId}/suspend`
    );

    return data;
  };

export const activateOrganization =
  async (organizationId) => {
    const { data } = await api.patch(
      `/organizations/${organizationId}/activate`
    );

    return data;
  };