document.addEventListener("DOMContentLoaded", async () => {
    const candidatesContainer = document.querySelector('.candidates__items');
    const searchInput = document.getElementById('searchInput');
    const showButton = document.querySelector('.filter__button');

    const regionSelect = document.getElementById('regionSelect');
    const directionSelect = document.getElementById('directionSelect');
    const universitySelect = document.getElementById('universitySelect');
    const skillsSelect = document.getElementById('skillsSelect');

    let allCandidates = [];
    try {
        // Fetch data from the API endpoint
        const response = await fetchWithAuth('/api/candidates');
        allCandidates = await response.json();

        // Initial render of all candidates
        renderCandidates(allCandidates);

        // Attach input event listener for search functionality
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase();
            const filteredCandidates = allCandidates.filter(candidate => {
                const fullName = `${candidate.first_name} ${candidate.last_name} ${candidate.middle_name}`.toLowerCase();
                const universityName = (candidate.resumes[0]?.educations[0]?.university_name || '').toLowerCase();
                const directionName = (candidate.resumes[0]?.educations[0]?.direction_name || '').toLowerCase();
                const skills = candidate.resumes[0]?.skills.map(skill => skill.skill_name.toLowerCase()).join(' ') || '';
                const city = (candidate.resumes[0]?.educations[0]?.city || '').toLowerCase();
                return fullName.includes(query) || universityName.includes(query) || directionName.includes(query) || skills.includes(query) || city.includes(query);
            });

            // Render filtered candidates
            renderCandidates(filteredCandidates);
        });
    } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        candidatesContainer.innerHTML = '<p>Ошибка загрузки данных кандидатов</p>';
    }
    try {
        // Fetch data for the select options
        const [regionResponse, universityResponse, directionResponse, skillsResponse] = await Promise.all([
            fetchWithAuth('/api/regions'),
            fetchWithAuth('/api/universities'),
            fetchWithAuth('/api/directions'),
            fetchWithAuth('/get/skills')
        ]);

        const regions = await regionResponse.json();
        const universities = await universityResponse.json();
        const directions = await directionResponse.json();
        const skills = await skillsResponse.json();

        console.log('Regions:', regions);
        console.log('Universities:', universities);
        console.log('Directions:', directions);
        console.log('Skills:', skills);

        // Populate select elements
        populateSelect(regionSelect, regions);
        populateSelect(universitySelect, universities, 'id', 'name');
        populateSelect(directionSelect, directions, 'id', 'name');
        populateSelect(skillsSelect, skills, 'id', 'skill_name');

        // Initial load of candidates
        await loadCandidates();

    } catch (error) {
        console.error('Ошибка загрузки данных для фильтров:', error);
    }

    // Populate select helper function
    function populateSelect(selectElement, data, valueKey = '', textKey = '') {
        data.forEach(item => {
            const option = document.createElement('option');
            option.value = valueKey ? item[valueKey] : item;
            option.textContent = textKey ? item[textKey] : item;
            selectElement.appendChild(option);
        });
    }

    // Load candidates function
    async function loadCandidates() {
        try {
            const response = await fetchWithAuth('/api/candidates');
            allCandidates = await response.json();
            renderCandidates(allCandidates);
        } catch (error) {
            console.error('Ошибка загрузки данных кандидатов:', error);
            candidatesContainer.innerHTML = '<p>Ошибка загрузки данных кандидатов</p>';
        }
    }

    // Apply filters when the 'Показать' button is clicked
    showButton.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent form submission

        const selectedRegion = regionSelect.value.toLowerCase();
        const selectedDirection = directionSelect.value.toLowerCase();
        const selectedSkill = skillsSelect.value.toLowerCase();
        const selectedUniversity = universitySelect.value.toLowerCase();

        const filteredCandidates = allCandidates.filter(candidate => {
            const candidateRegion = candidate.address?.toLowerCase() || '';
            const candidateEducation = candidate.resumes[0]?.educations[0] || {};
            const candidateUniversity = candidateEducation.university_name?.toLowerCase() || '';
            const candidateDirection = candidateEducation.direction_name?.toLowerCase() || '';
            const candidateSkills = (candidate.resumes[0]?.skills || []).map(skill => skill.skill_name.toLowerCase());

            const matchesRegion = selectedRegion ? candidateRegion.includes(selectedRegion) : true;
            const matchesUniversity = selectedUniversity ? candidateUniversity.includes(selectedUniversity) : true;
            const matchesDirection = selectedDirection ? candidateDirection.includes(selectedDirection) : true;
            const matchesSkill = selectedSkill ? candidateSkills.includes(selectedSkill) : true;

            return matchesRegion && matchesUniversity && matchesDirection && matchesSkill && matchesAge;
        });

        renderCandidates(filteredCandidates);
    });

    // Render function for candidates
    function renderCandidates(candidates) {
        candidatesContainer.innerHTML = '';

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
                    <img src="${candidate.profile_photo || '/assets/images/default_avatar.jpg'}" alt="Фото кандидата">
                </div>
            `;

            candidatesContainer.appendChild(candidateElement);
        });
    }

    function calculateAge(birthDate) {
        if (!birthDate) return null;
        const birth = new Date(birthDate);
        const now = new Date();
        let age = now.getFullYear() - birth.getFullYear();
        const monthDiff = now.getMonth() - birth.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && now.getDate() < birth.getDate())) {
            age--;
        }
        return age;
    }
});
