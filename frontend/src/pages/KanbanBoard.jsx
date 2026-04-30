import { useEffect, useState } from "react";
import {
  DndContext,
  DragOverlay,
  PointerSensor,
  useDraggable,
  useDroppable,
  useSensor,
  useSensors,
} from "@dnd-kit/core";
import { CSS } from "@dnd-kit/utilities";
import API from "../api/axios";
import Navbar from "../components/Navbar";

const columns = [
  { id: "todo", label: "TODO", bg: "bg-yellow-100", header: "bg-yellow-500" },
  { id: "in_progress", label: "IN PROGRESS", bg: "bg-blue-100", header: "bg-blue-500" },
  { id: "review", label: "REVIEW", bg: "bg-purple-100", header: "bg-purple-500" },
  { id: "done", label: "DONE", bg: "bg-green-100", header: "bg-green-500" },
];

const validFlow = {
  todo: ["in_progress"],
  in_progress: ["review"],
  review: ["done"],
  done: [],
};

function KanbanColumn({ column, children }) {
  const { isOver, setNodeRef } = useDroppable({ id: column.id });

  return (
    <div
      ref={setNodeRef}
      className={`${column.bg} rounded-xl p-4 min-h-[500px] shadow-inner transition ${
        isOver ? "ring-2 ring-indigo-500" : ""
      }`}
    >
      <div className={`${column.header} text-white text-center py-2 rounded-lg mb-4 font-semibold`}>
        {column.label}
      </div>
      {children}
    </div>
  );
}

function TaskCard({ task, onOpen, isOverlay = false }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    isDragging,
  } = useDraggable({
    id: String(task.id),
    data: {
      task,
      currentStatus: task.status,
    },
    disabled: isOverlay,
  });

  const style = {
    transform: CSS.Translate.toString(transform),
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      onClick={() => onOpen(task)}
      className={`bg-white p-4 mb-3 rounded-xl shadow hover:shadow-lg cursor-grab active:cursor-grabbing border-l-4 ${
        task.priority === "high" ? "border-red-500" : task.priority === "medium" ? "border-yellow-500" : "border-green-500"
      } ${isDragging ? "opacity-40" : ""} ${isOverlay ? "w-72 shadow-xl" : ""}`}
    >
      <h3 className="font-semibold">{task.title}</h3>
      <p className="text-xs mt-2 text-gray-500">Assigned: {task.assigned_to_name || "Unassigned"}</p>
      <p className="text-xs text-gray-400">Due: {task.due_date ? new Date(task.due_date).toLocaleDateString() : "No deadline"}</p>
    </div>
  );
}

