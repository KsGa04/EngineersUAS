// Function to delete selected projects
    function deleteSelectedProjects() {
        const selectedItems = document.querySelectorAll('.project-item.selected');
        if (selectedItems.length === 0) {
            alert("Please select at least one project to delete.");
            return;
        }

        selectedItems.forEach(item => {
            const projectId = item.dataset.projectId;
            fetch(`/universal/projects?id_project=${projectId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                console.log("Project deleted:", data);
                loadExistingProjects();
                alert("Project deleted successfully.");
            })
            .catch(error => {
                console.error("Error deleting project:", error);
                alert(`Error deleting project: ${error.message}`);
            });
        });
    }
function saveNewProject() {
        const id_resume = localStorage.getItem("id_resume");
        if (!id_resume) {
            alert("Resume ID is missing.");
            return;
        }

        const newProjectData = {
            project_name: document.getElementById("project-name").value,
            project_description: document.getElementById("project-desc").value,
            project_link: document.getElementById("project-link").value
        };

        for (const [key, value] of Object.entries(newProjectData)) {
            if (value.trim() === "") {
                alert(`Please fill out the ${key.replace('_', ' ')} field.`);
                return;
            }
        }

        fetch(`/api/project/${id_resume}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newProjectData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Project added:", data);
            loadExistingProjects();
            alert("Project added successfully.");
        })
        .catch(error => {
            console.error("Error adding project:", error);
            alert(`Error adding project: ${error.message}`);
        });
    }
// Function to load existing projects
    function loadExistingProjects() {
        const id_resume = localStorage.getItem("id_resume");
        if (!id_resume) {
            console.error("ID пользователя не найден в localStorage.");
            alert("ID пользователя не найден.");
            return;
        }

        fetch(`/api/projects/${id_resume}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            const projectList = document.getElementById('project-list');
            if (!projectList) {
                console.error("Element #project-list not found.");
                return;
            }

            projectList.innerHTML = '';

            if (data.length === 0) {
                projectList.innerHTML = '<p>Нет добавленных проектов.</p>';
            } else {
                data.forEach((project, index) => {
                    const listItem = document.createElement('div');
                    listItem.className = 'project-item';
                    listItem.tabIndex = 0;
                    listItem.dataset.projectId = project.id_project;

                    listItem.style.cursor = "pointer";
                    listItem.addEventListener('click', () => {
                        document.querySelectorAll('.project-item').forEach(item => {
                            item.style.backgroundColor = '';
                            item.classList.remove('selected');
                        });
                        listItem.style.backgroundColor = '#5198DC';
                        listItem.classList.add('selected');
                    });

                    const label = document.createElement('div');
                    label.className = 'project-label';
                    label.textContent = `${project.project_name} (${project.project_description})`;

                    listItem.appendChild(label);
                    projectList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error("Ошибка загрузки списка проектов:", error);
            alert(`Ошибка загрузки списка проектов: ${error.message}`);
        });
    }
function editSelectedProject() {
    const selectedItem = document.querySelector('.project-item.selected');
    const id_user = localStorage.getItem("user_id");
    if (!selectedItem) {
        alert("Please select a project item to edit.");
        return;
    }

    const projectId = selectedItem.dataset.projectId;
    fetch(`/api/projects/${id_user}/${projectId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(project => {
        openModal("Edit Project", `
            <label for="project-name">Project Name</label>
            <input id="project-name" type="text" value="${project.project_name}">
            <label for="project-desc">Project Description</label>
            <input id="project-desc" value="${project.project_description}">
            <label for="project-link">Project Link</label>
            <input id="project-link" type="url" value="${project.project_link}">
            <button onclick="saveEditedProject(${projectId})">Save</button>
        `);
    })
    .catch(error => {
        console.error("Error loading project for editing:", error);
        alert(`Error loading project: ${error.message}`);
    });
}
function saveEditedProject(projectId) {
        const id_user = localStorage.getItem("user_id");
        if (!projectId) {
            alert("Project ID is missing.");
            return;
        }

        const updatedData = {
            project_name: document.getElementById("project-name").value,
            project_description: document.getElementById("project-desc").value,
            project_link: document.getElementById("project-link").value
        };

        fetch(`/api/projects/${id_user}/${projectId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Project updated:", data);
            loadExistingProjects();
            alert("Project updated successfully.");
        })
        .catch(error => {
            console.error("Error updating project:", error);
            alert(`Error updating project: ${error.message}`);
        });
    }
document.addEventListener("DOMContentLoaded", function() {
    // Function to open a modal
    function openModal(title, content, onSave) {
        const modalOverlay = document.getElementById("modal-overlay");
        const modalContent = document.getElementById("modal-content");
        const modalTitle = document.getElementById("modal-title");

        if (!modalOverlay || !modalContent || !modalTitle) {
            console.error("Modal elements not found in the DOM.");
            return;
        }

        modalTitle.textContent = title;
        modalContent.innerHTML = content;
        modalOverlay.style.display = "block";

        document.getElementById("modal-close").onclick = function() {
            modalOverlay.style.display = "none";
        };

        window.onclick = function(event) {
            if (event.target === modalOverlay) {
                modalOverlay.style.display = "none";
            }
        };
    }

    // Function to edit a selected project
    function fillEditProjectModal() {
        const selectedItem = document.querySelector('.project-item.selected');
        const id_user = localStorage.getItem("user_id");
        if (!selectedItem) {
            alert("Please select a project to edit.");
            return;
        }

        const projectId = selectedItem.dataset.projectId;
        fetch(`/api/project/${id_user}/${projectId}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(project => {
            openModal("Edit Project", `
                <label for="project-name">Название проекта</label>
                <input id="project-name" type="text" value="${project.project_name}">
                <label for="project-desc">Описание проекта</label>
                <input id="project-desc" value="${project.project_description}">
                <label for="project-link">Ссылка на проект</label>
                <input id="project-link" type="url" value="${project.project_link}">
                <button onclick="saveEditedProject(${projectId})">Save</button>
            `);
        })
        .catch(error => {
            console.error("Error loading project for editing:", error);
            alert(`Error loading project: ${error.message}`);
        });
    }

    // Event listener to open the modal for adding/editing projects
    document.querySelector(".projects__item a").addEventListener("click", function(event) {
        event.preventDefault();
        openModal("Проекты", `
            <div class="tab-container">
                <button class="tab-button" onclick="showTabContent('view-projects')">Просмотр</button>
                <button class="tab-button" onclick="showTabContent('add-edit-projects')">Добавить/Изменить</button>
            </div>
            <div id="tab-view-projects" class="tab-content">
                <h4>Список добавленных проектов</h4>
                <div id="project-list">
                    <!-- Список проектов будет загружен динамически -->
                </div>
                <button onclick="deleteSelectedProjects()">Удалить выбранное</button>
                <button onclick="editSelectedProject()">Изменить выбранное</button>
            </div>
            <div id="tab-add-edit-projects" class="tab-content" style="display: none;">
                <label for="project-name">Название проекта</label>
                <input id="project-name" type="text" placeholder="Введите название проекта">
                <label for="project-desc">Описание проекта</label>
                <input id="project-desc" placeholder="Описание проекта">
                <label for="project-link">Ссылка на проект</label>
                <input id="project-link" type="url" placeholder="URL проекта">
                <button onclick="saveNewProject()">Сохранить</button>
            </div>
        `, loadExistingProjects());
    });

    // Show tab content
    function showTabContent(tabName) {
        document.querySelectorAll('.tab-content').forEach(tab => {
            tab.style.display = 'none';
            tab.classList.remove('active');
        });

        const tabContent = document.getElementById(`tab-${tabName}`);
        if (tabContent) {
            tabContent.style.display = 'block';
            tabContent.classList.add('active');
        } else {
            console.error(`Tab content with ID 'tab-${tabName}' not found`);
        }
    }
});
