from flask import Flask, render_template, jsonify
from db import init_db, get_db_connection

app = Flask(__name__)

@app.route('/')
def index():
    return "Sklep dziala!" # Uproszczenie na start

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)