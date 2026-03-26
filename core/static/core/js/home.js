document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.getElementById("navLinks");
    const searchBtn = document.getElementById("searchBtn");
    const searchInput = document.getElementById("courseSearchInput");

    if (menuToggle && navLinks) {
        menuToggle.addEventListener("click", function () {
            navLinks.classList.toggle("show");
        });
    }

    if (searchBtn && searchInput) {
        searchBtn.addEventListener("click", function () {
            const value = searchInput.value.trim();
            if (!value) {
                alert("Please enter a course or material to search.");
                return;
            }
            alert("Search feature for: " + value + " will be connected to backend later.");
        });
    }
});