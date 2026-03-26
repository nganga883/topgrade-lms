document.addEventListener("DOMContentLoaded", function () {

    // Toggle password
    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("password");

    if (togglePassword) {
        togglePassword.addEventListener("click", function () {
            passwordInput.type =
                passwordInput.type === "password" ? "text" : "password";
        });
    }

    // Copy link
    const copyBtn = document.getElementById("copyBtn");
    const lecturerLink = document.getElementById("lecturerLink");

    if (copyBtn && lecturerLink) {
        copyBtn.addEventListener("click", function () {
            navigator.clipboard.writeText(lecturerLink.value);

            copyBtn.textContent = "Copied!";
            copyBtn.classList.add("copy-success");

            setTimeout(() => {
                copyBtn.textContent = "Copy";
                copyBtn.classList.remove("copy-success");
            }, 2000);
        });
    }

    // Validation
    const form = document.getElementById("lecturerForm");

    if (form) {
        form.addEventListener("submit", function (e) {
            const password = passwordInput.value;

            if (password.length < 6) {
                e.preventDefault();
                alert("Password must be at least 6 characters.");
            }
        });
    }

});