export default function KanbanBoard() {
  const [tasks, setTasks] = useState({ todo: [], in_progress: [], review: [], done: [] });
  const [selectedTask, setSelectedTask] = useState(null);
  const [activeTask, setActiveTask] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [isInternal, setIsInternal] = useState(false);
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [userFilter, setUserFilter] = useState("");
  const [error, setError] = useState("");

  const fetchTasks = async () => {
    const res = await API.get("/tasks/kanban");
    setTasks({ todo: [], in_progress: [], review: [], done: [], ...res.data });
  };

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  useEffect(() => {
    const loadInitialTasks = async () => {
      try {
        const res = await API.get("/tasks/kanban");
        setTasks({ todo: [], in_progress: [], review: [], done: [], ...res.data });
      } catch (err) {
        setError(err.response?.data?.detail || "Unable to load Kanban board.");
      }
    };

    loadInitialTasks();
  }, []);

  const handleDragStart = (event) => {
    setActiveTask(event.active.data.current?.task || null);
  };

  const handleDragEnd = async (event) => {
    const { active, over } = event;
    setActiveTask(null);

    if (!over) return;

    const taskId = Number(active.id);
    const currentStatus = active.data.current?.currentStatus;
    const newStatus = over.id;

    if (!taskId || currentStatus === newStatus) return;
    if (!validFlow[currentStatus]?.includes(newStatus)) {
      setError(`Invalid transition: ${currentStatus} -> ${newStatus}`);
      return;
    }

    try {
      await API.patch(`/tasks/${taskId}/status`, { status: newStatus });
      setError("");
      await fetchTasks();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update task status.");
    }
  };

  const handleDragCancel = () => {
    setActiveTask(null);
  };

  const loadComments = async (task) => {
    try {
      setSelectedTask(task);
      const res = await API.get(`/tasks/${task.id}/comments`);
      setComments(res.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load comments.");
    }
  };

  const addComment = async () => {
    if (!newComment.trim() || !selectedTask) return;
    try {
      await API.post(`/tasks/${selectedTask.id}/comments`, {
        content: newComment,
        is_internal: isInternal,
      });
      setNewComment("");
      setIsInternal(false);
      const res = await API.get(`/tasks/${selectedTask.id}/comments`);
      setComments(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to add comment.");
    }
  };

  const visibleTasks = (columnId) => (
    tasks[columnId] || []
  )
    .filter((task) => priorityFilter === "all" || task.priority === priorityFilter)
    .filter((task) => !userFilter || task.assigned_to_name?.toLowerCase().includes(userFilter.toLowerCase()));

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />
      <div className="p-6">
        <div className="flex flex-wrap justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-700">Kanban Board</h1>
            <p className="text-sm text-gray-500">TODO &rarr; IN PROGRESS &rarr; REVIEW &rarr; DONE</p>
          </div>
          <div className="flex gap-3">
            <select value={priorityFilter} onChange={(e) => setPriorityFilter(e.target.value)} className="border p-2 rounded">
              <option value="all">All Priority</option>
              <option value="high">High</option>
              <option value="medium">Medium</option>
              <option value="low">Low</option>
            </select>
            <input value={userFilter} placeholder="Filter by user" onChange={(e) => setUserFilter(e.target.value)} className="border p-2 rounded" />
          </div>
        </div>

        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

        <DndContext
          sensors={sensors}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
          onDragCancel={handleDragCancel}
        >
          <div className="grid gap-6 md:grid-cols-4">
            {columns.map((col) => (
              <KanbanColumn key={col.id} column={col}>
                {visibleTasks(col.id).map((task) => (
                  <TaskCard key={task.id} task={task} onOpen={loadComments} />
                ))}
              </KanbanColumn>
            ))}
          </div>
          <DragOverlay>
            {activeTask ? <TaskCard task={activeTask} onOpen={() => {}} isOverlay /> : null}
          </DragOverlay>
        </DndContext>
      </div>

      {selectedTask && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center p-4">
          <div className="bg-white w-full max-w-lg p-5 rounded-xl shadow-lg">
            <div className="flex justify-between gap-3 mb-3">
              <h2 className="text-xl font-bold">{selectedTask.title}</h2>
              <button onClick={() => setSelectedTask(null)} className="text-gray-500">Close</button>
            </div>

            <div className="max-h-[300px] overflow-y-auto space-y-2 mb-3">
              {comments.map((comment) => (
                <div key={comment.id} className="bg-gray-100 p-2 rounded">
                  <p>{comment.content}</p>
                  <p className="text-xs text-gray-400">
                    {comment.user_name || `User ${comment.user_id}`} - {comment.is_internal ? "Internal" : "Public"} - {new Date(comment.created_at).toLocaleString()}
                  </p>
                </div>
              ))}
              {comments.length === 0 && <p className="text-sm text-gray-500">No comments yet.</p>}
            </div>

            <textarea value={newComment} onChange={(e) => setNewComment(e.target.value)} className="border w-full p-2 rounded mb-2" placeholder="Write comment..." />
            <label className="flex items-center gap-2 text-sm mb-3">
              <input type="checkbox" checked={isInternal} onChange={(e) => setIsInternal(e.target.checked)} />
              Internal note
            </label>
            <button onClick={addComment} className="bg-blue-500 text-white px-3 py-1 rounded">Add Comment</button>
          </div>
        </div>
      )}
    </div>
  );
}
