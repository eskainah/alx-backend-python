import mysql.connector
import csv
import uuid

def connect_db():
    return mysql.connector.connect(user='root', password='yourpassword', host='localhost')

def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

def connect_to_prodev():
    return mysql.connector.connect(user='root', password='yourpassword', host='localhost', database='ALX_prodev')

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL,
            INDEX (user_id)
        )
    """)
    connection.commit()
    print("Table user_data created successfully")
    cursor.close()

def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uid = row.get("user_id") or str(uuid.uuid4())
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (uid, row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()
