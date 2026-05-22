from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))
DB_PATH = os.path.join(BASE_DIR, 'krusty_krab.db')
BOOKING_INPUT_FORMAT = '%Y-%m-%d %H:%M'


app = Flask(__name__, static_folder=PROJECT_DIR, static_url_path='')
CORS(app)


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
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
            """
        )


def booking_row_to_dict(row):
    return {
        'id': row['id'],
        'name': row['name'],
        'email': row['email'],
        'checkin_datetime': row['checkin_datetime'],
        'checkout_datetime': row['checkout_datetime'],
        'people': row['people'],
        'message': row['message'],
        'created_at': row['created_at'],
    }


def parse_booking_datetime(value):
    return datetime.strptime(value, BOOKING_INPUT_FORMAT)


def fetch_bookings():
    with get_db() as conn:
        rows = conn.execute(
            """
            SELECT id, name, email, checkin_datetime, checkout_datetime, people, message, created_at
            FROM bookings
            ORDER BY checkin_datetime DESC, created_at DESC
            """
        ).fetchall()
    return [booking_row_to_dict(row) for row in rows]


def calculate_summary(bookings):
    now = datetime.now()
    today = now.date()

    total_bookings = len(bookings)
    today_bookings = 0
    upcoming_bookings = 0
    total_guests = 0

    for booking in bookings:
        total_guests += int(booking['people'])

        try:
            checkin_time = parse_booking_datetime(booking['checkin_datetime'])
        except ValueError:
            continue

        if checkin_time.date() == today:
            today_bookings += 1

        if checkin_time > now:
            upcoming_bookings += 1

    latest_booking = bookings[0] if bookings else None

    return {
        'total_bookings': total_bookings,
        'today_bookings': today_bookings,
        'upcoming_bookings': upcoming_bookings,
        'total_guests': total_guests,
        'latest_booking': latest_booking,
    }


init_db()


@app.route('/')
def index():
    return send_from_directory(PROJECT_DIR, 'booking.html')


@app.route('/admin')
@app.route('/admin.html')
def admin_dashboard():
    return send_from_directory(PROJECT_DIR, 'admin.html')


@app.route('/api/bookings', methods=['POST'])
def create_booking():
    try:
        data = request.get_json(silent=True) or {}

        name = str(data.get('name', '')).strip()
        email = str(data.get('email', '')).strip()
        checkin_datetime = str(data.get('checkin_datetime', '')).strip()
        checkout_datetime = str(data.get('checkout_datetime', '')).strip()
        people = data.get('people', 1)
        message = str(data.get('message', '')).strip()

        if not all([name, email, checkin_datetime, checkout_datetime]):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        try:
            checkin_time = parse_booking_datetime(checkin_datetime)
            checkout_time = parse_booking_datetime(checkout_datetime)
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid date format'}), 400

        if checkout_time <= checkin_time:
            return jsonify({'success': False, 'error': 'Check-out time must be after check-in time'}), 400

        try:
            people_count = int(people)
        except (TypeError, ValueError):
            return jsonify({'success': False, 'error': 'People must be a valid number'}), 400

        if people_count < 1:
            return jsonify({'success': False, 'error': 'People must be at least 1'}), 400

        with get_db() as conn:
            conn.execute(
                """
                INSERT INTO bookings (name, email, checkin_datetime, checkout_datetime, people, message)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, email, checkin_datetime, checkout_datetime, people_count, message),
            )

        return jsonify({
            'success': True,
            'message': 'Booking confirmed! We will contact you shortly.'
        }), 201

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    try:
        bookings = fetch_bookings()
        return jsonify({
            'success': True,
            'bookings': bookings
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/admin/summary', methods=['GET'])
def admin_summary():
    try:
        bookings = fetch_bookings()
        summary = calculate_summary(bookings)

        return jsonify({
            'success': True,
            'summary': summary,
            'recent_bookings': bookings[:5]
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200


if __name__ == '__main__':
    print('✓ Database initialized')
    app.run(debug=True, port=5000)
