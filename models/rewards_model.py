import sqlite3
import os

class Rewards:
    @staticmethod
    def get_rewards(user_id):
        try:
            db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "database.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT points FROM rewards WHERE user_id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            
            points = result[0] if result else 0
            
            # Return rewards information
            return {
                "points": points,
                "available_discounts": [
                    {"name": "Local Grocery Store", "discount": "10% off"},
                    {"name": "Community Center", "discount": "Free entry"},
                    {"name": "Recycling Workshop", "discount": "50% off"}
                ]
            }
        except Exception as e:
            print(f"Error getting rewards: {e}")
            # Return mock data in case of error
            return {
                "points": 120,
                "available_discounts": [
                    {"name": "Local Grocery Store", "discount": "10% off"},
                    {"name": "Community Center", "discount": "Free entry"},
                    {"name": "Recycling Workshop", "discount": "50% off"}
                ]
            }