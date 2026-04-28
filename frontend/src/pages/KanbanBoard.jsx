import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";

import {
  DndContext,
  closestCorners,
} from "@dnd-kit/core";

import {
  SortableContext,
  verticalListSortingStrategy,
} from "@dnd-kit/sortable";

const columns = ["TODO", "IN_PROGRESS", "REVIEW", "DONE"];

const columnStyles = {
  TODO: { bg: "bg-yellow-100", header: "bg-yellow-500" },
  IN_PROGRESS: { bg: "bg-blue-100", header: "bg-blue-500" },
  REVIEW: { bg: "bg-purple-100", header: "bg-purple-500" },
  DONE: { bg: "bg-green-100", header: "bg-green-500" },
};

export default function Kanban() {
  const [tasks, setTasks] = useState({});
  const [selectedTask, setSelectedTask] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");

  const [priorityFilter, setPriorityFilter] = useState("ALL");
  const [userFilter, setUserFilter] = useState("");

  const navigate = useNavigate();

  // Fetch tasks
  const fetchTasks = async () => {
    const res = await API.get("/tasks/");

    const grouped = {
      TODO: [],
      IN_PROGRESS: [],
      REVIEW: [],
      DONE: [],
    };

    res.data.forEach((task) => {
      const status = task.status.toUpperCase();
      if (grouped[status]) grouped[status].push(task);
    });

    setTasks(grouped);
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  // Drag logic
  const handleDragEnd = async (event) => {
    const { active, over } = event;
    if (!over) return;

    const taskId = parseInt(active.id);
    const newStatus = over.id;

    let currentStatus;
    for (const col of columns) {
      if (tasks[col]?.find((t) => t.id === taskId)) {
        currentStatus = col;
        break;
      }
    }

    const validFlow = {
      TODO: ["IN_PROGRESS"],
      IN_PROGRESS: ["REVIEW"],
      REVIEW: ["DONE"],
      DONE: [],
    };

    if (!validFlow[currentStatus].includes(newStatus)) {
      alert("Invalid transition!");
      return;
    }

    await API.put(`/tasks/${taskId}`, {
      status: newStatus.toLowerCase(),
    });

    fetchTasks();
  };

  // Comments
  const loadComments = async (taskId) => {
    const res = await API.get(`/tasks/${taskId}/comments`);
    setComments(res.data);
  };

  const addComment = async () => {
    if (!newComment.trim()) return;

    await API.post(`/tasks/${selectedTask.id}/comments`, {
      content: newComment,
    });

    setNewComment("");
    loadComments(selectedTask.id);
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />

      <div className="p-6">
        <h1 className="text-3xl font-bold text-gray-700 mb-4">
          🚀 Kanban Board
        </h1>

        {/* Filters */}
        <div className="flex gap-4 mb-6">
          <select
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="border p-2 rounded"
          >
            <option value="ALL">All Priority</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <input
            placeholder="Filter by user"
            onChange={(e) => setUserFilter(e.target.value)}
            className="border p-2 rounded"
          />
        </div>

        <DndContext collisionDetection={closestCorners} onDragEnd={handleDragEnd}>
          <div className="grid grid-cols-4 gap-6">
            {columns.map((col) => (
              <div
                key={col}
                id={col}
                className={`${columnStyles[col].bg} rounded-xl p-4 min-h-[500px] shadow-inner`}
              >
                <div
                  className={`${columnStyles[col].header} text-white text-center py-2 rounded-lg mb-4 font-semibold`}
                >
                  {col.replace("_", " ")}
                </div>

                <SortableContext
                  items={tasks[col]?.map((t) => t.id) || []}
                  strategy={verticalListSortingStrategy}
                >
                  {tasks[col]
                    ?.filter((task) => {
                      return (
                        (priorityFilter === "ALL" ||
                          task.priority === priorityFilter) &&
                        (!userFilter ||
                          task.assigned_to_name
                            ?.toLowerCase()
                            .includes(userFilter.toLowerCase()))
                      );
                    })
                    .map((task) => (
                      <div
                        key={task.id}
                        id={task.id}
                        draggable
                        onClick={() => {
                          setSelectedTask(task);
                          loadComments(task.id);
                        }}
                        className={`bg-white p-4 mb-3 rounded-xl shadow hover:shadow-lg cursor-pointer border-l-4 ${
                          task.priority === "high"
                            ? "border-red-500"
                            : task.priority === "medium"
                            ? "border-yellow-500"
                            : "border-green-500"
                        }`}
                      >
                        <h3 className="font-semibold">{task.title}</h3>

                        {/* Approval badge */}
                        <span
                          className={`text-xs px-2 py-1 rounded-full mt-2 inline-block ${
                            task.approval_status === "APPROVED"
                              ? "bg-green-500 text-white"
                              : task.approval_status === "REJECTED"
                              ? "bg-red-500 text-white"
                              : "bg-gray-400 text-white"
                          }`}
                        >
                          {task.approval_status || "NO APPROVAL"}
                        </span>

                        <p className="text-xs mt-2 text-gray-500">
                          👤 {task.assigned_to_name || "Unassigned"}
                        </p>

                        <p className="text-xs text-gray-400">
                          📅{" "}
                          {task.due_date
                            ? new Date(task.due_date).toLocaleDateString()
                            : "No deadline"}
                        </p>
                      </div>
                    ))}
                </SortableContext>
              </div>
            ))}
          </div>
        </DndContext>
      </div>

      {/* Comments Modal */}
      {selectedTask && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center">
          <div className="bg-white w-[500px] p-5 rounded-xl shadow-lg">
            <h2 className="text-xl font-bold mb-3">
              {selectedTask.title}
            </h2>

            <div className="max-h-[300px] overflow-y-auto space-y-2 mb-3">
              {comments.map((c) => (
                <div key={c.id} className="bg-gray-100 p-2 rounded">
                  <p>{c.content}</p>
                  <p className="text-xs text-gray-400">
                    {new Date(c.created_at).toLocaleString()}
                  </p>
                </div>
              ))}
            </div>

            <input
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              className="border w-full p-2 rounded mb-2"
              placeholder="Write comment..."
            />

            <div className="flex justify-between">
              <button
                onClick={addComment}
                className="bg-blue-500 text-white px-3 py-1 rounded"
              >
                Add
              </button>

              <button
                onClick={() => setSelectedTask(null)}
                className="text-gray-500"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}