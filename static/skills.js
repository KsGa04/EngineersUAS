document.addEventListener("DOMContentLoaded", async () => {
    const skillsSelect = document.getElementById("skills");

    // Load skills from the API
    async function loadSkills() {
        try {
            const response = await fetch("/api/skills");
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            const skills = await response.json();
            skills.forEach(skill => {
                const option = document.createElement("option");
                option.value = skill.id;
                option.textContent = skill.name;
                skillsSelect.appendChild(option);
            });
        } catch (error) {
            console.error("Ошибка загрузки навыков:", error);
        }
    }

    // Get selected skills
    function getSelectedSkills() {
        return Array.from(skillsSelect.selectedOptions).map(option => option.value);
    }

    // Save project with selected skills
    async function saveProjectWithSkills() {
        const projectName = document.querySelector("[name='cv__projects']").value;
        const selectedSkills = getSelectedSkills();
        const idResume = localStorage.getItem("id_resume");

        if (!projectName || !idResume) {
            alert("Пожалуйста, заполните все поля.");
            return;
        }

        try {
            const response = await fetch(`/api/project/${idResume}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    project_name: projectName,
                    project_description: "Описание проекта",
                    project_link: "http://example.com",
                    skills: selectedSkills
                })
            });

            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);

            const result = await response.json();
            alert(result.msg || "Проект успешно сохранен!");
        } catch (error) {
            console.error("Ошибка сохранения проекта:", error);
        }
    }

    // Initialize skills select
    await loadSkills();

    // Attach save handler to button
    const saveButton = document.getElementById("saveProjectButton");
    if (saveButton) {
        saveButton.addEventListener("click", saveProjectWithSkills);
    }
});
