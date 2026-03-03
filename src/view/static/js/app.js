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

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.score-btn').forEach(button => {
        button.addEventListener('click', function() {
            const uuid = this.getAttribute('data-uuid');
            const player = this.getAttribute('data-player');

            fetch(`/match-score?uuid=${uuid}&add_point=${player}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                }
            }) 
            .then(response => response.text())
            .then(html => {
                document.open();
                document.write(html);
                document.close();
            })           
        });
    });
});