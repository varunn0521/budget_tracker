document.addEventListener("DOMContentLoaded", function () {
    const passwordField = document.getElementById("id_password1");
    const passwordConfirmField = document.getElementById("id_password2");
    const passwordErrorDiv = document.createElement("div");
    const passwordRegex = /[A-Z]/;  // Uppercase letter
    const symbolRegex = /[\W_]/;   // Special character (symbol)
    const minLength = 8;

    // Password Validation Feedback
    function validatePassword() {
        const password = passwordField.value;
        let errors = [];

        if (!passwordRegex.test(password)) {
            errors.push("Password must contain at least one uppercase letter.");
        }
        if (password.length < minLength) {
            errors.push("Password must be at least 8 characters long.");
        }
        if (!symbolRegex.test(password)) {
            errors.push("Password must contain at least one symbol (e.g., !, @, #, $).");
        }

        // Display errors or clear previous messages
        passwordErrorDiv.innerHTML = "";
        if (errors.length > 0) {
            errors.forEach(error => {
                const errorElement = document.createElement("p");
                errorElement.textContent = error;
                passwordErrorDiv.appendChild(errorElement);
            });
            passwordField.classList.add("is-invalid");
        } else {
            passwordField.classList.remove("is-invalid");
        }

        // Append the error messages under the password field
        if (passwordField.parentElement.querySelector('.invalid-feedback') === null) {
            passwordField.parentElement.appendChild(passwordErrorDiv);
        }
    }

    // Trigger password validation when typing
    passwordField.addEventListener("input", validatePassword);

    // Confirm password validation
    passwordConfirmField.addEventListener("input", function () {
        if (passwordField.value !== passwordConfirmField.value) {
            passwordConfirmField.setCustomValidity("Passwords do not match.");
            passwordConfirmField.classList.add("is-invalid");
        } else {
            passwordConfirmField.setCustomValidity("");
            passwordConfirmField.classList.remove("is-invalid");
        }
    });

    // Password conditions icon (optional, for showing additional conditions next to the password field)
    const passwordConditionsIcon = document.querySelector('.password-rules i');
    const passwordRules = document.getElementById("password-rules");
    
    // Toggle the visibility of password rules when clicking the question mark icon
    passwordConditionsIcon.addEventListener("click", function () {
        passwordRules.classList.toggle("visible");
    });
});
