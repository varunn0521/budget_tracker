document.addEventListener('DOMContentLoaded', function () {
    const editExpenseBaseUrl = "{% url 'edit_expense' expense_id=0 %}".replace('/0/', '/');
    const deleteExpenseBaseUrl = "{% url 'delete_expense' expense_id=0 %}".replace('/0/', '/');

    // Open the edit modal and load expense data
    function editExpense(expenseId) {
        const editUrl = `${editExpenseBaseUrl}${expenseId}/`;
        fetch(editUrl)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('edit-expense-id').value = expenseId;
                    document.getElementById('edit-expense-amount').value = data.expense.amount;
                    document.getElementById('edit-expense-category').value = data.expense.category.id;
                    document.getElementById('edit-expense-description').value = data.expense.description;

                    const myModal = new bootstrap.Modal(document.getElementById('editExpenseModal'));
                    myModal.show();
                } else {
                    alert('Failed to fetch expense details. Please try again.');
                }
            })
            .catch(error => {
                alert('Error fetching expense data: ' + error);
            });
    }

    // Submit edited expense data
    document.getElementById('edit-expense-form').addEventListener('submit', function (e) {
        e.preventDefault();

        const expenseId = document.getElementById('edit-expense-id').value;
        const amount = document.getElementById('edit-expense-amount').value;
        const category = document.getElementById('edit-expense-category').value;
        const description = document.getElementById('edit-expense-description').value;

        const data = {
            amount: amount,
            category: category,
            description: description,
        };

        // Send POST request to save the edited expense
        fetch(`${editExpenseBaseUrl}${expenseId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify(data),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Expense updated successfully');
                    location.reload();
                } else {
                    alert('Failed to update expense: ' + data.message);
                }
            })
            .catch(error => {
                alert('Error updating expense: ' + error);
            });
    });

    // Delete expense
    window.deleteExpense = function (expenseId) {
        if (confirm('Are you sure you want to delete this expense?')) {
            fetch(`${deleteExpenseBaseUrl}${expenseId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                body: JSON.stringify({ expense_id: expenseId }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Expense deleted successfully');
                        location.reload();
                    } else {
                        alert('Failed to delete expense: ' + data.message);
                    }
                })
                .catch(error => {
                    alert('Error deleting expense: ' + error);
                });
        }
    };
});
