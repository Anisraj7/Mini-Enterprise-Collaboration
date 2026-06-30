import API from "../../api/axios";

export const getMeetingSummary =
  async (meetingId) => {
    const { data } = await API.get(
      `/meetings/${meetingId}/summary`
    );

    return data;
  };

export const saveMeetingSummary = async (meetingId, payload) => {
  const { data } = await API.post(
    `/meetings/${meetingId}/summary`,
    payload
  );

  return data;
};