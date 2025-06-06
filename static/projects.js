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
        const selectedSkills = Array.from(document.getElementById("project-skills").selectedOptions).map(opt => parseInt(opt.value));
        const newProjectData = {
            project_name: document.getElementById("project-name").value,
            project_description: document.getElementById("project-desc").value,
            project_link: document.getElementById("project-link").value,
            skills: selectedSkills  // Include selected skills
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
async function loadSkills() {
        try {
            const response = await fetch('/api/skills');
            const skills = await response.json();
            const skillsSelect = document.getElementById("project-skills");
            skillsSelect.innerHTML = skills.map(skill => `<option value="${skill.id_skill}">${skill.skill_name}</option>`).join('');
        } catch (error) {
            console.error("Error loading skills:", error);
        }
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
            openModal("Изменение проекта", `
                <label for="project-name">Название</label>
                <input id="project-name" type="text" value="${project.project_name}">
                <label for="project-desc">Описание</label>
                <input id="project-desc" value="${project.project_description}">
                <label for="project-link">Ссылка</label>
                <input id="project-link" type="url" value="${project.project_link}">
                <div class="skills-container">
                    <label for="skills-dropdown">Выберите навык:</label>
                    <select id="skills-dropdown">
                        <!-- Опции будут добавлены динамически -->
                    </select>
                    <button id="add-skill-btn">Добавить навык</button>
                </div>
                <div id="selected-skills" class="selected-skills">
                    ${project.skill.map(skill => `
                        <div class="skill-block" data-id="${skill.id_skill}">
                            <span>${skill.skill_name}</span>
                            <button onclick="removeSkill(${projectId}, ${skill.id_skill})">&times;</button>
                        </div>
                    `).join('')}
                </div>
                <button onclick="saveEditedProject(${projectId})">Сохранить</button>
            `);

            loadSkillsDropdown(project.skill.map(skill => skill.id_skill));
            // Привязка события для добавления навыков
            const addSkillBtn = document.getElementById("add-skill-btn");
            addSkillBtn.addEventListener("click", function () {
                addSkillToProject(projectId);
            });
        })
        .catch(error => {
            console.error("Error loading project for editing:", error);
            alert(`Error loading project: ${error.message}`);
        });
}

async function loadSkillsDropdown(selectedSkills) {
    try {
            const response = await fetch("/api/skills");
            if (!response.ok) throw new Error("Не удалось загрузить навыки.");
            const skills = await response.json();
            const skillsDropdown = document.getElementById('skills-dropdown');
            skillsDropdown.innerHTML = ""; // Очистка существующих опций
            skills.forEach(skill => {
                const option = document.createElement("option");
                option.value = skill.id;
                option.textContent = skill.name;
                skillsDropdown.appendChild(option);
            });
        } catch (error) {
            console.error("Ошибка загрузки навыков:", error);
        }
}

function addSkillToProject(projectId) {
    const skillsDropdown = document.getElementById("skills-dropdown");
    const selectedSkillId = skillsDropdown.value;
    const selectedSkillName = skillsDropdown.options[skillsDropdown.selectedIndex].text;

    if (!selectedSkillId) {
        alert("Please select a skill.");
        return;
    }

    fetch(`/api/projects/${projectId}/skills`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_skill: selectedSkillId })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to add skill to project");
            }
            return response.json();
        })
        .then(() => {
            // Обновляем отображение навыков
            const selectedSkillsContainer = document.getElementById('selected-skills');
            const skillBlock = document.createElement('div');
            skillBlock.classList.add('skill-block');
            skillBlock.dataset.id = selectedSkillId;
            skillBlock.innerHTML = `
                <span>${selectedSkillName}</span>
                <button onclick="removeSkill(${projectId}, ${selectedSkillId})">&times;</button>
            `;
            selectedSkillsContainer.appendChild(skillBlock);

            // Перезагружаем dropdown с обновленными навыками
            const selectedSkills = Array.from(selectedSkillsContainer.children).map(
                skillBlock => parseInt(skillBlock.dataset.id, 10)
            );
            loadSkillsDropdown(selectedSkills);
        })
        .catch(error => {
            console.error("Error adding skill to project:", error);
            alert("Failed to add skill.");
        });
}

function removeSkill(projectId, skillId) {
    fetch(`/api/projects/${projectId}/skills/${skillId}`, {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' }
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Failed to remove skill from project");
            }
            return response.json();
        })
        .then(data => {
            const skillBlock = document.querySelector(`.skill-block[data-id="${skillId}"]`);
            if (skillBlock) {
                skillBlock.remove();
            }

            // Обновляем dropdown
            const skillsDropdown = document.getElementById('skills-dropdown');
            const option = [...skillsDropdown.options].find(opt => opt.value == skillId);
            if (option) {
                option.disabled = false;
            }
        })
        .catch(error => {
            console.error("Error removing skill from project:", error);
            alert("Failed to remove skill.");
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
    // Function to load available skills
    async function loadSkills() {
        try {
            const response = await fetch('/api/skills');
            const skills = await response.json();
            const skillsSelect = document.getElementById("project-skills");
            skillsSelect.innerHTML = skills
                .map(skill => `<option value="${skill.id_skill}">${skill.skill_name}</option>`)
                .join('');
        } catch (error) {
            console.error("Error loading skills:", error);
        }
    }

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
    async function fillEditProjectModal() {
        const selectedItem = document.querySelector('.project-item.selected');
        const id_user = localStorage.getItem("user_id");
        if (!selectedItem) {
            alert("Please select a project to edit.");
            return;
        }

        const projectId = selectedItem.dataset.projectId;
        await fetch(`/api/project/${id_user}/${projectId}`, {
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
                <select id="project-skills" multiple>
                ${project.skill.map(skill => `<option value="${skill.id_skill}" ${project.skill.includes(skill.id_skill) ? 'selected' : ''}>${skill.skill_name}</option>`).join('')}
            </select>
                <button onclick="saveEditedProject(${projectId})">Save</button>
            `);
        })
        .catch(error => {
            console.error("Error loading project for editing:", error);
            alert(`Error loading project: ${error.message}`);
        });
    }

    // Event listener to open the modal for adding/editing projects
    document.querySelector(".projects__item textarea").addEventListener("click", () => {
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
