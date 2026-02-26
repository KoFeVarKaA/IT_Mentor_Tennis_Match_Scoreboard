// JavaScript for toggling the dropdown menu
document.addEventListener("DOMContentLoaded", function () {
    const navToggle = document.querySelector(".nav-toggle");
    const navLinks = document.querySelector(".nav-links");

    navToggle.addEventListener("click", function () {
        navLinks.classList.toggle("active");
    });
});


document.addEventListener("DOMContentLoaded", function() {
    const inputFilter = document.getElementById("playerNameFilter");
    const searchButton = document.getElementById("searchButton");

    searchButton.addEventListener("click", function() {
        const playerName = inputFilter.value.trim();
        if (playerName) {
            window.location.href = `/matches?page=1&filter_by_name=${encodeURIComponent(playerName)}`;
        }
    });
    
   inputFilter.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            const playerName = inputFilter.value.trim();
            if (playerName) {
                window.location.href = `/matches?page=1&filter_by_name=${encodeURIComponent(playerName)}`;
            }
        }
    })
});