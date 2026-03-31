document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("userSearch");
    const table = document.getElementById("usersTable");

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

    const toggleForms = document.querySelectorAll(".action-form");
    toggleForms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            const button = form.querySelector("button");
            const actionText = button ? button.textContent.trim() : "update";

            const confirmed = confirm(`Are you sure you want to ${actionText.toLowerCase()} this user?`);
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });

    const resetForms = document.querySelectorAll(".reset-form");
    resetForms.forEach((form) => {
        form.addEventListener("submit", function (event) {
            const passwordInput = form.querySelector('input[name="new_password"]');
            if (!passwordInput.value.trim()) {
                event.preventDefault();
                alert("Please enter a new password.");
                return;
            }

            const confirmed = confirm("Are you sure you want to reset this user's password?");
            if (!confirmed) {
                event.preventDefault();
            }
        });
    });
});