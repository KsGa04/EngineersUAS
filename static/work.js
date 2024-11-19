function fillEditWorkModal() {
    const selectedItem = document.querySelector('.work-item.selected');
    const id_user = localStorage.getItem("user_id");
    if (!selectedItem) {
        alert("Пожалуйста выберите пункт для изменения данных");
        return;
    }

    const workId = selectedItem.dataset.workId;

    // Fetch details for the selected work experience
    fetch(`/api/works/${id_user}/${workId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(work => {
        // Fetch necessary dropdown data from the API
        Promise.all([
            fetch('/api/organizations').then(res => res.json())
        ])
        .then(([organizations]) => {
            // Create organization options
            const organizationOptions = organizations.map(org =>
                `<option value="${org.id}" ${org.id === work.organization_id ? 'selected' : ''}>${org.name}</option>`
            ).join('');

            // Populate the modal with data
            openModal("Изменение опыта работы", `
                <label for="organization">Организация</label>
                <select id="organization">${organizationOptions}</select>
                <label for="position">Должность</label>
                <input id="position" type="text" value="${work.position}">
                <label for="start-date">Начало работы</label>
                <input id="start-date" type="date" value="${new Date(work.start_date).toISOString().split('T')[0]}">
                <label for="end-date">Окончание работы</label>
                <input id="end-date" type="date" value="${new Date(work.end_date).toISOString().split('T')[0]}">
                <label for="responsibilities">Обязанности</label>
                <input id="responsibilities" value="${work.responsibilities || ''}">
                <button onclick="saveEditedWork(${workId})">Сохранить</button>
            `);
        })
        .catch(error => {
            console.error("Error loading dropdown data:", error);
            alert("Failed to load related data for editing.");
        });
    })
    .catch(error => {
        console.error("Error loading work for editing:", error);
        alert(`Error loading work: ${error.message}`);
    });
}
function saveNewWorkExperience() {
        const id_user = localStorage.getItem("user_id");
        if (!id_user) {
            alert("User ID not found.");
            return;
        }

        const newWorkData = {
            organization: document.getElementById("organization").value,
            position: document.getElementById("position").value,
            start_date: document.getElementById("start-date").value,
            end_date: document.getElementById("end-date").value,
            responsibilities: document.getElementById("responsibilities").value
        };

        // Validate required fields
        for (const [key, value] of Object.entries(newWorkData)) {
            if (value.trim() === "") {
                alert(`Please fill out the ${key.replace('_', ' ')} field.`);
                return;
            }
        }

        // Validate date consistency (start_date should not be after end_date)
        if (new Date(newWorkData.start_date) > new Date(newWorkData.end_date)) {
            alert("Начальная дата не может быть после окончания");
            return;
        }

        fetch(`/api/works/${id_user}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(newWorkData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Опыт работы был добавлен:", data);
            loadExistingWorkExperience(); // Refresh the work list after addition
            alert("Опыт работы был добавлен");
        })
        .catch(error => {
            console.error("Ошибка при добавлении опыта работы:", error);
            alert(`Error adding work experience: ${error.message}.`);
        });
    }
