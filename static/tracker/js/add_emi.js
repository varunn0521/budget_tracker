document.addEventListener("DOMContentLoaded", function () {
  const emiForm = document.querySelector(".emi-form"); // Reference to the EMI form
  const frequencyField = document.getElementById("id_frequency");
  const installmentsField = document.getElementById("id_remaining_installments");

  // Function to handle frequency change and update the number of installments
  frequencyField.addEventListener("change", function () {
      const selectedFrequency = frequencyField.value;
      let remainingInstallments = 0;

      // Adjust installments based on selected frequency
      switch (selectedFrequency) {
          case "daily":
              remainingInstallments = 30; // Example: 30 days in a month
              break;
          case "weekly":
              remainingInstallments = 4; // Example: 4 weeks in a month
              break;
          case "bi-weekly":
              remainingInstallments = 2; // Example: 2 bi-weekly installments in a month
              break;
          case "monthly":
              remainingInstallments = 12; // Default: 12 installments in a year
              break;
          case "quarterly":
              remainingInstallments = 4; // Example: 4 quarterly installments in a year
              break;
          case "yearly":
              remainingInstallments = 1; // Example: 1 yearly installment
              break;
          default:
              remainingInstallments = 0; // Default value if no valid frequency is selected
      }

      // Update the number of installments field
      installmentsField.value = remainingInstallments;
  });

  // Optional: Trigger the change event on page load to pre-fill the installments field
  frequencyField.dispatchEvent(new Event("change"));

  // Handle EMI form submission
  emiForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent traditional form submission

      // Collect form data
      const formData = new FormData(emiForm);

      // Disable the submit button to prevent multiple submissions
      const emiSubmitButton = emiForm.querySelector("button[type='submit']");
      emiSubmitButton.disabled = true;
      emiSubmitButton.textContent = "Submitting...";

      // Send the EMI data using fetch
      fetch(emiForm.action, { // The URL will be taken from the form's 'action' attribute
          method: "POST",
          body: formData,
      })
          .then((response) => response.json())
          .then((data) => {
              if (data.success) {
                  alert(data.message || "EMI added successfully!");
                  window.location.href = data.redirect_url || "/"; // Redirect to dashboard or any URL from the response
              } else {
                  alert(data.message || "Failed to add EMI. Please try again.");
              }
          })
          .catch((error) => {
              console.error("Error:", error);
              alert("There was an error adding the EMI. Please try again.");
          })
          .finally(() => {
              emiSubmitButton.disabled = false;
              emiSubmitButton.textContent = "Add EMI";
          });
  });
});
