from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

DB_PATH = 'krusty_krab.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            checkin_datetime TEXT NOT NULL,
            checkout_datetime TEXT NOT NULL,
            people INTEGER NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return send_from_directory('..', 'booking.html')

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.json
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        checkin_datetime = data.get('checkin_datetime', '').strip()
        checkout_datetime = data.get('checkout_datetime', '').strip()
        people = data.get('people', 1)
        message = data.get('message', '').strip()

        if not all([name, email, checkin_datetime, checkout_datetime]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bookings (name, email, checkin_datetime, checkout_datetime, people, message)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, email, checkin_datetime, checkout_datetime, people, message))
        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Booking confirmed! We will contact you shortly.'
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, checkin_datetime, checkout_datetime, people, message, created_at FROM bookings ORDER BY created_at DESC")
        bookings = cursor.fetchall()
        conn.close()

        return jsonify({
            'success': True,
            'bookings': [dict(b) for b in bookings]
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    init_db()
    print("✓ Database initialized")
    app.run(debug=True, port=5000)
