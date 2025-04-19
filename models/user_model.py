import sqlite3
import os

class User:
    @staticmethod
    def get_user(username):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "database.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            conn.close()
            if user:
                return {
                    "id": user[0], 
                    "username": user[1], 
                    "password": user[2], 
                    "status": user[3]
                }
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None

    @staticmethod
    def update_status(user_id, status):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "database.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET status = ? WHERE id = ?", (status, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating status: {e}")
            return False