import API from "../../api/axios";

export const getMeetingNotes = async (
  meetingId
) => {
  const { data } = await API.get(
    `/meetings/${meetingId}/notes`
  );

  return data;
};

export const createMeetingNote =
  async (meetingId, payload) => {
    const { data } = await API.post(
      `/meetings/${meetingId}/notes`,
      payload
    );

    return data;
  };

export const updateMeetingNote =
  async (noteId, payload) => {
    const { data } = await API.put(
      `/meeting-notes/${noteId}`,
      payload
    );

    return data;
  };