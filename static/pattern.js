//document.querySelectorAll(".cv__generation__preview__item__open").forEach((button, index) => {
//    button.addEventListener("click", function(event) {
//        event.preventDefault();
//        const userId = localStorage.getItem("user_id");
//        const login = localStorage.getItem("login"); // Fetch login from localStorage
//        const password = localStorage.getItem("password"); // Fetch password from localStorage
//
//        if (!userId || !login || !password) {
//            console.error("Необходимые данные (ID пользователя, логин или пароль) не найдены в localStorage.");
//            alert("Необходимые данные отсутствуют.");
//            return;
//        }
//
//        // Determine the API URL based on the template number
//        const templateNumber = index + 1; // Assuming templates are 1-indexed
//        if (templateNumber) {
//            window.open(`/pattern${templateNumber}/${userId}?login=${encodeURIComponent(login)}&password=${encodeURIComponent(password)}`, '_blank');
//        } else {
//            alert("Не указан шаблон резюме.");
//        }
//    });
//
//});
//document.querySelectorAll(".cv__generation__preview__item").forEach((item, index) => {
//    item.addEventListener("click", function() {
//        document.querySelectorAll(".cv__generation__preview__item").forEach(el => el.classList.remove('active'));
//        item.classList.add('active');
//        // You can add code here to store the selected template ID in localStorage if needed
//        localStorage.setItem("id_resume", index + 1);
//    });
//});
//document.querySelector(".cv__generation__create").addEventListener("click", function(event) {
//    event.preventDefault();
//    const userId = localStorage.getItem("user_id");
//    const resumePatternId = localStorage.getItem("id_resume"); // Retrieve selected template ID
//
//    if (!userId || !resumePatternId) {
//        console.error("User ID or template ID not specified.");
//        alert("Resume template or user ID not specified.");
//        return;
//    }
//
//    const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
//    const createApiUrl = `${proxyUrl}http://46.229.215.18:5000/pattern_image_pdf/${userId}/${resumePatternId}`;
//
//    fetch(createApiUrl, {
//        method: 'GET',
//        mode: 'cors', // Ensure CORS mode is set
//        headers: {
//            'Content-Type': 'application/json'
//        }
//    })
//    .then(response => {
//        if (!response.ok) {
//            throw new Error(`HTTP error: ${response.status}`);
//        }
//        return response.blob(); // Receive PDF as blob
//    })
//    .then(blob => {
//        const url = window.URL.createObjectURL(blob);
//        window.open(url, '_blank'); // Open PDF in new tab
//    })
//    .catch(error => {
//        console.error("Error creating resume:", error);
//        alert(`Error creating resume: ${error.message}`);
//    });
//});
