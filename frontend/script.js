const API_URL = "http://127.0.0.1:8000/todos";

const todoListElement = document.getElementById("todo-list");
const taskCountElement = document.getElementById("task-count");
const errorElement = document.getElementById("error-message");

function renderTodos(todos) {
  todoListElement.replaceChildren();
  taskCountElement.textContent = `${todos.length} ${todos.length === 1 ? "task" : "tasks"}`;

  todos.forEach((todo) => {
    const taskElement = document.createElement("article");
    taskElement.className = `todo-card ${todo.completed ? "completed" : ""}`;

    const headElement = document.createElement("div");
    headElement.className = "todo-head";

    const titleElement = document.createElement("h3");
    titleElement.className = "todo-title";
    titleElement.textContent = todo.title;

    const statusElement = document.createElement("span");
    statusElement.className = "status";
    statusElement.textContent = todo.completed ? "Completed" : "Incomplete";

    const descriptionElement = document.createElement("p");
    descriptionElement.className = "todo-description";
    descriptionElement.textContent = todo.description;

    headElement.appendChild(titleElement);
    headElement.appendChild(statusElement);
    taskElement.appendChild(headElement);
    taskElement.appendChild(descriptionElement);
    todoListElement.appendChild(taskElement);
  });
}

async function loadTodos() {
  errorElement.hidden = true;
  try {
    const response = await fetch(API_URL);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const todos = await response.json();
    renderTodos(todos);
  } catch (error) {
    console.error("Unable to load todos:", error);
    errorElement.textContent =
      "Could not load the todo list. Make sure the FastAPI server is running on port 8000.";
    errorElement.hidden = false;
  }
}

loadTodos();
