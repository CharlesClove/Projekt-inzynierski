// Global state
let editingProductId = null;

// Toast notification function
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Load and display products in the admin table
async function loadProducts() {
    const loading = document.getElementById('loading');
    const emptyState = document.getElementById('empty-state');
    const tableContainer = document.getElementById('products-table-container');
    const tbody = document.getElementById('products-tbody');

    try {
        const response = await fetch('/items');
        const products = await response.json();

        loading.style.display = 'none';

        if (products.length === 0) {
            emptyState.style.display = 'flex';
            tableContainer.style.display = 'none';
            return;
        }

        emptyState.style.display = 'none';
        tableContainer.style.display = 'block';

        tbody.innerHTML = products.map(product => `
            <tr data-id="${product.id}">
                <td>${product.id}</td>
                <td>
                    <span class="product-name-text">${escapeHtml(product.name)}</span>
                    <input type="text" class="editable product-name-edit" value="${escapeHtml(product.name)}" style="display: none;">
                </td>
                <td>
                    <span class="product-price-text">${product.price.toFixed(2)} PLN</span>
                    <input type="number" class="editable product-price-edit" value="${product.price}" step="0.01" style="display: none;">
                </td>
                <td>
                    <span class="product-desc-text">${escapeHtml(product.description || '-')}</span>
                    <textarea class="editable product-desc-edit" style="display: none; min-height: 60px;">${escapeHtml(product.description || '')}</textarea>
                </td>
                <td class="actions">
                    <button class="btn btn-success edit-btn" onclick="editProduct(${product.id})">
                        ✏️ Edytuj
                    </button>
                    <button class="btn btn-success save-btn" onclick="saveProduct(${product.id})" style="display: none;">
                        ✓ Zapisz
                    </button>
                    <button class="btn btn-danger delete-btn" onclick="deleteProduct(${product.id})">
                        🗑️ Usuń
                    </button>
                    <button class="btn btn-danger cancel-btn" onclick="cancelEdit(${product.id})" style="display: none;">
                        ✕ Anuluj
                    </button>
                </td>
            </tr>
        `).join('');

    } catch (error) {
        loading.style.display = 'none';
        showToast('Błąd podczas ładowania produktów', 'error');
        console.error('Error loading products:', error);
    }
}

// Add new product //
async function addProduct(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const productData = {
        name: formData.get('name'),
        price: parseFloat(formData.get('price')),
        description: formData.get('description') || ''
    };

    try {
        const response = await fetch('/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData)
        });

        const result = await response.json();

        if (response.ok) {
            showToast('Produkt dodany pomyślnie!', 'success');
            form.reset();
            loadProducts();
        } else {
            showToast(result.error || 'Błąd podczas dodawania produktu', 'error');
        }
    } catch (error) {
        showToast('Błąd podczas dodawania produktu', 'error');
        console.error('Error adding product:', error);
    }
}

// Enable edit mode for a product
function editProduct(productId) {
    if (editingProductId !== null) {
        cancelEdit(editingProductId);
    }

    editingProductId = productId;
    const row = document.querySelector(`tr[data-id="${productId}"]`);

    // Hide text, show inputs
    row.querySelectorAll('.product-name-text, .product-price-text, .product-desc-text').forEach(el => {
        el.style.display = 'none';
    });

    row.querySelectorAll('.product-name-edit, .product-price-edit, .product-desc-edit').forEach(el => {
        el.style.display = 'block';
    });

    // Switch buttons
    row.querySelector('.edit-btn').style.display = 'none';
    row.querySelector('.delete-btn').style.display = 'none';
    row.querySelector('.save-btn').style.display = 'inline-flex';
    row.querySelector('.cancel-btn').style.display = 'inline-flex';
}

// Cancel edit mode
function cancelEdit(productId) {
    const row = document.querySelector(`tr[data-id="${productId}"]`);

    // Show text, hide inputs
    row.querySelectorAll('.product-name-text, .product-price-text, .product-desc-text').forEach(el => {
        el.style.display = 'inline';
    });

    row.querySelectorAll('.product-name-edit, .product-price-edit, .product-desc-edit').forEach(el => {
        el.style.display = 'none';
    });

    // Switch buttons back
    row.querySelector('.edit-btn').style.display = 'inline-flex';
    row.querySelector('.delete-btn').style.display = 'inline-flex';
    row.querySelector('.save-btn').style.display = 'none';
    row.querySelector('.cancel-btn').style.display = 'none';

    editingProductId = null;
}

// Save edited product
async function saveProduct(productId) {
    const row = document.querySelector(`tr[data-id="${productId}"]`);

    const productData = {
        id: productId,
        name: row.querySelector('.product-name-edit').value,
        price: parseFloat(row.querySelector('.product-price-edit').value),
        description: row.querySelector('.product-desc-edit').value
    };

    try {
        const response = await fetch('/items', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(productData)
        });

        const result = await response.json();

        if (response.ok) {
            showToast('Produkt zaktualizowany pomyślnie!', 'success');
            editingProductId = null;
            loadProducts();
        } else {
            showToast(result.error || 'Błąd podczas aktualizacji produktu', 'error');
        }
    } catch (error) {
        showToast('Błąd podczas aktualizacji produktu', 'error');
        console.error('Error updating product:', error);
    }
}

// Delete product
async function deleteProduct(productId) {
    if (!confirm('Czy na pewno chcesz usunąć ten produkt?')) {
        return;
    }

    try {
        const response = await fetch(`/items?id=${productId}`, {
            method: 'DELETE'
        });

        const result = await response.json();

        if (response.ok) {
            showToast('Produkt usunięty pomyślnie!', 'success');
            loadProducts();
        } else {
            showToast(result.error || 'Błąd podczas usuwania produktu', 'error');
        }
    } catch (error) {
        showToast('Błąd podczas usuwania produktu', 'error');
        console.error('Error deleting product:', error);
    }
}

// Utility function to escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function () {
    // Load products if we're on the admin page
    if (document.getElementById('products-tbody')) {
        loadProducts();

        // Attach form submit handler
        const form = document.getElementById('add-product-form');
        if (form) {
            form.addEventListener('submit', addProduct);
        }
    }
});
