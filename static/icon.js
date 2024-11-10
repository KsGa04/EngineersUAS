document.addEventListener("DOMContentLoaded", function() {
    const personIcon = document.getElementById("personIcon");
    const personMenu = document.getElementById("personMenu");

    personIcon.addEventListener("click", function() {
        if (personMenu.style.display === "block") {
            personMenu.style.display = "none";
        } else {
            personMenu.style.display = "block";
        }
    });

    // Close the menu when clicking outside
    document.addEventListener("click", function(event) {
        if (!personIcon.contains(event.target) && !personMenu.contains(event.target)) {
            personMenu.style.display = "none";
        }
    });
});
