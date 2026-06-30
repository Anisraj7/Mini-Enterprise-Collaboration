import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { getMeetingById } from "../../services/collaboration/meetingService";

import {
  getMeetingAttendees,
  addMeetingAttendee,
  removeMeetingAttendee,
} from "../../services/collaboration/meetingAttendeeService";

import {
  getMeetingNotes,
  createMeetingNote,
} from "../../services/collaboration/meetingNoteService";

import {
  getMeetingSummary,
  saveMeetingSummary,
} from "../../services/collaboration/aiMeetingSummaryService";

import { getUsers } from "../../services/collaboration/memberService";

export default function MeetingDetails() {
  const { meetingId } = useParams();

  const [meeting, setMeeting] = useState(null);
  const [users, setUsers] = useState([]);

  const [attendees, setAttendees] = useState([]);

  const [notes, setNotes] = useState([]);

  const [summary, setSummary] = useState({
    summary: "",
    decisions: "",
    risks: "",
    action_items: "",
  });

  const [userId, setUserId] = useState("");

  const [noteText, setNoteText] = useState("");

  const [loading, setLoading] = useState(true);
  const [summarySaving, setSummarySaving] = useState(false);
  const [summaryMessage, setSummaryMessage] = useState("");

  const loadData = useCallback(async () => {
    try {
      setLoading(true);

      const meetingData = await getMeetingById(meetingId);
      setMeeting(meetingData);

      try {
        const attendeesData = await getMeetingAttendees(meetingId);

        setAttendees(
          Array.isArray(attendeesData)
            ? attendeesData
            : attendeesData.items || [],
        );
      } catch (error) {
        console.error("Attendees:", error);
        setAttendees([]);
      }

      try {
        const notesData = await getMeetingNotes(meetingId);

        setNotes(Array.isArray(notesData) ? notesData : notesData.items || []);
      } catch (error) {
        console.error("Notes:", error);
        setNotes([]);
      }

      try {
        const summaryData = await getMeetingSummary(meetingId);

        if (summaryData) {
          setSummary({
            summary: summaryData.summary || "",
            decisions: summaryData.decisions || "",
            risks: summaryData.risks || "",
            action_items: summaryData.action_items || "",
          });
        }
      } catch (error) {
        console.error("Summary:", error);
      }
    } catch (error) {
      console.error(error);
      setMeeting(null);
    } finally {
      setLoading(false);
    }
  }, [meetingId]);

  const loadUsers = useCallback(async () => {
    try {
      const data = await getUsers();

      setUsers(Array.isArray(data) ? data : data.items || []);
    } catch (error) {
      console.error(error);
    }
  }, []);

  useEffect(() => {
    loadData();
    loadUsers();
  }, [loadData, loadUsers]);

  const handleAddAttendee = async (e) => {
    e.preventDefault();

    try {
      await addMeetingAttendee(meetingId, {
        user_id: Number(userId),
      });

      setUserId("");

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleRemoveAttendee = async (userIdValue) => {
    try {
      await removeMeetingAttendee(meetingId, userIdValue);

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleAddNote = async (e) => {
    e.preventDefault();

    try {
      await createMeetingNote(meetingId, {
        notes: noteText,
      });

      setNoteText("");

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleSummaryChange = (e) => {
    setSummaryMessage("");

    setSummary((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSaveSummary = async (e) => {
    e.preventDefault();

    try {
      setSummarySaving(true);
      setSummaryMessage("");

      const savedSummary = await saveMeetingSummary(meetingId, summary);

      setSummary({
        summary: savedSummary.summary || "",
        decisions: savedSummary.decisions || "",
        risks: savedSummary.risks || "",
        action_items: savedSummary.action_items || "",
      });
      setSummaryMessage("Summary saved");
    } catch (error) {
      console.error(error);
      setSummaryMessage(
        error.response?.data?.detail || "Unable to save summary",
      );
    } finally {
      setSummarySaving(false);
    }
  };

  if (loading) {
    return <div className="p-6">Loading meeting...</div>;
  }

  if (!meeting) {
    return <div className="p-6">Meeting not found</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <div className="bg-white border rounded-lg p-4">
        <h1 className="text-2xl font-bold">{meeting.title}</h1>

        <p className="mt-2 text-gray-600">{meeting.description}</p>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold mb-4">Add Attendee</h2>

        <form onSubmit={handleAddAttendee} className="flex gap-2">
          <select
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="border rounded px-3 py-2 w-72"
          >
            <option value="">Select Employee</option>

            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} ({user.email})
              </option>
            ))}
          </select>

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Add
          </button>
        </form>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold mb-4">Attendees</h2>

        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left p-2">User ID</th>

              <th className="text-left p-2">Action</th>
            </tr>
          </thead>

          <tbody>
            {attendees.map((attendee) => (
              <tr key={attendee.user_id}>
                <td className="p-2">{attendee.user_id}</td>

                <td className="p-2">
                  <button
                    onClick={() => handleRemoveAttendee(attendee.user_id)}
                    className="text-red-600"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold mb-4">Meeting Notes</h2>

        <form onSubmit={handleAddNote} className="space-y-3">
          <textarea
            value={noteText}
            onChange={(e) => setNoteText(e.target.value)}
            placeholder="Add meeting note"
            className="w-full border rounded px-3 py-2"
          />

          <button
            type="submit"
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Save Note
          </button>
        </form>

        <div className="mt-4 space-y-2">
          {notes.map((note) => (
            <div key={note.id} className="border rounded p-3">
              {note.notes}
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold mb-4">AI Meeting Summary</h2>

        <form onSubmit={handleSaveSummary} className="space-y-3">
          <textarea
            name="summary"
            value={summary.summary}
            onChange={handleSummaryChange}
            placeholder="Summary"
            className="w-full border rounded px-3 py-2"
          />

          <textarea
            name="decisions"
            value={summary.decisions}
            onChange={handleSummaryChange}
            placeholder="Decisions"
            className="w-full border rounded px-3 py-2"
          />

          <textarea
            name="risks"
            value={summary.risks}
            onChange={handleSummaryChange}
            placeholder="Risks"
            className="w-full border rounded px-3 py-2"
          />

          <textarea
            name="action_items"
            value={summary.action_items}
            onChange={handleSummaryChange}
            placeholder="Action Items"
            className="w-full border rounded px-3 py-2"
          />

          <button
            type="submit"
            disabled={summarySaving}
            className="bg-purple-600 text-white px-4 py-2 rounded"
          >
            {summarySaving ? "Saving..." : "Save Summary"}
          </button>

          {summaryMessage && (
            <p className="text-sm text-gray-600">{summaryMessage}</p>
          )}
        </form>
      </div>
    </div>
  );
}
