import API from "../../api/axios";

export const getMeetingAttendees =
  async (meetingId) => {
    const { data } = await API.get(
      `/meetings/${meetingId}/attendees`
    );

    return data;
  };

export const addMeetingAttendee =
  async (meetingId, payload) => {
    const { data } = await API.post(
      `/meetings/${meetingId}/attendees`,
      payload
    );

    return data;
  };

export const removeMeetingAttendee =
  async (meetingId, userId) => {
    const { data } = await API.delete(
      `/meetings/${meetingId}/attendees/${userId}`
    );

    return data;
  };