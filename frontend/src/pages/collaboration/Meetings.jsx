import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  getMeetings,
  createMeeting,
  deleteMeeting,
} from "../../services/collaboration/meetingService";

import { getProjects } from "../../services/collaboration/projectService";

const STATUS_COLORS = {
  SCHEDULED: "bg-blue-100 text-blue-800",
  COMPLETED: "bg-green-100 text-green-800",
  CANCELLED: "bg-red-100 text-red-800",
};

export default function Meetings() {
  const [meetings, setMeetings] = useState([]);

  const [loading, setLoading] = useState(true);
  const [projects, setProjects] = useState([]);

  const [formData, setFormData] = useState({
    project_id: "",
    title: "",
    description: "",
    start_time: "",
    end_time: "",
  });

  const loadMeetings = async () => {
    try {
      setLoading(true);

      const [meetingsResponse, projectsResponse] = await Promise.all([
        getMeetings(),
        getProjects(),
      ]);

      setMeetings(
        Array.isArray(meetingsResponse)
          ? meetingsResponse
          : meetingsResponse.items || [],
      );

      setProjects(
        Array.isArray(projectsResponse)
          ? projectsResponse
          : projectsResponse.items || [],
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMeetings();
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createMeeting(formData);

      setFormData({
        project_id: "",
        title: "",
        description: "",
        start_time: "",
        end_time: "",
      });

      loadMeetings();
    } catch (error) {
      console.log("Status:", error.response?.status);
      console.log("Response:", error.response?.data);
      console.error(error);
    }
  };

  const handleDelete = async (meetingId) => {
    try {
      await deleteMeeting(meetingId);

      loadMeetings();
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <div className="p-6">Loading meetings...</div>;
  }


  
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Meetings</h1>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <select
            name="project_id"
            value={formData.project_id}
            onChange={handleChange}
            className="border rounded px-3 py-2"
            required
          >
            <option value="">Select Project</option>

            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>

          <input
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Meeting Title"
            className="border rounded px-3 py-2"
          />

          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Description"
            className="border rounded px-3 py-2 col-span-2"
          />

          <input
            type="datetime-local"
            name="start_time"
            value={formData.start_time}
            onChange={handleChange}
            className="border rounded px-3 py-2"
          />

          <input
            type="datetime-local"
            name="end_time"
            value={formData.end_time}
            onChange={handleChange}
            className="border rounded px-3 py-2"
          />

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Create Meeting
          </button>
        </form>
      </div>

      <div className="grid gap-4">
        {meetings.map((meeting) => (
          <div key={meeting.id} className="bg-white border rounded-lg p-4">
            <div className="flex justify-between">
              <div>
                <h2 className="font-semibold text-lg">{meeting.title}</h2>

                <p className="text-gray-600">{meeting.description}</p>

                <p className="text-sm text-gray-500 mt-2">
                  {meeting.start_time}
                </p>
              </div>

              <span
                className={`px-2 py-1 rounded text-xs ${
                  STATUS_COLORS[meeting.status]
                }`}
              >
                {meeting.status}
              </span>
            </div>

            <div className="mt-4 flex gap-4">
              <Link to={`/meetings/${meeting.id}`} className="text-blue-600">
                View
              </Link>

              <button
                onClick={() => handleDelete(meeting.id)}
                className="text-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        ))}

        {!meetings.length && (
          <div className="bg-white border rounded-lg p-6 text-center">
            No meetings found
          </div>
        )}
      </div>
    </div>
  );
}
