import API from "../../api/axios";

export const getMeetings = async (
  params = {}
) => {
  const { data } = await API.get(
    "/meetings",
    {
      params,
    }
  );

  return data;
};

export const getMeetingById = async (
  meetingId
) => {
  const { data } = await API.get(
    `/meetings/${meetingId}`
  );

  return data;
};

export const createMeeting = async (
  payload
) => {
  const { data } = await API.post(
    "/meetings",
    payload
  );

  return data;
};

export const updateMeeting = async (
  meetingId,
  payload
) => {
  const { data } = await API.put(
    `/meetings/${meetingId}`,
    payload
  );

  return data;
};

export const deleteMeeting = async (
  meetingId
) => {
  const { data } = await API.delete(
    `/meetings/${meetingId}`
  );

  return data;
};