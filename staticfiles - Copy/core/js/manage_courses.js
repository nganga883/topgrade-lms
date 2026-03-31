document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("courseSearch");
    const table = document.getElementById("coursesTable");
    const form = document.getElementById("courseForm");

    if (searchInput && table) {
        searchInput.addEventListener("keyup", function () {
            const filter = searchInput.value.toLowerCase();
            const rows = table.querySelectorAll("tbody tr");

            rows.forEach((row) => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(filter) ? "" : "none";
            });
        });
    }

    if (form) {
        form.addEventListener("submit", function (event) {
            const name = document.getElementById("name").value.trim();
            const code = document.getElementById("code").value.trim();
            const lecturer = document.getElementById("lecturer").value.trim();

            if (!name || !code || !lecturer) {
                event.preventDefault();
                alert("Please fill in Course Name, Course Code, and Assign Lecturer.");
            }
        });
    }
});