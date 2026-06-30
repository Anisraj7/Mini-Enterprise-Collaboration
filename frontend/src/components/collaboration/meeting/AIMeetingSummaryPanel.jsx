export default function AIMeetingSummaryPanel({
  summary,
  onChange,
  onSave,
}) {
  return (
    <form
      onSubmit={onSave}
      className="space-y-3"
    >
      <textarea
        name="summary"
        value={summary.summary}
        onChange={onChange}
        placeholder="Summary"
        className="w-full border rounded px-3 py-2"
      />

      <textarea
        name="decisions"
        value={
          summary.decisions
        }
        onChange={onChange}
        placeholder="Decisions"
        className="w-full border rounded px-3 py-2"
      />

      <textarea
        name="risks"
        value={summary.risks}
        onChange={onChange}
        placeholder="Risks"
        className="w-full border rounded px-3 py-2"
      />

      <textarea
        name="action_items"
        value={
          summary.action_items
        }
        onChange={onChange}
        placeholder="Action Items"
        className="w-full border rounded px-3 py-2"
      />

      <button
        type="submit"
        className="bg-purple-600 text-white px-4 py-2 rounded"
      >
        Save Summary
      </button>
    </form>
  );
}