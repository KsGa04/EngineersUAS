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

    function loadExistingEducations() {
        const id_user = localStorage.getItem("user_id");
        if (!id_user) {
            console.error("ID пользователя не найден в localStorage.");
            alert("ID пользователя не найден.");
            return;
        }

        fetch(`/universal_api/universal/education?user_id=${id_user}`, {
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
            console.log("Полученные данные:", data);
            const educationList = document.getElementById('education-list');
            if (!educationList) {
                console.error("Элемент #education-list не найден.");
                return;
            }

            educationList.innerHTML = '';

            if (data.length === 0) {
                educationList.innerHTML = '<p>Нет добавленных образований.</p>';
            } else {
                data.forEach((education, index) => {
                    const listItem = document.createElement('div');
                    listItem.className = 'education-item';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `education-${index}`;
                    checkbox.value = education.id_education;

                    const label = document.createElement('label');
                    label.htmlFor = `education-${index}`;
                    label.textContent = `${education.degree} - ${education.university} (${new Date(education.start_date).toLocaleDateString()} - ${new Date(education.end_date).toLocaleDateString()})`;

                    listItem.appendChild(checkbox);
                    listItem.appendChild(label);

                    educationList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error("Ошибка загрузки списка образований:", error);
            alert(`Ошибка загрузки списка образований: ${error.message}. Проверьте правильность работы API.`);
        });
    }

    document.querySelector(".bio__item textarea").addEventListener("click", () => {
        console.log("Opening modal for education..."); // Debugging statement
        openModal("Образование", `
            <div class="tab-container">
                <button class="tab-button" onclick="showTabContent('view')">Просмотр</button>
                <button class="tab-button" onclick="showTabContent('add-edit')">Добавить/Изменить</button>
            </div>
            <div id="tab-view" class="tab-content">
                <h4>Список добавленных образований</h4>
                <div id="education-list">
                    <!-- Список чекбоксов будет загружен динамически -->
                </div>
                <button onclick="deleteSelectedEducations()">Удалить выбранное</button>
                <button onclick="editSelectedEducation()">Изменить выбранное</button>
            </div>
            <div id="tab-add-edit" class="tab-content" style="display: none;">
                <label for="degree">Уровень образования</label>
                <select id="degree"><option>Загрузка...</option></select>
                <label for="university">Университет</label>
                <select id="university"><option>Загрузка...</option></select>
                <label for="direction">Направление</label>
                <select id="direction"><option>Выберите университет</option></select>
                <label for="group">Группа</label>
                <select id="group"><option>Выберите направление</option></select>
                <label for="start-year">Год начала</label>
                <input type="date" id="start-year">
                <label for="end-year">Год окончания</label>
                <input type="date" id="end-year">
                <button id="modal-submit">Сохранить</button>
            </div>
        `, loadExistingEducations);
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
function loadExistingEducations() {
        const id_user = localStorage.getItem("user_id");
        if (!id_user) {
            console.error("ID пользователя не найден в localStorage.");
            alert("ID пользователя не найден.");
            return;
        }

        fetch(`/universal_api/universal/education?user_id=${id_user}`, {
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
            console.log("Полученные данные:", data);
            const educationList = document.getElementById('education-list');
            if (!educationList) {
                console.error("Элемент #education-list не найден.");
                return;
            }

            educationList.innerHTML = '';

            if (data.length === 0) {
                educationList.innerHTML = '<p>Нет добавленных образований.</p>';
            } else {
                data.forEach((education, index) => {
                    const listItem = document.createElement('div');
                    listItem.className = 'education-item';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `education-${index}`;
                    checkbox.value = education.id_education;

                    const label = document.createElement('label');
                    label.htmlFor = `education-${index}`;
                    label.textContent = `${education.degree} - ${education.university} (${new Date(education.start_date).toLocaleDateString()} - ${new Date(education.end_date).toLocaleDateString()})`;

                    listItem.appendChild(checkbox);
                    listItem.appendChild(label);

                    educationList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error("Ошибка загрузки списка образований:", error);
            alert(`Ошибка загрузки списка образований: ${error.message}. Проверьте правильность работы API.`);
        });
    }