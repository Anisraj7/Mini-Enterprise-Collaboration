
import { useEffect, useMemo, useState } from "react";

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

import {
  AlertTriangle,
  CalendarDays,
  CheckCircle2,
  Circle,
  Clock3,
  Download,
  FileText,
  MessageSquare,
  Upload,
  User,
  Wifi,
  WifiOff,
} from "lucide-react";

import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import { getPageItems } from "../api/pagination";
import { getUserWebSocketUrl } from "../api/websocket";
import Navbar from "../components/Navbar";

const columns = [
  {
    id: "todo",
    label: "TODO",
    icon: Circle,
    bg: "bg-yellow-50",
    border: "border-yellow-400",
    countBg: "bg-yellow-500",
  },
  {
    id: "in_progress",
    label: "IN PROGRESS",
    icon: Clock3,
    bg: "bg-blue-50",
    border: "border-blue-400",
    countBg: "bg-blue-500",
  },
  {
    id: "review",
    label: "REVIEW",
    icon: AlertTriangle,
    bg: "bg-purple-50",
    border: "border-purple-400",
    countBg: "bg-purple-500",
  },
  {
    id: "done",
    label: "DONE",
    icon: CheckCircle2,
    bg: "bg-green-50",
    border: "border-green-400",
    countBg: "bg-green-500",
  },
];

const validFlow = {
  todo: ["in_progress"],
  in_progress: ["review"],
  review: ["done"],
  done: [],
};

function Column({ column, tasks, children }) {

  const { setNodeRef, isOver } = useDroppable({
    id: column.id,
  });

  const Icon = column.icon;

  return (
    <div
      ref={setNodeRef}
      className={`
        ${column.bg}
        border-t-4
        ${column.border}
        rounded-2xl
        p-4
        min-h-[650px]
        transition-all
        duration-200
        shadow-sm
        ${isOver ? "ring-2 ring-indigo-500 scale-[1.01]" : ""}
      `}
    >

      <div className="flex items-center justify-between mb-5">

        <div className="flex items-center gap-2">
          <Icon size={18} />

          <h2 className="font-bold text-gray-700">
            {column.label}
          </h2>
        </div>

        <div
          className={`
            ${column.countBg}
            text-white
            text-xs
            px-3
            py-1
            rounded-full
            font-semibold
          `}
        >
          {tasks.length}
        </div>

      </div>

      {children}

    </div>
  );
}

function TaskCard({
  task,
  onOpen,
  canDrag,
  isOverlay = false,
}) {

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
    disabled: !canDrag || isOverlay,
  });

  const style = {
    transform: CSS.Translate.toString(transform),
  };

  const overdue =
    task.due_date &&
    new Date(task.due_date) < new Date();

  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      onClick={() => onOpen(task)}
      className={`
        bg-white
        rounded-2xl
        p-4
        mb-4
        border
        shadow-sm
        hover:shadow-lg
        transition-all
        duration-200
        cursor-grab
        active:cursor-grabbing
        ${isDragging ? "opacity-40" : ""}
        ${isOverlay ? "w-80 rotate-2 shadow-2xl" : ""}
      `}
    >

      <div className="flex justify-between items-start mb-3">

        <div>
          <h3 className="font-semibold text-gray-800 text-sm">
            {task.title}
          </h3>

          <p className="text-xs text-gray-400 mt-1">
            #{task.id}
          </p>
        </div>

        <div
          className={`
            text-xs
            px-2
            py-1
            rounded-full
            font-medium
            ${
              task.priority === "high"
                ? "bg-red-100 text-red-600"
                : task.priority === "medium"
                ? "bg-yellow-100 text-yellow-700"
                : "bg-green-100 text-green-600"
            }
          `}
        >
          {task.priority}
        </div>

      </div>

      <div className="space-y-2 text-xs text-gray-500">

        <div className="flex items-center gap-2">
          <User size={14} />
          <span>
            {task.assigned_to_name || "Unassigned"}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <CalendarDays size={14} />

          <span>
            {task.due_date
              ? new Date(task.due_date).toLocaleDateString()
              : "No deadline"}
          </span>
        </div>

        {task.comments_count > 0 && (
          <div className="flex items-center gap-2">
            <MessageSquare size={14} />
            <span>{task.comments_count} comments</span>
          </div>
        )}

      </div>

      {overdue && (
        <div className="mt-3 bg-red-50 text-red-600 text-xs px-2 py-2 rounded-lg font-medium flex items-center gap-2">
          <AlertTriangle size={14} />
          Overdue Task
        </div>
      )}

      {!canDrag && (
        <div className="mt-3 bg-gray-100 text-gray-500 text-xs px-2 py-2 rounded-lg">
          Read-only access
        </div>
      )}

    </div>
  );
}

