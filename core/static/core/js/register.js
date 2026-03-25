// Front-end validation for registration
document.getElementById("registerForm").addEventListener("submit", function(event) {
    let email = document.getElementById("email").value;
    let confirmEmail = document.getElementById("confirm_email").value;
    let password = document.getElementById("password1").value;
    let confirmPassword = document.getElementById("password2").value;

    let message = "";

    if (email !== confirmEmail) {
        message = "Emails do not match!";
    } else if (password !== confirmPassword) {
        message = "Passwords do not match!";
    }

    if (message) {
        event.preventDefault();
        alert(message);
    }
});