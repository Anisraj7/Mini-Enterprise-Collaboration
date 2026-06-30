export default function CalendarEventList({
  events,
}) {
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

  return (
    <div className="space-y-4">
      {Object.entries(
        groupedEvents
      ).map(
        ([date, items]) => (
          <div
            key={date}
            className="bg-white border rounded-lg"
          >
            <div className="border-b p-3 bg-gray-50">
              <h3 className="font-semibold">
                {date}
              </h3>
            </div>

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
                  className="p-3 border-b last:border-b-0"
                >
                  <p className="font-medium">
                    {event.title ||
                      event.name}
                  </p>

                  <p className="text-sm text-gray-500">
                    {event.type ||
                      event.event_type}
                  </p>
                </div>
              )
            )}
          </div>
        )
      )}
    </div>
  );
}