export default function KanbanBoard() {
  const navigate = useNavigate();

  const [tasks, setTasks] = useState({
    todo: [],
    in_progress: [],
    review: [],
    done: [],
  });

  const [activeTask, setActiveTask] = useState(null);

  const [selectedTask, setSelectedTask] = useState(null);

  const [comments, setComments] = useState([]);
  const [documents, setDocuments] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);

  const [newComment, setNewComment] = useState("");

  const [isInternal, setIsInternal] = useState(false);

  const [priorityFilter, setPriorityFilter] = useState("all");

  const [search, setSearch] = useState("");

  const [socketConnected, setSocketConnected] = useState(false);

  const [error, setError] = useState("");

  const [user, setUser] = useState(null);

  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    })
  );

  const fetchTasks = async () => {

    try {

      const response = await API.get(
        "/tasks/kanban"
      );

      setTasks({
        todo: [],
        in_progress: [],
        review: [],
        done: [],
        ...response.data,
      });

    } catch (err) {

      setError(
        err.response?.data?.detail ||
        "Unable to load tasks"
      );
    }
  };

  useEffect(() => {

    const loadInitialData = async () => {

      try {

        const userRes = await API.get(
          "/auth/me"
        );

        setUser(userRes.data);

        await fetchTasks();

      } catch (err) {

        setError(
          err.response?.data?.detail ||
          "Unable to load board"
        );
      }
    };

    loadInitialData();

  }, []);

  useEffect(() => {

    if (!user) return;

    const ws = new WebSocket(
      getUserWebSocketUrl(user.id)
    );

    ws.onopen = () => {
      setSocketConnected(true);
    };

    ws.onmessage = async (event) => {

      toast.success(event.data);

      await fetchTasks();
    };

    ws.onclose = () => {
      setSocketConnected(false);
    };

    return () => {
      ws.close();
    };

  }, [user]);

  const handleDragStart = (event) => {
    setActiveTask(
      event.active.data.current?.task
    );
  };

  const handleDragEnd = async (event) => {

    const { active, over } = event;

    setActiveTask(null);

    if (!over) return;

    const taskId = Number(active.id);

    const currentStatus =
      active.data.current?.currentStatus;

    const newStatus = over.id;

    if (
      !validFlow[currentStatus]?.includes(
        newStatus
      )
    ) {

      toast.error(
        "Invalid workflow transition"
      );

      return;
    }

    try {

      await API.patch(
        `/tasks/${taskId}/status`,
        {
          status: newStatus,
        }
      );

      toast.success(
        `Moved to ${newStatus}`
      );

      await fetchTasks();

    } catch (err) {

      toast.error(
        err.response?.data?.detail ||
        "Unable to move task"
      );
    }
  };

  const openTask = async (task) => {

    try {

      setSelectedTask(task);

      const response = await API.get(
        `/tasks/${task.id}/comments`
      );

      setComments(getPageItems(response.data));

      const docsResponse = await API.get(
        `/documents/task/${task.id}`
      );

      setDocuments(getPageItems(docsResponse.data));

    } catch {

      toast.error(
        "Unable to load comments"
      );
    }
  };

  const uploadDocument = async () => {

    if (!selectedFile || !selectedTask) return;

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {

      await API.post(
        `/documents/upload?task_id=${selectedTask.id}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      );

      toast.success("Document uploaded");
      setSelectedFile(null);

      const docsResponse = await API.get(
        `/documents/task/${selectedTask.id}`
      );

      setDocuments(getPageItems(docsResponse.data));

    } catch (err) {

      toast.error(
        err.response?.data?.detail ||
        "Unable to upload document"
      );
    }
  };

  const downloadDocument = async (doc) => {

    try {

      const response = await API.get(
        `/documents/${doc.id}`,
        {
          responseType: "blob",
        }
      );

      const url = URL.createObjectURL(response.data);
      const link = document.createElement("a");
      link.href = url;
      link.download = doc.file_name;
      link.click();
      URL.revokeObjectURL(url);

    } catch {
      toast.error("Unable to download document");
    }
  };

  const addComment = async () => {

    if (!newComment.trim()) return;

    try {

      await API.post(
        `/tasks/${selectedTask.id}/comments`,
        {
          content: newComment,
          is_internal: isInternal,
        }
      );

      toast.success("Comment added");

      setNewComment("");

      const response = await API.get(
        `/tasks/${selectedTask.id}/comments`
      );

      setComments(getPageItems(response.data));

    } catch {
      toast.error(
        "Unable to add comment"
      );
    }
  };

  const filteredTasks = useMemo(() => {

    const result = {};

    Object.keys(tasks).forEach((key) => {

      result[key] = tasks[key]

        .filter(
          (task) =>
            priorityFilter === "all" ||
            task.priority === priorityFilter
        )

        .filter(
          (task) =>
            task.title
              .toLowerCase()
              .includes(search.toLowerCase())
        );
    });

    return result;

  }, [tasks, priorityFilter, search]);

  const canDrag =
    user?.role === "admin" ||
    user?.role === "manager";

  return (
    <div className="bg-gray-100 min-h-screen">

      <Navbar />

      <div className="max-w-[1800px] mx-auto p-6">

        {/* HEADER */}
        <div className="flex flex-wrap justify-between items-center gap-4 mb-8">

          <div>
            <h1 className="text-4xl font-bold text-gray-800">
              Enterprise Workflow Board
            </h1>

            <p className="text-gray-500 mt-2">
              Real-time collaborative Kanban workflow
            </p>

            <div className="flex items-center gap-2 mt-3 text-sm text-gray-500">

              {socketConnected ? (
                <Wifi className="text-green-500" size={16} />
              ) : (
                <WifiOff className="text-red-500" size={16} />
              )}

              {socketConnected
                ? "Live sync connected"
                : "Disconnected"}

            </div>

          </div>

          <div className="flex flex-wrap gap-3">

            <input
              value={search}
              onChange={(e) =>
                setSearch(e.target.value)
              }
              placeholder="Search tasks"
              className="bg-white border rounded-xl px-4 py-2 shadow-sm"
            />

            <select
              value={priorityFilter}
              onChange={(e) =>
                setPriorityFilter(e.target.value)
              }
              className="bg-white border rounded-xl px-4 py-2 shadow-sm"
            >

              <option value="all">
                All Priority
              </option>

              <option value="high">
                High
              </option>

              <option value="medium">
                Medium
              </option>

              <option value="low">
                Low
              </option>

            </select>

          </div>

        </div>

        {/* ERROR */}
        {error && (
          <div className="bg-red-100 text-red-600 p-4 rounded-xl mb-6">
            {error}
          </div>
        )}

        {/* BOARD */}
        <DndContext
          sensors={sensors}
          onDragStart={handleDragStart}
          onDragEnd={handleDragEnd}
        >

          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">

            {columns.map((column) => (

              <Column
                key={column.id}
                column={column}
                tasks={filteredTasks[column.id]}
              >

                {filteredTasks[column.id].map((task) => (

                  <TaskCard
                    key={task.id}
                    task={task}
                    onOpen={openTask}
                    canDrag={canDrag}
                  />

                ))}

              </Column>

            ))}

          </div>

          <DragOverlay>

            {activeTask ? (
              <TaskCard
                task={activeTask}
                onOpen={() => {}}
                isOverlay
                canDrag
              />
            ) : null}

          </DragOverlay>

        </DndContext>

      </div>

      {/* TASK DETAILS MODAL */}
      {selectedTask && (

        <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50 p-4">

          <div className="bg-white w-full max-w-2xl rounded-3xl shadow-2xl p-6">

            <div className="flex justify-between items-center mb-6">

              <div>
                <h2 className="text-2xl font-bold text-gray-800">
                  {selectedTask.title}
                </h2>

                <p className="text-gray-400 text-sm mt-1">
                  Task #{selectedTask.id}
                </p>
              </div>

              <button
                onClick={() =>
                  setSelectedTask(null)
                }
                className="text-gray-400 hover:text-gray-600"
              >
                Close
              </button>

            </div>

            {/* ASSIGNEE */}
            <div className="grid md:grid-cols-3 gap-4 mb-6">

              <div className="bg-gray-50 p-4 rounded-2xl">
                <p className="text-xs text-gray-400 mb-1">
                  Assigned To
                </p>

                <p className="font-semibold text-gray-700">
                  {selectedTask.assigned_to_name || "Unassigned"}
                </p>
              </div>

              <div className="bg-gray-50 p-4 rounded-2xl">
                <p className="text-xs text-gray-400 mb-1">
                  Priority
                </p>

                <p className="font-semibold text-gray-700 capitalize">
                  {selectedTask.priority}
                </p>
              </div>

              <div className="bg-gray-50 p-4 rounded-2xl">
                <p className="text-xs text-gray-400 mb-1">
                  Status
                </p>

                <p className="font-semibold text-gray-700 capitalize">
                  {selectedTask.status.replace("_", " ")}
                </p>
              </div>

            </div>

            {canDrag && (
              <div className="mb-6">
                <button
                  onClick={() =>
                    navigate(
                      `/tasks/${selectedTask.id}/assign`
                    )
                  }
                  className="bg-sky-600 hover:bg-sky-700 text-white px-4 py-2 rounded-xl text-sm font-medium"
                >
                  Assign To
                </button>
              </div>
            )}

            {/* DOCUMENTS */}
            <div className="mb-6">

              <div className="flex items-center gap-2 mb-3">
                <FileText size={18} />
                <h3 className="font-semibold text-gray-700">
                  Documents
                </h3>
              </div>

              <div className="flex flex-wrap gap-2 mb-3">
                <input
                  type="file"
                  onChange={(e) =>
                    setSelectedFile(e.target.files?.[0] || null)
                  }
                  className="text-sm"
                />

                <button
                  onClick={uploadDocument}
                  disabled={!selectedFile}
                  className="bg-sky-600 disabled:bg-gray-300 text-white px-3 py-2 rounded-xl text-sm flex items-center gap-2"
                >
                  <Upload size={14} />
                  Upload
                </button>
              </div>

              <div className="space-y-2 max-h-28 overflow-y-auto">
                {documents.length === 0 ? (
                  <p className="text-gray-400 text-sm">
                    No documents yet
                  </p>
                ) : (
                  documents.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => downloadDocument(doc)}
                      className="bg-gray-50 hover:bg-gray-100 p-3 rounded-xl flex items-center justify-between text-sm"
                    >
                      <span>
                        {doc.file_name} v{doc.version}
                      </span>
                      <Download size={14} />
                    </button>
                  ))
                )}
              </div>

            </div>

            {/* COMMENTS */}
            <div className="max-h-[300px] overflow-y-auto space-y-3 mb-5">

              {comments.length === 0 ? (
                <p className="text-gray-400 text-sm">
                  No comments yet
                </p>
              ) : (

                comments.map((comment) => (

                  <div
                    key={comment.id}
                    className="bg-gray-100 p-4 rounded-2xl"
                  >

                    <p className="text-gray-700">
                      {comment.content}
                    </p>

                    <p className="text-xs text-gray-400 mt-2">
                      {comment.user_name || `User ${comment.user_id}`}
                      {" â€¢ "}
                      {comment.is_internal
                        ? "Internal"
                        : "Public"}
                      {" â€¢ "}
                      {new Date(
                        comment.created_at
                      ).toLocaleString()}
                    </p>

                  </div>

                ))

              )}

            </div>

            {/* COMMENT BOX */}
            <textarea
              value={newComment}
              onChange={(e) =>
                setNewComment(e.target.value)
              }
              placeholder="Write comment"
              className="border rounded-2xl w-full p-4 mb-4"
            />

            <div className="flex justify-between items-center">

              <label className="flex items-center gap-2 text-sm text-gray-600">

                <input
                  type="checkbox"
                  checked={isInternal}
                  onChange={(e) =>
                    setIsInternal(
                      e.target.checked
                    )
                  }
                />

                Internal Note

              </label>

              <button
                onClick={addComment}
                className="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2 rounded-xl font-medium"
              >
                Add Comment
              </button>

            </div>

          </div>

        </div>

      )}

    </div>
  );
}

