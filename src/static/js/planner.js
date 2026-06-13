let allTasks = [];

async function loadTasks() {
  try {
    const response = await fetch("/api/tasks");
    allTasks = await response.json();
    const sortContainer = document.getElementById("sortContainer");
    if (sortContainer) {
      sortContainer.style.display = allTasks.length > 1 ? "flex" : "none";
    }
    renderTasks();
  } catch (err) {
    console.error("Error loading tasks:", err);
  }
}

function renderTasks() {
  const list = document.getElementById("taskList");
  const sortSelect = document.getElementById("sortSelect");
  if (!list || !sortSelect) return;

  const sortBy = sortSelect.value;
  list.innerHTML = "";

  let tasksToDisplay = [...allTasks];
  if (sortBy === "priority") {
    const weights = { high: 3, medium: 2, low: 1 };
    tasksToDisplay.sort(
      (a, b) => (weights[b.priority] || 0) - (weights[a.priority] || 0),
    );
  } else if (sortBy === "status") {
    const weights = { in_progress: 3, pending: 2, completed: 1 };
    tasksToDisplay.sort(
      (a, b) => (weights[b.status] || 0) - (weights[a.status] || 0),
    );
  }

  tasksToDisplay.forEach((task) => {
    const a = document.createElement("a");
    a.href = "task.html?id=" + task.id;
    a.className = "task-item";

    const priorityClass = "priority-" + (task.priority || "medium");
    const statusText = (task.status || "pending").replace("_", " ");

    a.innerHTML = `
            <div class="task-info">
                <span class="task-title">${task.title}</span>
            </div>
            <div class="task-badges">
                <span class="badge ${priorityClass}">${task.priority || "medium"}</span>
                <span class="badge status-badge">${statusText}</span>
            </div>
        `;
    list.appendChild(a);
  });
}

async function addNewTask() {
  const input = document.getElementById("taskInput");
  if (!input) return;

  const title = input.value.trim();
  if (!title) return;
  try {
    const response = await fetch("/api/tasks", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title: title }),
    });
    if (response.ok) {
      input.value = "";
      await loadTasks();
    }
  } catch (err) {
    console.error("Error adding task:", err);
  }
}

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  const addBtn = document.getElementById("addBtn");
  const taskInput = document.getElementById("taskInput");
  const sortSelect = document.getElementById("sortSelect");

  if (addBtn) addBtn.addEventListener("click", addNewTask);
  if (taskInput) {
    taskInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") addNewTask();
    });
  }
  if (sortSelect) sortSelect.addEventListener("change", renderTasks);

  loadTasks();
});
