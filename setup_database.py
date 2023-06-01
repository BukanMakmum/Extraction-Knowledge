import mysql.connector

def create_table():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="imam",
            password="12345",
            database="project_uas"
        )
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS extracted_knowledge (category VARCHAR(255), sentence TEXT, accuracy FLOAT)''')
        conn.commit()
        conn.close()
        print("Table created successfully!")
    except mysql.connector.Error as error:
        print("Error creating table:", error)
