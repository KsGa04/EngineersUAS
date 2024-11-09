document.addEventListener("DOMContentLoaded", function() {
    function openModal(title, content, onSave) {
        const modalOverlay = document.getElementById("modal-overlay");
        const modalContent = document.getElementById("modal-content");
        const modalTitle = document.getElementById("modal-title");
        const modalSubmit = document.getElementById("modal-submit");

        if (!modalOverlay || !modalContent || !modalTitle || !modalSubmit) {
            console.error("Элементы модального окна не найдены в DOM.");
            return;
        }

        modalTitle.textContent = title;
        modalContent.innerHTML = content;
        modalOverlay.style.display = "block";

        modalSubmit.onclick = function () {
            if (validateFields()) {
                modalOverlay.style.display = "none";
                if (onSave && typeof onSave === "function") {
                    onSave();
                }
            } else {
                alert("Пожалуйста, заполните все поля.");
            }
        };

        document.getElementById("modal-close").onclick = function() {
            modalOverlay.style.display = "none";
        };

        window.onclick = function(event) {
            if (event.target === modalOverlay) {
                modalOverlay.style.display = "none";
            }
        };
    }

    function validateFields() {
        const modalContent = document.getElementById("modal-content");
        const requiredFields = modalContent.querySelectorAll("input, select, textarea");
        for (const field of requiredFields) {
            if ((field.type === "text" || field.tagName === "TEXTAREA" || field.type === "date") && field.value.trim() === "") {
                return false;
            }
            if (field.tagName === "SELECT" && field.value === "") {
                return false;
            }
        }
        return true;
    }

    function loadExistingProjects() {
        const id_user = localStorage.getItem("user_id");
        if (!id_user) {
            console.error("ID пользователя не найден в localStorage.");
            alert("ID пользователя не найден.");
            return;
        }

        fetch(`/universal_api/universal/projects?user_id=${id_user}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status} - ${response.statusText}`);
            }
            const contentType = response.headers.get("content-type");
            if (contentType && contentType.includes("application/json")) {
                return response.json();
            } else {
                return response.text().then(text => {
                    console.error("Получен не-JSON ответ:", text);
                    throw new Error("Ответ сервера не в формате JSON. Проверьте ответ сервера.");
                });
            }
        })
        .then(data => {
            console.log("Полученные данные проектов:", data);
            const projectList = document.getElementById('project-list');
            if (!projectList) {
                console.error("Элемент #project-list не найден.");
                return;
            }

            projectList.innerHTML = '';

            if (data.length === 0) {
                projectList.innerHTML = '<p>Нет добавленных проектов.</p>';
            } else {
                data.forEach((project, index) => {
                    const listItem = document.createElement('div');
                    listItem.className = 'project-item';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `project-${index}`;
                    checkbox.value = project.id_project;

                    const label = document.createElement('label');
                    label.htmlFor = `project-${index}`;
                    label.textContent = `${project.project_name} (${project.project_description})`;

                    listItem.appendChild(checkbox);
                    listItem.appendChild(label);

                    projectList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error("Ошибка загрузки списка проектов:", error);
            alert(`Ошибка загрузки списка проектов: ${error.message}. Проверьте правильность работы API.`);
        });
    }

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
                    <!-- Список чекбоксов будет загружен динамически -->
                </div>
                <button onclick="deleteSelectedProjects()">Удалить выбранное</button>
                <button onclick="editSelectedProject()">Изменить выбранное</button>
            </div>
            <div id="tab-add-edit-projects" class="tab-content" style="display: none;">
                <label for="project-name">Название проекта</label>
                <input id="project-name" type="text" placeholder="Введите название проекта">
                <label for="project-desc">Описание проекта</label>
                <textarea id="project-desc" placeholder="Описание проекта"></textarea>
                <label for="project-link">Ссылка на проект</label>
                <input id="project-link" type="url" placeholder="URL проекта">
                <button id="modal-submit">Сохранить</button>
            </div>
        `, loadExistingProjects);
    });

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
