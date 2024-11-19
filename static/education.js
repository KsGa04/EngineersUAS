function openModal(title, content, onSave) {
        const modalOverlay = document.getElementById("modal-overlay");
        const modalContent = document.getElementById("modal-content");
        const modalTitle = document.getElementById("modal-title");

        if (!modalOverlay || !modalContent || !modalTitle) {
            console.error("Элементы модального окна не найдены в DOM.");
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
function loadExistingEducations() {
        const id_resume = localStorage.getItem("id_resume");
        if (!id_resume) {
            console.error("ID not found in localStorage.");
            alert("User ID not found.");
            return;
        }

        fetch(`/api/educations/${id_resume}`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        })
        .then(response => response.json())
        .then(data => {
            console.log("Received education data:", data);
            const educationList = document.getElementById('education-list');
            if (!educationList) {
                console.error("Element #education-list not found.");
                return;
            }

            educationList.innerHTML = '';
            if (data.length === 0) {
                educationList.innerHTML = '<p>No educations added.</p>';
            } else {
                data.forEach((education, index) => {
                    const listItem = document.createElement('div');
                    listItem.className = 'education-item';
                    listItem.tabIndex = 0;
                    listItem.dataset.educationId = education.id_education;
                    listItem.style.cursor = "pointer";

                    listItem.addEventListener('click', () => {
                        document.querySelectorAll('.education-item').forEach(item => {
                            item.style.backgroundColor = '';
                            item.classList.remove('selected');
                        });
                        listItem.style.backgroundColor = '#5198DC';
                        listItem.classList.add('selected');
                    });

                    const label = document.createElement('div');
                    label.className = 'education-label';
                    label.textContent = `${education.degree_name} - ${education.university_name} (${new Date(education.start_date).toLocaleDateString()} - ${new Date(education.end_date).toLocaleDateString()})`;

                    listItem.appendChild(label);
                    educationList.appendChild(listItem);
                });
            }
        })
        .catch(error => {
            console.error("Error loading education list:", error);
            alert(`Error loading education list: ${error.message}`);
        });
    }
    function saveNewEducation() {
    const id_user = localStorage.getItem("user_id");
    if (!id_user) {
        alert("User ID is missing.");
        return;
    }

    const newEducationData = {
        university: document.getElementById("university").value,
        degree: document.getElementById("degree").value,
        direction: document.getElementById("direction").value,
        group: document.getElementById("group").value,
        start_date: document.getElementById("start-year").value,
        end_date: document.getElementById("end-year").value
    };

    // Validate required fields
    for (const [key, value] of Object.entries(newEducationData)) {
        if (value.trim() === "") {
            alert(`Пожалуйста заполните поле ${key.replace('_', ' ')}.`);
            return;
        }
    }
    // Validate date consistency (start_date should not be after end_date)
    if (new Date(newEducationData.start_date) > new Date(newEducationData.end_date)) {
        alert("Начальная дата обучения должна быть раньше чем окончание");
        return;
    }
    fetch(`/api/education/${id_user}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newEducationData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Education added:", data);
        loadExistingEducations(); // Refresh the list after adding
        alert("Education added successfully.");
    })
    .catch(error => {
        console.error("Error adding education:", error);
        alert(`Error adding education: ${error.message}`);
    });
}

document.addEventListener("DOMContentLoaded", function() {
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

    // Call this function when the "Add/Edit" button is clicked
    function loadDropdownData() {
        Promise.all([
            fetch('/api/universities').then(res => res.json()),
            fetch('/api/directions').then(res => res.json()),
            fetch('/api/groups').then(res => res.json()),
            fetch('/api/degrees').then(res => res.json())
        ])
        .then(([universities, directions, groups, degree]) => {
            document.getElementById('degree').innerHTML = degree.map(deg => `<option value="${deg.id}">${deg.name}</option>`).join('');
            document.getElementById('university').innerHTML = universities.map(uni => `<option value="${uni.id}">${uni.name}</option>`).join('');
            document.getElementById('direction').innerHTML = directions.map(dir => `<option value="${dir.id}">${dir.name}</option>`).join('');
            document.getElementById('group').innerHTML = groups.map(grp => `<option value="${grp.id}">${grp.name}</option>`).join('');
        })
        .catch(error => {
            console.error("Error loading dropdown data:", error);
            alert("Failed to load dropdown data.");
        });
    }

    // Load dropdown data when the modal is opened for adding/editing
    document.querySelector(".bio__item textarea").addEventListener("click", () => {
        console.log("Opening modal for education..."); // Debugging statement
        openModal("Образование", `
            <div class="tab-container">
                <button class="tab-button" onclick="showTabContent('view')">Просмотреть</button>
                <button class="tab-button" onclick="showTabContent('add-edit')">Добавить</button>
            </div>
            <div id="tab-view" class="tab-content">
                <h4>List of Added Educations</h4>
                <div id="education-list">
                    <!-- Education list will be dynamically loaded -->
                </div>
                <button onclick="deleteSelectedEducations()">Удалить</button>
                <button onclick="fillEditEducationModal()">Изменить</button>
            </div>
            <div id="tab-add-edit" class="tab-content" style="display: none;">
                <label for="degree">Уровень образования</label>
                <select id="degree"><option>Loading...</option></select>
                <label for="university">Университеты</label>
                <select id="university"><option>Loading...</option></select>
                <label for="direction">Направления</label>
                <select id="direction"><option>Select a university</option></select>
                <label for="group">Группы</label>
                <select id="group"><option>Select a direction</option></select>
                <label for="start-year">Начало обучения</label>
                <input type="date" id="start-year">
                <label for="end-year">Окончание обучения</label>
                <input type="date" id="end-year">
                <button onclick="saveNewEducation()">Сохранить</button>
            </div>
        `, loadExistingEducations());
        loadDropdownData(); // Load dropdown data when opening the modal
    });

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
function deleteSelectedEducations() {
        const selectedCheckboxes = document.querySelector('.education-item.selected');
        const educationId = selectedCheckboxes.dataset.educationId;
        if (!educationId) {
            alert("Education ID is missing.");
            return;
        }

        fetch(`/universal/education?id_education=${educationId}`, {
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
                console.log("Education deleted:", data);
                loadExistingEducations();
                alert("Образование было удалено")
            })
            .catch(error => {
                console.error("Error deleting education:", error);
                alert(`Error deleting education: ${error.message}.`);
            });
    }
function fillEditEducationModal() {
    const selectedItem = document.querySelector('.education-item.selected');
    const id_user = localStorage.getItem("user_id");
    const educationId = selectedItem.dataset.educationId;
    if (!educationId) {
        alert("Education ID is missing.");
        return;
    }

    fetch(`/api/education/${id_user}/${educationId}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(education => {
        return Promise.all([
            fetch('/api/universities').then(res => res.json()),
            fetch('/api/directions').then(res => res.json()),
            fetch('/api/groups').then(res => res.json()),
            fetch('/api/degrees').then(res => res.json())
        ])
        .then(([universities, directions, groups, degrees]) => {
            const degreeOptions = degrees.map(deg =>
                `<option value="${deg.id}" ${deg.id === education.degree_id ? 'selected' : ''}>${deg.name}</option>`
            ).join('');
            const universityOptions = universities.map(uni =>
                `<option value="${uni.id}" ${uni.id === education.university_id ? 'selected' : ''}>${uni.name}</option>`
            ).join('');
            const directionOptions = directions.map(dir =>
                `<option value="${dir.id}" ${dir.id === education.direction_id ? 'selected' : ''}>${dir.name}</option>`
            ).join('');
            const groupOptions = groups.map(grp =>
                `<option value="${grp.id}" ${grp.id === education.group_id ? 'selected' : ''}>${grp.name}</option>`
            ).join('');

            openModal("Edit Education", `
                <div class="tab-view">
                    <label for="degree">Уровень образования</label>
                    <select id="degree">${degreeOptions}</select>
                    <label for="university">Университет</label>
                    <select id="university">${universityOptions}</select>
                    <label for="direction">Направление</label>
                    <select id="direction">${directionOptions}</select>
                    <label for="group">Группа</label>
                    <select id="group">${groupOptions}</select>
                    <label for="start-year">Год начала</label>
                    <input type="date" id="start-year" value="${new Date(education.start_date).toISOString().split('T')[0]}">
                    <label for="end-year">Год окончания</label>
                    <input type="date" id="end-year" value="${new Date(education.end_date).toISOString().split('T')[0]}">
                    <button onclick="saveEditedEducation(${educationId})">Сохранить</button>
                </div>
            `);
        });
    })
    .catch(error => {
        console.error("Error loading education for editing:", error);
        alert(`Error loading education: ${error.message}.`);
    });
}
function saveEditedEducation(educationId) {
    const id_user = localStorage.getItem("user_id");
    if (!educationId) {
        alert("Education ID is missing.");
        return;
    }

    const updatedData = {
        degree: document.getElementById("degree").value,
        university: document.getElementById("university").value,
        direction: document.getElementById("direction").value,
        group: document.getElementById("group").value,
        start_date: document.getElementById("start-year").value,
        end_date: document.getElementById("end-year").value
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
        alert("Начальная дата обучения должна быть раньше чем окончание");
        return;
    }
    fetch(`/api/education/${id_user}/${educationId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log("Education updated:", data);
        alert("Education updated successfully.");
    })
    .catch(error => {
        console.error("Error updating education:", error);
        alert(`Error updating education: ${error.message}.`);
    });
}

