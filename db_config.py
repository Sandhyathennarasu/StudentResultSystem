import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sandhya@05",  # 🔹 replace with your actual MySQL password
        database="student_db"
    )
    return connection


# ✅ Add this test section at the END of the file
if __name__ == "__main__":
    conn = get_connection()
    if conn.is_connected():
        print("✅ Database connected successfully!")
        conn.close()
