# Krusty Krab Backend - Flask + SQLite

## Setup Complete! ✓

No configuration needed—everything is ready to go.

## Run the Server

```bash
cd backend
python3 app.py
```

Server will start at `http://localhost:5000`

The database file `krusty_krab.db` is created automatically on first run.

## API Endpoints

### Create Booking
**POST** `/api/bookings`

```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "datetime": "2024-05-25 19:00",
    "people": 4,
    "message": "Window seat please"
  }'
```

Response:
```json
{
  "success": true,
  "message": "Booking confirmed! We will contact you shortly."
}
```

### Get All Bookings
**GET** `/api/bookings`

```bash
curl http://localhost:5000/api/bookings
```

### Health Check
**GET** `/api/health`

## Database

SQLite database: `backend/krusty_krab.db`

Table schema:
```sql
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    datetime TEXT NOT NULL,
    people INTEGER NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Frontend Integration

The booking form in `booking.html` is already configured to send data to the backend.

Just run the Flask server and submit bookings from the form!
