document.addEventListener('DOMContentLoaded', function () {
  const addCategoryBtn = document.getElementById('add-category-expense-btn');
  const categoryModal = new bootstrap.Modal(document.getElementById('addCategoryModal'));
  const addCategoryForm = document.getElementById('add-category-form');
  const categoryNameInput = document.getElementById('category-name');
  const categorySelect = document.getElementById('id_category_expense');
  const expenseForm = document.querySelector('.expense-form'); // Reference to the expense form

  // Ensure required elements are present
  if (!categorySelect) {
    console.error('Category select element not found');
    return;
  }

  // Function to show alerts (success or error)
  const showAlert = (message, type = 'success') => {
    const alertBox = document.createElement('div');
    alertBox.className = `alert alert-${type} alert-dismissible fade show`;
    alertBox.role = 'alert';
    alertBox.innerHTML = `
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.prepend(alertBox); // Add alert to the top of the page
    setTimeout(() => alertBox.remove(), 5000); // Auto-remove alert after 5 seconds
  };

  // Open modal when the "Add Your Category" button is clicked
  addCategoryBtn.addEventListener('click', function () {
    categoryModal.show();
  });

  // Handle adding a new category
  addCategoryForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent traditional form submission

    const categoryName = categoryNameInput.value.trim();

    // Validate the input
    if (!categoryName) {
      showAlert('Category name cannot be empty.', 'danger');
      return;
    }

    // AJAX request to add the new category
    fetch(addCategoryUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
      },
      body: JSON.stringify({
        name: categoryName,
        type: 'expense', // Explicitly set the category type as 'expense'
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          // Add the new category to the dropdown
          const newOption = document.createElement('option');
          newOption.value = data.category.id;
          newOption.textContent = data.category.name;
          categorySelect.appendChild(newOption);

          // Select the newly added category
          categorySelect.value = data.category.id;

          // Close the modal and reset the form
          categoryModal.hide();
          categoryNameInput.value = ''; // Clear the input field
          showAlert('Category added successfully!');
        } else {
          showAlert(data.message || 'Failed to add category. Please try again.', 'danger');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        showAlert('There was an error adding the category. Please try again.', 'danger');
      });
  });

  // Handle adding an expense
  expenseForm.addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent traditional form submission

    const amount = document.getElementById('id_amount').value.trim();
    const category = categorySelect.value;
    const description = document.getElementById('id_description').value.trim();

    // Validate inputs
    if (!amount || isNaN(amount) || Number(amount) <= 0) {
      showAlert('Please enter a valid amount.', 'danger');
      return;
    }

    // Disable the submit button to prevent multiple submissions
    const expenseSubmitButton = expenseForm.querySelector('button[type="submit"]');
    expenseSubmitButton.disabled = true;
    expenseSubmitButton.textContent = 'Submitting...';

    // Prepare FormData for submission
    const formData = new FormData(expenseForm);

    // Use fetch with FormData to submit the expense data
    fetch(addExpenseUrl, {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showAlert(data.message || 'Expense added successfully!');
          window.location.href = dashboardUrl; // Redirect to dashboard
        } else {
          showAlert(data.message || 'Failed to add expense. Please try again.', 'danger');
        }
      })
      .catch((error) => {
        console.error('Error:', error);
        showAlert('There was an error adding the expense. Please try again.', 'danger');
      })
      .finally(() => {
        // Re-enable the submit button and reset its text
        expenseSubmitButton.disabled = false;
        expenseSubmitButton.textContent = 'Add Expense';
      });
  });
});
