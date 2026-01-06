from flask import Flask, render_template, jsonify, request, redirect
from db import init_db, get_items, add_item, delete_item, update_item

app = Flask(__name__)

# Routes for pages
@app.route('/')
def index():
    """Redirect to client page."""
    return redirect('/client')

@app.route('/client')
def client():
    """Render client interface (read-only product list)."""
    return render_template('client.html')

@app.route('/admin')
def admin():
    """Render admin interface (CRUD operations)."""
    return render_template('admin.html')

# API endpoints
@app.route('/items', methods=['GET'])
def get_items_api():
    """Return all products in JSON format."""
    try:
        items = get_items()
        return jsonify(items), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items', methods=['POST'])
def add_item_api():
    """Add a new product."""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'price' not in data:
            return jsonify({'error': 'Missing required fields: name, price'}), 400
        
        name = data['name']
        price = float(data['price'])
        description = data.get('description', '')
        
        item_id = add_item(name, price, description)
        
        return jsonify({
            'id': item_id,
            'name': name,
            'price': price,
            'description': description,
            'message': 'Product added successfully'
        }), 201
    except ValueError:
        return jsonify({'error': 'Invalid price format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items', methods=['DELETE'])
def delete_item_api():
    """Delete a product by ID."""
    try:
        item_id = request.args.get('id')
        
        if not item_id:
            return jsonify({'error': 'Missing required parameter: id'}), 400
        
        deleted = delete_item(int(item_id))
        
        if deleted:
            return jsonify({'message': 'Product deleted successfully'}), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid ID format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/items', methods=['PUT'])
def update_item_api():
    """Update an existing product."""
    try:
        data = request.get_json()
        
        if not data or 'id' not in data:
            return jsonify({'error': 'Missing required field: id'}), 400
        
        item_id = int(data['id'])
        name = data.get('name', '')
        price = float(data.get('price', 0))
        description = data.get('description', '')
        
        updated = update_item(item_id, name, price, description)
        
        if updated:
            return jsonify({
                'id': item_id,
                'name': name,
                'price': price,
                'description': description,
                'message': 'Product updated successfully'
            }), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)