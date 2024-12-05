document.addEventListener("DOMContentLoaded", async () => {
    const skillsDropdown = document.getElementById("skills");
    const selectedSkillsContainer = document.getElementById("selected-skills");
    const resumeId = localStorage.getItem("id_resume");

    // Проверяем, указан ли ID резюме
    if (!resumeId) {
        console.error("Ошибка: ID резюме отсутствует в localStorage.");
        return;
    }

    // Функция для получения навыков резюме
    async function fetchResumeSkills() {
        try {
            const response = await fetch(`/api/resume/${resumeId}/skills`);
            if (!response.ok) {
                const errorData = await response.json();
                console.error("Ошибка получения навыков:", errorData.error);
                return [];
            }

            const data = await response.json();
            return data.skills || []; // Возвращаем массив навыков
        } catch (error) {
            console.error("Ошибка запроса навыков:", error);
            return [];
        }
    }

    // Функция для получения доступных навыков
    async function fetchSkills() {
        try {
            const response = await fetch("/api/skills");
            if (!response.ok) throw new Error("Не удалось загрузить навыки.");
            const skills = await response.json();

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

    async function addSkill(skillId, skillName) {
    try {
        const response = await fetch("/api/resume_skills", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_resume: resumeId, id_skill: skillId }),
        });

        // Проверяем, возвращает ли сервер JSON
        const contentType = response.headers.get("Content-Type");
        if (!contentType || !contentType.includes("application/json")) {
            throw new Error("Сервер вернул неверный формат данных.");
        }

        const data = await response.json(); // Обработка JSON-ответа

        if (!response.ok) {
            throw new Error(data.error || "Ошибка при добавлении навыка.");
        }

        // Добавляем блок навыка в интерфейс
        const skillBlock = createSkillBlock(skillId, skillName);
        selectedSkillsContainer.appendChild(skillBlock);
        alert("Навык успешно добавлен.");
    } catch (error) {
        console.error("Ошибка добавления навыка:", error);
        alert(error.message);
    }
}


    // Функция для удаления навыка
    async function deleteSkill(idResumeSkill, skillBlock) {
        try {
            const response = await fetch(`/api/skills/${idResumeSkill}`, {
                method: "DELETE",
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || "Ошибка при удалении навыка.");
            }

            skillBlock.remove(); // Удаляем блок из интерфейса
            alert("Навык успешно удален.");
        } catch (error) {
            console.error("Ошибка удаления навыка:", error);
            alert(error.message);
        }
    }

    // Создание блока навыка с кнопкой удаления
    function createSkillBlock(idResumeSkill, skillName) {
        const skillBlock = document.createElement("div");
        skillBlock.classList.add("skill-block");
        skillBlock.innerHTML = `
            <span>${skillName}</span>
            <button type="button" aria-label="Удалить навык">✖</button>
        `;

        // Удаление навыка при клике
        skillBlock.querySelector("button").addEventListener("click", () => {
            deleteSkill(idResumeSkill, skillBlock);
        });

        return skillBlock;
    }

    // Загрузка навыков в интерфейс
    async function loadResumeSkills() {
        const skills = await fetchResumeSkills();
        selectedSkillsContainer.innerHTML = ""; // Очистка текущего контейнера
        skills.forEach(skill => {
            const skillBlock = createSkillBlock(skill.id_resume_skill, skill.skill_name);
            selectedSkillsContainer.appendChild(skillBlock);
        });
    }

    // Событие для добавления навыка из выпадающего списка
    skillsDropdown.addEventListener("change", async () => {
        const selectedOption = skillsDropdown.options[skillsDropdown.selectedIndex];
        const skillId = selectedOption.value;
        const skillName = selectedOption.text;

        // Проверка, чтобы навык не был добавлен дважды
        if (document.querySelector(`[data-skill-id="${skillId}"]`)) {
            alert("Этот навык уже добавлен.");
            return;
        }

        await addSkill(skillId, skillName);
    });

    // Инициализация: загрузка навыков
    await fetchSkills();
    await loadResumeSkills();
});

