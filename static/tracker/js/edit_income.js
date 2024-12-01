document.addEventListener('DOMContentLoaded', function () {
    const addCategoryBtn = document.getElementById('add-category-btn');
    const categoryModal = new bootstrap.Modal(document.getElementById('addCategoryModal'));
    const addCategoryForm = document.getElementById('add-category-form');
    const categoryNameInput = document.getElementById('category-name');
    const categorySelect = document.getElementById('id_category');
    const incomeForm = document.querySelector('.income-form');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // URLs (Make sure they are correctly generated in your Django template)
    const addCategoryUrl = "{% url 'add_category' %}";
    const dashboardUrl = "{% url 'dashboard' %}";
    const editIncomeUrl = "{% url 'edit_income' income.id %}";  // Correct this URL if necessary

    // Open modal for adding a category
    addCategoryBtn.addEventListener('click', function () {
        categoryModal.show();
        categoryNameInput.value = ''; // Clear previous value
    });

    // Handle the category addition form submission
    addCategoryForm.addEventListener('submit', async function (event) {
        event.preventDefault();
        const categoryName = categoryNameInput.value.trim();

        if (categoryName === '') {
            alert('Category name cannot be empty.');
            return;
        }

        try {
            const response = await fetch(addCategoryUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ name: categoryName, type: 'income' })
            });

            const data = await response.json();
            if (data.success) {
                const newOption = document.createElement('option');
                newOption.value = data.id; // Ensure the 'id' is correct in the response
                newOption.textContent = categoryName;
                categorySelect.appendChild(newOption);
                categoryModal.hide();
            } else {
                alert('Failed to add category: ' + (data.message || 'Unknown error.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while adding the category.');
        }
    });

    // Handle the income update form submission
    incomeForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        // Get form data
        const incomeId = document.getElementById('id_income').value;
        const amount = document.getElementById('id_amount').value;
        const category = document.getElementById('id_category').value;
        const description = document.getElementById('id_description').value;

        // Validate amount input
        if (!amount || isNaN(amount) || Number(amount) <= 0) {
            alert('Please enter a valid amount.');
            return;
        }

        // Validate category input
        if (!category) {
            alert('Please select a category.');
            return;
        }

        const formData = new FormData();
        formData.append('amount', amount);
        formData.append('category', category);
        formData.append('description', description);
        formData.append('csrfmiddlewaretoken', csrfToken);

        try {
            const response = await fetch(editIncomeUrl, {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (data.success) {
                alert('Income updated successfully!');
                window.location.href = dashboardUrl;
            } else {
                alert('Failed to update income: ' + (data.message || 'Unknown error.'));
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while updating income.');
        }
    });
});
