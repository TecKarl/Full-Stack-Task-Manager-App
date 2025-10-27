// API endpoint configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const addTaskForm = document.getElementById('addTaskForm');
const tasksContainer = document.querySelector('.tasks-container');
const clearAllTasksBtn = document.getElementById('clearAllTasks');
const editTaskModal = document.getElementById('editTaskModal');
const editTaskForm = document.getElementById('editTaskForm');
const closeModalBtn = document.getElementById('closeModal');

let currentEditingTaskId = null;

// Utility Functions
const formatDateTime = (dateString) => {
    return new Date(dateString).toLocaleString();
};

const showModal = () => {
    editTaskModal.classList.add('active');
};

const hideModal = () => {
    editTaskModal.classList.remove('active');
    currentEditingTaskId = null;
};

// Task HTML Template
const createTaskHTML = (task) => `
    <div class="task-item" data-task-id="${task.task_id}">
        <div class="task-content">
            <h3>${task.task_desc}</h3>
            <p class="task-date">${formatDateTime(task.date)}</p>
        </div>
        <div class="task-actions">
            <button class="btn btn-edit" onclick="handleEditClick(${task.task_id}, '${task.task_desc}', '${task.date}')">
                <i class="fas fa-edit"></i>
            </button>
            <button class="btn btn-delete" onclick="handleDelete(${task.task_id})">
                <i class="fas fa-trash"></i>
            </button>
        </div>
    </div>
`;

// API Functions
async function fetchTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`);
        if (!response.ok) {
            if (response.status === 404) {
                tasksContainer.innerHTML = '<p>No tasks found</p>';
                return;
            }
            throw new Error('Failed to fetch tasks');
        }
        const tasks = await response.json();
        tasksContainer.innerHTML = tasks.map(task => createTaskHTML(task)).join('');
    } catch (error) {
        console.error('Error:', error);
        tasksContainer.innerHTML = '<p>Error loading tasks</p>';
    }
}

async function createTask(taskData) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        if (!response.ok) throw new Error('Failed to create task');
        fetchTasks(); // Refresh task list
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to create task');
    }
}

async function updateTask(taskId, taskData) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData)
        });
        if (!response.ok) throw new Error('Failed to update task');
        fetchTasks(); // Refresh task list
        hideModal();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to update task');
    }
}

async function deleteTask(taskId) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete task');
        fetchTasks(); // Refresh task list
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to delete task');
    }
}

async function deleteAllTasks() {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error('Failed to delete all tasks');
        fetchTasks(); // Refresh task list
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to delete all tasks');
    }
}

// Event Handlers
function handleEditClick(taskId, taskDesc, date) {
    currentEditingTaskId = taskId;
    document.getElementById('editTaskDesc').value = taskDesc;
    showModal();
}

function handleDelete(taskId) {
    if (confirm('Are you sure you want to delete this task?')) {
        deleteTask(taskId);
    }
}

// Event Listeners
addTaskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const taskData = {
        task_desc: document.getElementById('taskDesc').value
    };
    createTask(taskData);
    addTaskForm.reset();
});

editTaskForm.addEventListener('submit', (e) => {
    e.preventDefault();
    if (!currentEditingTaskId) return;

    const taskData = {
        task_desc: document.getElementById('editTaskDesc').value
    };
    updateTask(currentEditingTaskId, taskData);
});

clearAllTasksBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to delete all tasks?')) {
        deleteAllTasks();
    }
});

closeModalBtn.addEventListener('click', hideModal);

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    fetchTasks();
});