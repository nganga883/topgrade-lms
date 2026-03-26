document.addEventListener("DOMContentLoaded", function () {

    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    if (togglePassword) {
        togglePassword.addEventListener("click", function () {
            const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
            passwordInput.setAttribute("type", type);
        });
    }

    const form = document.getElementById("lecturerForm");

    if (form) {
        form.addEventListener("submit", function (e) {
            const username = form.querySelector('input[name="username"]').value.trim();
            const email = form.querySelector('input[name="email"]').value.trim();
            const password = form.querySelector('input[name="password"]').value.trim();

            if (!username || !email || !password) {
                e.preventDefault();
                alert("Please fill all required fields.");
                return;
            }

            if (password.length < 6) {
                e.preventDefault();
                alert("Password must be at least 6 characters.");
            }
        });
    }

});