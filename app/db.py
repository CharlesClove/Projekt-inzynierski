import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'products.db')

def get_connection():
    """Create a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            description TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

def get_items():
    """Retrieve all products from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM products ORDER BY id')
    rows = cursor.fetchall()
    
    conn.close()
    
    # Convert rows to list of dictionaries
    items = []
    for row in rows:
        items.append({
            'id': row['id'],
            'name': row['name'],
            'price': row['price'],
            'description': row['description']
        })
    
    return items

def add_item(name, price, description):
    """Add a new product to the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO products (name, price, description) VALUES (?, ?, ?)',
        (name, price, description)
    )
    
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    
    return item_id

def delete_item(item_id):
    """Delete a product from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM products WHERE id = ?', (item_id,))
    
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    
    return deleted

def update_item(item_id, name, price, description):
    """Update an existing product in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        'UPDATE products SET name = ?, price = ?, description = ? WHERE id = ?',
        (name, price, description, item_id)
    )
    
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    
    return updated