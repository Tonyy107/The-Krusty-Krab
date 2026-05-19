from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', '')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'krusty_krab')

mysql = MySQL(app)

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.json

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        datetime_str = data.get('datetime', '').strip()
        people = data.get('people', 1)
        message = data.get('message', '').strip()

        if not all([name, email, datetime_str]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO bookings (name, email, datetime, people, message, created_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """, (name, email, datetime_str, people, message))

        mysql.connection.commit()
        cursor.close()

        return jsonify({
            'success': True,
            'message': 'Booking confirmed! We will contact you shortly.'
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, email, datetime, people, message, created_at FROM bookings ORDER BY created_at DESC")
        bookings = cursor.fetchall()
        cursor.close()

        return jsonify({
            'success': True,
            'bookings': [
                {
                    'id': b[0],
                    'name': b[1],
                    'email': b[2],
                    'datetime': b[3],
                    'people': b[4],
                    'message': b[5],
                    'created_at': str(b[6])
                }
                for b in bookings
            ]
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
