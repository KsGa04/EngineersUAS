document.addEventListener("DOMContentLoaded", async () => {
    const candidatesContainer = document.querySelector('.candidates__items');
    const searchInput = document.getElementById('searchInput');
    const showButton = document.querySelector('.filter__button');
    const paginationContainer = document.querySelector('.pagination');

    const regionSelect = document.getElementById('regionSelect');
    const directionSelect = document.getElementById('directionSelect');
    const universitySelect = document.getElementById('universitySelect');
    const skillsSelect = document.getElementById('skillsSelect');
    let currentPage = 1;
    let totalPages = 1;
    console.log(skillsSelect)
    // Load and render candidates
    async function loadCandidates(page = 1) {
        try {
            const queryParams = new URLSearchParams({
                page: page,
                limit: 10,
                search: searchInput.value || '',
                region: regionSelect.value || '',
                university: universitySelect.value || '',
                direction: directionSelect.value || '',
                skill: document.getElementById("skillsSelect").value,
            });

            const response = await fetch(`/api/candidates?${queryParams.toString()}`);
            const data = await response.json();

            totalPages = data.total_pages || 1;
            renderCandidates(data.candidates || []);
            updatePagination();
        } catch (error) {
            console.error('Ошибка загрузки данных кандидатов:', error);
            candidatesContainer.innerHTML = '<p>Ошибка загрузки данных кандидатов</p>';
        }
    }

    // Render candidates
    function renderCandidates(candidates) {
        candidatesContainer.innerHTML = '';

        if (candidates.length === 0) {
            candidatesContainer.innerHTML = '<p>Кандидаты не найдены.</p>';
            return;
        }

        candidates.forEach(candidate => {
            const resumes = candidate.resumes || [];
            const resume = resumes[0] || {};
            const education = (resume.educations && resume.educations[0]) || {};
            const universityName = education.university_name || 'Не указан';
            const directionName = education.direction_name || 'Не указано';
            const city = education.city || 'Город не указан';

            const resumeLink = resume.id_pattern ? `/pattern${resume.id_pattern}/${candidate.id_user}` : '#';
            const skillsList = (resume.skills || []).map(skill => `<div class="candidate__skill__item">${skill.skill_name}</div>`).join('') || '<div class="candidate__skill__item">Нет навыков</div>';

            const candidateElement = document.createElement('a');
            candidateElement.href = resumeLink;
            candidateElement.classList.add('candidate__item');
            candidateElement.target = '_blank';
            candidateElement.innerHTML = `
                <div class="candidate__item__main">
                    <div class="candidate__name"><h2>${candidate.first_name} ${candidate.last_name}</h2></div>
                    <div class="candidate__university">${city}</div>
                    <div class="candidate__university">${universityName}</div>
                    <div class="candidate__direction">${directionName}</div>
                    <div class="candidate__skills__items">${skillsList}</div>
                </div>
                <div class="candidate__item__photo">
                    <img src="${candidate.profile_photo || 'static/assets/images/user__avatar.png'}" alt="Фото кандидата">
                </div>
            `;

            candidatesContainer.appendChild(candidateElement);
        });
    }

    // Update pagination
    function updatePagination() {
        paginationContainer.innerHTML = '';

        for (let page = 1; page <= totalPages; page++) {
            const pageButton = document.createElement('button');
            pageButton.textContent = page;
            pageButton.classList.add('pagination__button');
            if (page === currentPage) {
                pageButton.classList.add('active');
            }
            pageButton.addEventListener('click', () => {
                currentPage = page;
                loadCandidates(currentPage);
            });
            paginationContainer.appendChild(pageButton);
        }
    }

    // Populate select options
    async function populateFilters() {
        try {
            const [regionResponse, universityResponse, directionResponse, skillsResponse] = await Promise.all([
                fetch('/api/regions'),
                fetch('/api/universities'),
                fetch('/api/directions'),
                fetch('/get/skills')
            ]);

            const regions = await regionResponse.json();
            const universities = await universityResponse.json();
            const directions = await directionResponse.json();
            const skills = await skillsResponse.json();

            populateSelect(regionSelect, regions);
            populateSelect(universitySelect, universities, 'id', 'name');
            populateSelect(directionSelect, directions, 'id', 'name');
            populateSelect(skillsSelect, skills, 'id', 'skill_name');
        } catch (error) {
            console.error('Ошибка загрузки данных для фильтров:', error);
        }
    }

    function populateSelect(selectElement, data, valueKey = '', textKey = '') {
        selectElement.innerHTML = '<option value="">Все</option>';
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = textKey ? item[textKey] : item; // Default to textKey if valueKey is not set
            option.textContent = textKey ? item[textKey] : item;
            selectElement.appendChild(option);
        });
    }


    // Event listeners
    searchInput.addEventListener('input', (event) => {
        event.preventDefault();
        currentPage = 1;
        loadCandidates(currentPage);
    });

    showButton.addEventListener('click', (event) => {
        event.preventDefault();
        currentPage = 1;
        loadCandidates(currentPage);
    });

    // Initial load
    await populateFilters();
    loadCandidates(currentPage);
});
