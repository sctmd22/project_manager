document.addEventListener("DOMContentLoaded", () => {
  const nameInput = document.getElementById("cylConFlowActual");
  const emailInput = document.getElementById("cylConFlowMin");
  const passwordInput = document.getElementById("cylConFlowMax");

  const nameError = document.getElementById("nameError");
  const emailError = document.getElementById("emailError");
  const passwordError = document.getElementById("passwordError");

  // Name validation: Ensure it is not empty and has at least 3 characters
  nameInput.addEventListener("input", () => {
    if (nameInput.value.trim().length < 3) {
      nameError.textContent = "Name must be at least 3 characters long.";
    } else {
      nameError.textContent = "";
    }
  });

  // Email validation: Basic email pattern check
  emailInput.addEventListener("input", () => {
    const emailPattern = /^[^ ]+@[^ ]+\.[a-z]{2,6}$/i;
    if (!emailPattern.test(emailInput.value)) {
      emailError.textContent = "Please enter a valid email address.";
    } else {
      emailError.textContent = "";
    }
  });

  // Password validation: Minimum 6 characters, at least one number
  passwordInput.addEventListener("input", () => {
    const passwordPattern = /^(?=.*\d).{6,}$/;
    if (!passwordPattern.test(passwordInput.value)) {
      passwordError.textContent =
        "Password must be at least 6 characters and contain at least one number.";
    } else {
      passwordError.textContent = "";
    }
  });
});
