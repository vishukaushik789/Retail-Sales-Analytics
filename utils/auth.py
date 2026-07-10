import sqlite3
import bcrypt

DB_PATH = "database/sales.db"

def create_admin():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    username = "admin"
    password = "admin123"

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )

    cursor.execute(
        """
        INSERT OR IGNORE INTO users
        (username,password,role)
        VALUES(?,?,?)
        """,
        (username, hashed_password, "Admin")
    )

    conn.commit()
    conn.close()

    print("Admin account created!")

if __name__ == "__main__":
    create_admin()