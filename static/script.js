const API_URL = '/api/tasks';
const taskInput = document.getElementById('taskInput');
const taskList = document.getElementById('taskList');

// Fetch tasks on load
document.addEventListener('DOMContentLoaded', fetchTasks);

// Event Listeners
taskInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTask();
});

async function fetchTasks() {
    try {
        const res = await fetch(API_URL);
        const data = await res.json();
        renderTasks(data.tasks);
    } catch (err) {
        console.error("Failed to fetch tasks:", err);
    }
}

function renderTasks(tasks) {
    taskList.innerHTML = '';

    if (tasks.length === 0) {
        taskList.innerHTML = '<div class="empty-state">No tasks to do. Enjoy your day! ✨</div>';
        return;
    }

    tasks.forEach((task, index) => {
        const li = document.createElement('li');
        // Add staggered animation delay
        li.style.animationDelay = `${index * 0.05}s`;
        li.dataset.id = task.id; // Store ID for animation/selection

        li.innerHTML = `
            <span>${escapeHtml(task.content)}</span>
            <button class="delete-btn" onclick="deleteTask(${task.id})" aria-label="Delete task">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
            </button>
        `;
        taskList.appendChild(li);
    });
}

async function addTask() {
    const task = taskInput.value.trim();
    if (!task) return;

    // Optimistic Update (optional, but good for UX)
    // For now we'll just wait for the server

    try {
        const res = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ task })
        });

        if (res.ok) {
            taskInput.value = '';
            // Get the new list directly from response to update
            const data = await res.json();
            renderTasks(data.tasks);
            taskInput.focus();
        }
    } catch (err) {
        console.error("Error adding task:", err);
    }
}

async function deleteTask(id) {
    // Add exit animation
    // Find the LI with this ID
    const li = document.querySelector(`li[data-id='${id}']`);
    if (li) {
        li.style.transition = 'all 0.3s ease';
        li.style.opacity = '0';
        li.style.transform = 'translateX(20px)';
    }

    // Wait for animation
    setTimeout(async () => {
        try {
            const res = await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
            if (res.ok) {
                const data = await res.json();
                renderTasks(data.tasks);
            }
        } catch (err) {
            console.error("Error deleting task:", err);
        }
    }, 300);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
