# Krusty Krab Backend - Flask + MySQL

## Setup Instructions

### 1. Install MySQL
Make sure MySQL is installed and running on your machine.

### 2. Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure Environment
Copy `.env.example` to `.env` and update with your MySQL credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=krusty_krab
```

### 4. Create Database and Tables
```bash
python setup_db.py
```

You should see: `✓ Database and table created successfully!`

### 5. Run Flask Server
```bash
python app.py
```

Server will start at `http://localhost:5000`

## API Endpoints

### Create Booking
**POST** `/api/bookings`

Request:
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "datetime": "2024-05-25 19:00",
    "people": 4,
    "message": "Window seat please"
}
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

Response:
```json
{
    "success": true,
    "bookings": [
        {
            "id": 1,
            "name": "John Doe",
            "email": "john@example.com",
            "datetime": "2024-05-25 19:00:00",
            "people": 4,
            "message": "Window seat please",
            "created_at": "2024-05-19 10:30:45"
        }
    ]
}
```

### Health Check
**GET** `/api/health`

Response:
```json
{
    "status": "healthy"
}
```

## Database Schema

```sql
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    datetime DATETIME NOT NULL,
    people INT NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Frontend
The booking form in `booking.html` is already configured to send data to the backend. Just make sure the Flask server is running when you submit bookings.
