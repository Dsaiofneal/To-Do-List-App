const urlParams = new URLSearchParams(window.location.search);
const taskId = urlParams.get("id");

async function loadTaskDetails() {
  if (!taskId) return;

  try {
    const response = await fetch("/api/tasks/" + taskId);
    if (!response.ok) {
      alert("Task not found");
      window.location.href = "planner.html";
      return;
    }
    const task = await response.json();
    document.getElementById("editTitle").value = task.title;
    document.getElementById("editDescription").value = task.description || "";
    document.getElementById("editStatus").value = task.status;
    document.getElementById("editPriority").value = task.priority;
  } catch (err) {
    console.error("Error loading task:", err);
  }
}

async function saveTask() {
  const data = {
    title: document.getElementById("editTitle").value,
    description: document.getElementById("editDescription").value,
    status: document.getElementById("editStatus").value,
    priority: document.getElementById("editPriority").value,
  };

  try {
    const response = await fetch("/api/tasks/" + taskId, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      window.location.href = "planner.html";
    }
  } catch (err) {
    console.error("Error saving task:", err);
  }
}

async function deleteTask() {
  if (!confirm("Are you sure you want to delete this task?")) return;

  try {
    const response = await fetch("/api/tasks/" + taskId, {
      method: "DELETE",
    });

    if (response.ok) {
      window.location.href = "planner.html";
    }
  } catch (err) {
    console.error("Error deleting task:", err);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  if (taskId) {
    loadTaskDetails();
  } else {
    window.location.href = "planner.html";
  }
});
