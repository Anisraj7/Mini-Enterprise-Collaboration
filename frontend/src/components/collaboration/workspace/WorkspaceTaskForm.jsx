import { useState } from "react";

const DEFAULT_FORM = {
  title: "",
  description: "",
  status: "todo",
  priority: "medium",
  due_date: "",
  assigned_to_id: "",
};

export default function WorkspaceTaskForm({
  members = [],
  onSubmit,
  loading = false,
}) {
  const [form, setForm] =
    useState(DEFAULT_FORM);

  const handleChange = (e) => {
    const { name, value } =
      e.target;

    setForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = async (
    e
  ) => {
    e.preventDefault();

    await onSubmit({
      ...form,
      assigned_to_id:
        form.assigned_to_id
          ? Number(
              form.assigned_to_id
            )
          : null,
    });

    setForm(DEFAULT_FORM);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="space-y-4"
    >
      <input
        type="text"
        name="title"
        value={form.title}
        onChange={handleChange}
        placeholder="Task title"
        className="w-full border rounded-lg p-3"
        required
      />

      <textarea
        name="description"
        value={form.description}
        onChange={handleChange}
        placeholder="Description"
        rows={4}
        className="w-full border rounded-lg p-3"
      />

      <div className="grid md:grid-cols-2 gap-4">
        <select
          name="status"
          value={form.status}
          onChange={handleChange}
          className="border rounded-lg p-3"
        >
          <option value="todo">
            Todo
          </option>
          <option value="in_progress">
            In Progress
          </option>
          <option value="review">
            Review
          </option>
          <option value="done">
            Done
          </option>
        </select>

        <select
          name="priority"
          value={form.priority}
          onChange={handleChange}
          className="border rounded-lg p-3"
        >
          <option value="low">
            Low
          </option>
          <option value="medium">
            Medium
          </option>
          <option value="high">
            High
          </option>
        </select>
      </div>

      <input
        type="datetime-local"
        name="due_date"
        value={form.due_date}
        onChange={handleChange}
        className="w-full border rounded-lg p-3"
      />

      <select
        name="assigned_to_id"
        value={form.assigned_to_id}
        onChange={handleChange}
        className="w-full border rounded-lg p-3"
      >
        <option value="">
          Unassigned
        </option>

        {members.map((member) => (
          <option
            key={member.user_id}
            value={member.user_id}
          >
            User #{member.user_id}
          </option>
        ))}
      </select>

      <button
        type="submit"
        disabled={loading}
        className="
          px-4
          py-2
          bg-blue-600
          text-white
          rounded-lg
        "
      >
        {loading
          ? "Creating..."
          : "Create Task"}
      </button>
    </form>
  );
}