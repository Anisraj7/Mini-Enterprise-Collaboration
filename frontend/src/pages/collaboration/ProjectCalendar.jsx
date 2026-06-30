import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getProjectCalendar,
} from "../../services/collaboration/calendarService";

export default function ProjectCalendar() {
  const { projectId } = useParams();

  const [events, setEvents] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const loadCalendar = async () => {
    try {
      setLoading(true);

      const response =
        await getProjectCalendar(
          projectId
        );

      setEvents(
        Array.isArray(response)
          ? response
          : response.items || []
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCalendar();
  }, [projectId]);

  const groupedEvents =
    events.reduce(
      (acc, event) => {
        const date =
          event.date ||
          event.event_date ||
          event.start_date ||
          "Unknown";

        if (!acc[date]) {
          acc[date] = [];
        }

        acc[date].push(event);

        return acc;
      },
      {}
    );

  if (loading) {
    return (
      <div className="p-6">
        Loading calendar...
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">
          Project Calendar
        </h1>
      </div>

      {!events.length && (
        <div className="bg-white border rounded-lg p-6 text-center">
          No calendar events found
        </div>
      )}

      {Object.entries(
        groupedEvents
      ).map(
        ([date, items]) => (
          <div
            key={date}
            className="bg-white border rounded-lg"
          >
            <div className="border-b px-4 py-3 bg-gray-50">
              <h2 className="font-semibold">
                {date}
              </h2>
            </div>

            <div className="divide-y">
              {items.map(
                (
                  event,
                  index
                ) => (
                  <div
                    key={
                      event.id ||
                      index
                    }
                    className="p-4"
                  >
                    <div className="font-medium">
                      {event.title ||
                        event.name ||
                        event.event_name}
                    </div>

                    <div className="text-sm text-gray-500 mt-1">
                      {event.type ||
                        event.event_type ||
                        "Event"}
                    </div>

                    {event.description && (
                      <p className="mt-2 text-gray-600">
                        {
                          event.description
                        }
                      </p>
                    )}
                  </div>
                )
              )}
            </div>
          </div>
        )
      )}
    </div>
  );
}