import sqlite3


DATABASE_PATH = "data/finance.db"


def get_connection():

    return sqlite3.connect(DATABASE_PATH)


def create_tables():

    connection = get_connection()

    cursor = connection.cursor()

    # Transactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            date TEXT NOT NULL,

            type TEXT NOT NULL,

            category TEXT NOT NULL,

            description TEXT,

            amount REAL NOT NULL,

            payment_method TEXT
        )
    """)

    # Budgets table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS budgets (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT UNIQUE NOT NULL,

            budget REAL NOT NULL
        )
    """)

    connection.commit()

    connection.close()


if __name__ == "__main__":

    create_tables()

    print("✅ Database ready!")