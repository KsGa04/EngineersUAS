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

    function loadExistingWorkExperience() {
        const id_user = localStorage.getItem("user_id");
        if (!id_user) {
            console.error("ID пользователя не найден в localStorage.");
            alert("ID пользователя не найден.");
            return;
        }

        fetch(`/universal_api/universal/work_experience?user_id=${id_user}`, {
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
            console.log("Полученные данные опыта работы:", data);
            const workList = document.getElementById('work-list');
            if (!workList) {
                console.error("Элемент #work-list не найден.");
                return;
            }

            workList.innerHTML = '';

            if (data.length === 0) {
                workList.innerHTML = '<p>Нет добавленного опыта работы.</p>';
            } else {
                data.forEach((work, index) => {
                    const listItem = document.createElement('div');
                    listItem.className = 'work-item';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = `work-${index}`;
                    checkbox.value = work.id_work;

                    const label = document.createElement('label');
                    label.htmlFor = `work-${index}`;
                    label.textContent = `${work.position} - ${work.organization} (${new Date(work.start_date).toLocaleDateString()} - ${new Date(work.end_date).toLocaleDateString()})`;

                    listItem.appendChild(checkbox);
                    listItem.appendChild(label);

                    workList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error("Ошибка загрузки списка опыта работы:", error);
            alert(`Ошибка загрузки списка опыта работы: ${error.message}. Проверьте правильность работы API.`);
        });
    }

    document.querySelector(".groupnumber__item textarea").addEventListener("click", () => {
        openModal("Опыт работы", `
            <div class="tab-container">
                <button class="tab-button" onclick="showTabContent('view-work')">Просмотр</button>
                <button class="tab-button" onclick="showTabContent('add-edit-work')">Добавить/Изменить</button>
            </div>
            <div id="tab-view-work" class="tab-content">
                <h4>Список добавленного опыта работы</h4>
                <div id="work-list">
                    <!-- Список чекбоксов будет загружен динамически -->
                </div>
                <button onclick="deleteSelectedWorks()">Удалить выбранное</button>
                <button onclick="editSelectedWork()">Изменить выбранное</button>
            </div>
            <div id="tab-add-edit-work" class="tab-content" style="display: none;">
                <label for="organization">Организация</label>
                <select id="organization"><option>Загрузка...</option></select>
                <label for="position">Должность</label>
                <input id="position" type="text" placeholder="Введите должность">
                <label for="start-date">Год начала</label>
                <input id="start-date" type="date">
                <label for="end-date">Год окончания</label>
                <input id="end-date" type="date">
                <label for="responsibilities">Обязанности</label>
                <textarea id="responsibilities" placeholder="Описание обязанностей"></textarea>
                <button id="modal-submit">Сохранить</button>
            </div>
        `, loadExistingWorkExperience);
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
