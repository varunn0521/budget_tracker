document.addEventListener('DOMContentLoaded', function () {
    const addCategoryBtn = document.getElementById('add-category-btn');
    const categoryModal = new bootstrap.Modal(document.getElementById('addCategoryModal'));
    const addCategoryForm = document.getElementById('add-category-form');
    const categoryNameInput = document.getElementById('category-name');
    const categorySelect = document.getElementById('id_category');
    const submitButton = addCategoryForm.querySelector('button[type="submit"]');
    const incomeForm = document.querySelector('.income-form'); // Reference to the income form

    // Ensure CSRF token is correctly extracted
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // Open modal when the "Add Your Category" button is clicked
    addCategoryBtn.addEventListener('click', function () {
        categoryModal.show();
        categoryNameInput.value = ''; // Clear input when modal opens
    });

    // Handle category submission
    addCategoryForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent traditional form submission

        const categoryName = categoryNameInput.value.trim();

        // Validate the input
        if (categoryName === '') {
            alert('Category name cannot be empty.');
            return;
        }

        // Disable submit button and show loading feedback
        submitButton.disabled = true;
        submitButton.textContent = 'Adding...';

        // Send category data as JSON to the backend
        fetch(addCategoryUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ name: categoryName, type: 'income' })  // Explicitly set category type to income
        })
        .then(response => response.json()) // Get the response as JSON
        .then(data => {
            if (data.success) {
                // Add new category to the dropdown
                const newOption = document.createElement('option');
                newOption.value = data.id;  // Assuming the backend sends the category ID
                newOption.textContent = categoryName;
                categorySelect.appendChild(newOption);

                // Close modal and reset form
                categoryModal.hide();
                categoryNameInput.value = ''; // Clear the input field
            } else {
                alert('Failed to add category: ' + (data.message || 'Please try again.'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error adding the category. Please try again.');
        })
        .finally(() => {
            // Re-enable the submit button and reset its text
            submitButton.disabled = false;
            submitButton.textContent = 'Add Category';
        });
    });

    // Handle income form submission via traditional form submission
    incomeForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent traditional form submission

        const amount = document.getElementById('id_amount').value;
        const category = document.getElementById('id_category').value;
        const description = document.getElementById('id_description').value;

        // Validate inputs (ensure amount is a valid number)
        if (amount.trim() === '' || isNaN(amount) || Number(amount) <= 0) {
            alert('Please enter a valid amount.');
            return;
        }

        // Disable submit button to prevent multiple submissions
        const incomeSubmitButton = incomeForm.querySelector('button[type="submit"]');
        incomeSubmitButton.disabled = true;
        incomeSubmitButton.textContent = 'Submitting...';

        // Prepare FormData for form submission
        const formData = new FormData();
        formData.append('amount', amount);
        formData.append('category', category);
        formData.append('description', description);
        formData.append('csrfmiddlewaretoken', csrfToken);  // Include CSRF token

        // Use fetch with FormData to submit the income data
        fetch(addIncomeUrl, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json()) // Get the response as JSON
        .then(data => {
            if (data.success) {
                alert('Income added successfully!');
                window.location.href = dashboardUrl;  // Redirect to dashboard after success
            } else {
                alert('Failed to add income: ' + (data.message || 'Please try again.'));
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error adding the income. Please try again.');
        })
        .finally(() => {
            // Re-enable the submit button and reset its text
            incomeSubmitButton.disabled = false;
            incomeSubmitButton.textContent = 'Add Income';
        });
    });
});
