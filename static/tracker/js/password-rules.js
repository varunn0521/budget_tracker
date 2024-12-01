document.addEventListener("DOMContentLoaded", () => {
    const passwordField = document.getElementById("id_password1");
    const confirmPasswordField = document.getElementById("id_password2");
    const matchFeedback = document.getElementById("password-match-feedback");

    passwordField.addEventListener("keyup", () => {
        const password = passwordField.value;
        const minLength = password.length >= 8;
        const hasUppercase = /[A-Z]/.test(password);
        const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

        document.getElementById("min-length-rule").classList.toggle("valid-rule", minLength);
        document.getElementById("min-length-rule").classList.toggle("invalid-rule", !minLength);

        document.getElementById("uppercase-rule").classList.toggle("valid-rule", hasUppercase);
        document.getElementById("uppercase-rule").classList.toggle("invalid-rule", !hasUppercase);

        document.getElementById("special-char-rule").classList.toggle("valid-rule", hasSpecialChar);
        document.getElementById("special-char-rule").classList.toggle("invalid-rule", !hasSpecialChar);
    });

    confirmPasswordField.addEventListener("keyup", () => {
        if (passwordField.value !== confirmPasswordField.value) {
            matchFeedback.style.display = "block";
        } else {
            matchFeedback.style.display = "none";
        }
    });
});
