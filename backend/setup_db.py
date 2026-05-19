import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', 'krusty_krab')

try:
    # Connect to MySQL (without database first)
    conn = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        charset='utf8mb4'
    )

    cursor = conn.cursor()

    # Create database
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    print(f"✓ Database '{DB_NAME}' ready")

    # Use the database
    cursor.execute(f"USE {DB_NAME}")

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            datetime DATETIME NOT NULL,
            people INT NOT NULL,
            message TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print(f"✓ Table 'bookings' ready")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n✓ MySQL Setup Complete!")
    print(f"  Host: {DB_HOST}")
    print(f"  User: {DB_USER}")
    print(f"  Database: {DB_NAME}")

except Exception as e:
    print(f"✗ Error: {e}")
    print("\nMake sure MySQL is running and credentials are correct in .env")
