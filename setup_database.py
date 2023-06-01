import mysql.connector

# Mengatur koneksi ke database MySQL
db = mysql.connector.connect(
    host="localhost",
    user="imam",
    password="12345"
)

# Membuat database jika belum ada


def create_database():
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS uas_km")
    print("Database created successfully!")

# Membuat tabel untuk menyimpan pengetahuan eksplisit


def create_table():
    cursor = db.cursor()
    cursor.execute("USE uas_km")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS extracted_knowledge (id INT AUTO_INCREMENT PRIMARY KEY, category VARCHAR(255), sentence TEXT, accuracy FLOAT)")
    print("Table created successfully!")

# Menutup koneksi database


def close_connection():
    db.close()


# Menjalankan fungsi setup
if __name__ == "__main__":
    create_database()
    create_table()
    close_connection()
