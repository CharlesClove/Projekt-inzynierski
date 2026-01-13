import pytest
import json
import os
import sys

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app import app
from db import init_db, get_connection

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    # Use a test database
    app.config['TESTING'] = True
    
    # Create test client
    with app.test_client() as client:
        # Initialize the database
        with app.app_context():
            init_db()
            # Clear any existing test data
            conn = get_connection()
            conn.execute('DELETE FROM products')
            conn.commit()
            conn.close()
        yield client
        
        # Cleanup after tests
        with app.app_context():
            conn = get_connection()
            conn.execute('DELETE FROM products')
            conn.commit()
            conn.close()

class TestRoutes:
    """Test Flask route endpoints."""
    
    def test_index_redirect(self, client):
        """Test that / redirects to /client."""
        response = client.get('/', follow_redirects=False)
        assert response.status_code == 302
        assert '/client' in response.location
    
    def test_client_page(self, client):
        """Test that client page loads successfully."""
        response = client.get('/client')
        assert response.status_code == 200
        assert b'Nasze Produkty' in response.data
    
    def test_admin_page(self, client):
        """Test that admin page loads successfully."""
        response = client.get('/admin')
        assert response.status_code == 200
        assert b'Panel Administratora' in response.data

class TestAPIEndpoints:
    """Test API endpoints for CRUD operations."""
    
    def test_get_items_empty(self, client):
        """Test GET /items returns empty array initially."""
        response = client.get('/items')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) == 0
    
    def test_add_item(self, client):
        """Test POST /items creates a new product."""
        product_data = {
            'name': 'Test Laptop',
            'price': 2999.99,
            'description': 'Test description'
        }
        
        response = client.post(
            '/items',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['name'] == 'Test Laptop'
        assert data['price'] == 2999.99
        assert data['description'] == 'Test description'
        assert 'id' in data
    
    def test_add_item_missing_fields(self, client):
        """Test POST /items with missing required fields."""
        product_data = {
            'name': 'Test Product'
            # Missing 'price' field
        }
        
        response = client.post(
            '/items',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_items_with_data(self, client):
        """Test GET /items returns products after adding them."""
        # Add a product first
        product_data = {
            'name': 'Test Phone',
            'price': 1999.99,
            'description': 'Smartphone'
        }
        
        client.post(
            '/items',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        # Get all items
        response = client.get('/items')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['name'] == 'Test Phone'
        assert data[0]['price'] == 1999.99
    
    def test_update_item(self, client):
        """Test PUT /items updates an existing product."""
        # Add a product first
        product_data = {
            'name': 'Original Name',
            'price': 999.99,
            'description': 'Original description'
        }
        
        add_response = client.post(
            '/items',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        product_id = json.loads(add_response.data)['id']
        
        # Update the product
        update_data = {
            'id': product_id,
            'name': 'Updated Name',
            'price': 1299.99,
            'description': 'Updated description'
        }
        
        response = client.put(
            '/items',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Name'
        assert data['price'] == 1299.99
        assert data['description'] == 'Updated description'
    
    def test_update_nonexistent_item(self, client):
        """Test PUT /items with non-existent product ID."""
        update_data = {
            'id': 99999,
            'name': 'Test',
            'price': 100.00,
            'description': 'Test'
        }
        
        response = client.put(
            '/items',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_item(self, client):
        """Test DELETE /items removes a product."""
        # Add a product first
        product_data = {
            'name': 'To Be Deleted',
            'price': 599.99,
            'description': 'Will be deleted'
        }
        
        add_response = client.post(
            '/items',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        product_id = json.loads(add_response.data)['id']
        
        # Delete the product
        response = client.delete(f'/items?id={product_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verify it's deleted
        get_response = client.get('/items')
        items = json.loads(get_response.data)
        assert len(items) == 0
    
    def test_delete_nonexistent_item(self, client):
        """Test DELETE /items with non-existent product ID."""
        response = client.delete('/items?id=99999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_delete_missing_id(self, client):
        """Test DELETE /items without ID parameter."""
        response = client.delete('/items')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

class TestIntegration:
    """Integration tests for complete workflows."""
    
    def test_full_crud_workflow(self, client):
        """Test complete CRUD workflow."""
        # 1. Initially empty
        response = client.get('/items')
        assert len(json.loads(response.data)) == 0
        
        # 2. Add multiple products
        products = [
            {'name': 'Laptop', 'price': 3999.99, 'description': 'Gaming laptop'},
            {'name': 'Mouse', 'price': 99.99, 'description': 'Wireless mouse'},
            {'name': 'Keyboard', 'price': 199.99, 'description': 'Mechanical keyboard'}
        ]
        
        product_ids = []
        for product in products:
            response = client.post(
                '/items',
                data=json.dumps(product),
                content_type='application/json'
            )
            assert response.status_code == 201
            product_ids.append(json.loads(response.data)['id'])
        
        # 3. Verify all products exist
        response = client.get('/items')
        items = json.loads(response.data)
        assert len(items) == 3
        
        # 4. Update one product
        update_data = {
            'id': product_ids[0],
            'name': 'Gaming Laptop',
            'price': 4299.99,
            'description': 'High-end gaming laptop'
        }
        response = client.put(
            '/items',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        assert response.status_code == 200
        
        # 5. Delete one product
        response = client.delete(f'/items?id={product_ids[1]}')
        assert response.status_code == 200
        
        # 6. Verify final state
        response = client.get('/items')
        items = json.loads(response.data)
        assert len(items) == 2
        assert items[0]['name'] == 'Gaming Laptop'
        assert items[0]['price'] == 4299.99