function saveEditedWork(workId) {
        const id_user = localStorage.getItem("user_id");
        if (!workId) {
            alert("Работа ID не найден.");
            return;
        }

        const updatedData = {
            organization: document.getElementById("organization").value,
            position: document.getElementById("position").value,
            start_date: document.getElementById("start-date").value,
            end_date: document.getElementById("end-date").value,
            responsibilities: document.getElementById("responsibilities").value
        };
        // Validate required fields
        for (const [key, value] of Object.entries(updatedData)) {
            if (value.trim() === "") {
                alert(`Пожалуйста заполните поле ${key.replace('_', ' ')}.`);
                return;
            }
        }

        // Validate date consistency (start_date should not be after end_date)
        if (new Date(updatedData.start_date) > new Date(updatedData.end_date)) {
            alert("Начальная дата не может быть после окончания");
            return;
        }
        fetch(`/api/works/${id_user}/${workId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedData)
        })
        .then(response => response.json())
        .then(data => {
            console.log("Опыт работы был изменен:", data);
            alert("Опыт работы был изменен.");
        })
        .catch(error => {
            console.error("Error updating work experience:", error);
            alert(`Error updating work experience: ${error.message}`);
        });
    }
function deleteSelectedWorks() {
        const selectedItems = document.querySelectorAll('.work-item.selected');
        if (selectedItems.length === 0) {
            alert("Выберите пункт для удаления");
            return;
        }

        selectedItems.forEach(item => {
            const workId = item.dataset.workId;
            fetch(`/universal/work?id_work=${workId}`, {
                method: 'DELETE',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log("Опыт работы удален:", data);
                loadExistingWorkExperience();
            })
            .catch(error => {
                console.error("Ошибка при удалении опыта работы:", error);
                alert(`Error deleting work experience: ${error.message}`);
            });
        });
    }
function loadExistingWorkExperience() {
        const id_resume = localStorage.getItem("id_resume");
        if (!id_resume) {
            console.error("Resume ID not found in localStorage.");
            alert("Резюме ID не найден.");
            return;
        }

        fetch(`/api/works/${id_resume}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Work experience data received:", data);
            const workList = document.getElementById('work-list');
            if (!workList) {
                console.error("Element #work-list not found.");
                return;
            }

            workList.innerHTML = '';
            if (data.length === 0) {
                workList.innerHTML = '<p>Опыт работы отсутствует</p>';
            } else {
                data.forEach((work, index) => {
                    const listItem = document.createElement('div');
                    listItem.className = 'work-item';
                    listItem.tabIndex = 0;
                    listItem.dataset.workId = work.id_work;
                    listItem.style.cursor = "pointer";

                    listItem.addEventListener('click', () => {
                        document.querySelectorAll('.work-item').forEach(item => {
                            item.style.backgroundColor = '';
                            item.classList.remove('selected');
                        });
                        listItem.style.backgroundColor = '#5198DC';
                        listItem.classList.add('selected');
                    });

                    const label = document.createElement('div');
                    label.className = 'work-label';
                    label.textContent = `${work.position} - ${work.organizations.map(org => org.organization_name).join(", ")} (${new Date(work.start_date).toLocaleDateString()} - ${new Date(work.end_date).toLocaleDateString()})`;

                    listItem.appendChild(label);
                    workList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error("Ошибка при загрузке опыта работы:", error);
            alert(`Error loading work experiences: ${error.message}`);
        });
    }
document.addEventListener("DOMContentLoaded", function () {
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

        document.getElementById("modal-close").onclick = function () {
            modalOverlay.style.display = "none";
        };

        window.onclick = function (event) {
            if (event.target === modalOverlay) {
                modalOverlay.style.display = "none";
            }
        };
    }

    function fillEditWorkModal() {
    const selectedItem = document.querySelector('.work-item.selected');
    const id_user = localStorage.getItem("user_id");
    if (!selectedItem) {
        alert("Пожалуйста выберите пункт для изменения");
        return;
    }

    const workId = selectedItem.dataset.workId;

    // Fetch details for the selected work experience
    fetch(`/api/works/${id_user}/${workId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(work => {
        // Fetch necessary dropdown data from the API
        Promise.all([
            fetch('/api/organizations').then(res => res.json())
        ])
        .then(([organizations]) => {
            // Create organization options
            const organizationOptions = organizations.map(org =>
                `<option value="${org.id}" ${org.id === work.organization_id ? 'selected' : ''}>${org.name}</option>`
            ).join('');

            // Populate the modal with data
            openModal("Изменение опыта работы", `
                <label for="organization">Организация</label>
                <select id="organization">${organizationOptions}</select>
                <label for="position">Должность</label>
                <input id="position" type="text" value="${work.position}">
                <label for="start-date">Начало работы</label>
                <input id="start-date" type="date" value="${new Date(work.start_date).toISOString().split('T')[0]}">
                <label for="end-date">Окончание работы</label>
                <input id="end-date" type="date" value="${new Date(work.end_date).toISOString().split('T')[0]}">
                <label for="responsibilities">Обязанности</label>
                <input id="responsibilities" value="${work.responsibilities || ''}">
                <button onclick="saveEditedWork(${workId})">Save</button>
            `);
        })
        .catch(error => {
            console.error("Error loading dropdown data:", error);
            alert("Загрузка данных для изменения опыта работы не удалась.");
        });
    })
    .catch(error => {
        console.error("Error loading work for editing:", error);
        alert(`Error loading work: ${error.message}`);
    });
}
    document.querySelector(".groupnumber__item textarea").addEventListener("click", () => {
        openModal("Опыт работы", `
            <div class="tab-container">
                <button class="tab-button" onclick="showTabContent('view-work')">Просмотреть</button>
                <button class="tab-button" onclick="showTabContent('add-edit-work')">Добавить</button>
            </div>
            <div id="tab-view-work" class="tab-content">
                <h4>Список добавленных карьер</h4>
                <div id="work-list">
                    <!-- Work list will be dynamically loaded -->
                </div>
                <button onclick="deleteSelectedWorks()">Удалить</button>
                <button onclick="fillEditWorkModal()">Изменить</button>
            </div>
            <div id="tab-add-edit-work" class="tab-content" style="display: none;">
                <label for="organization">Организация</label>
                <select id="organization">Загрузка...</select>
                <label for="position">Должность</label>
                <input id="position" type="text" placeholder="Напишите должность">
                <label for="start-date">Начало работы</label>
                <input id="start-date" type="date">
                <label for="end-date">Окончание работы</label>
                <input id="end-date" type="date">
                <label for="responsibilities">Обязанности</label>
                <input id="responsibilities">
                <button onclick="saveNewWorkExperience()">Сохранить</button>
            </div>
        `, loadExistingWorkExperience());
        loadOrganizationDropdown();
    });
    function loadOrganizationDropdown() {
    fetch('/api/organizations')
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(organizations => {
            const organizationSelect = document.getElementById('organization');
            organizationSelect.innerHTML = organizations.map(org =>
                `<option value="${org.id}">${org.name}</option>`
            ).join('');
        })
        .catch(error => {
            console.error("Error loading organizations:", error);
            alert("Failed to load organizations.");
        });
}
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
