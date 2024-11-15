async function fetchWithAuth(url, options = {}) {
    // Устанавливаем токен аутентификации в заголовок
    const token = localStorage.getItem("authToken");
    options.headers = {
        ...options.headers,
        "Authorization": `Bearer ${token}`
    };

    try {
        const response = await fetch(url, options);

        // Проверка статуса 401 - истекший токен
        if (response.status === 401) {
            alert("Необходимо заново авторизоваться");
            // Перенаправляем на страницу авторизации
            window.location.href = "/login.html";
        } else {
            return response;
        }
    } catch (error) {
        console.error("Ошибка запроса:", error);
    }
}