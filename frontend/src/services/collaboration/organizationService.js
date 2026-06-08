import api from "../../api/axios";
import { getPageItems } from "../../api/pagination";

/* =========================
   Organizations
========================= */

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

/* =========================
   Collaboration Settings
========================= */

export const getOrganizationSettings = async (
  organizationId
) => {
  const { data } = await api.get(
    `/organizations/${organizationId}/collaboration/settings`
  );

  return data;
};

export const updateOrganizationSettings = async (
  organizationId,
  payload
) => {
  const { data } = await api.put(
    `/organizations/${organizationId}/collaboration/settings`,
    payload
  );

  return data;
};

/* =========================
   Collaboration Usage
========================= */

export const getOrganizationUsage = async (
  organizationId
) => {
  const { data } = await api.get(
    `/organizations/${organizationId}/usage`
  );

  return data;
};

export const recalculateOrganizationUsage = async (
  organizationId
) => {
  const { data } = await api.post(
    `/organizations/${organizationId}/recalculate-usage`
  );

  return data;
};

export const onboardOrganization =
  async (payload) => {
    const { data } =
      await api.post(
        "/organizations/onboard",
        payload
      );

    return data;
  };

export const deleteOrganization = async (
  organizationId
) => {
  const { data } = await api.delete(
    `/organizations/${organizationId}`
  );

  return data;
};


export const getOnboardingStatus = async (
  organizationId
) => {
  const { data } = await api.get(
    `/organizations/${organizationId}/onboarding-status`
  );

  return data;
};