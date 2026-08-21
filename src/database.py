import sqlite3
import csv
import os


DATABASE_PATH = "data/finance.db"
TRANSACTIONS_CSV = "data/transactions.csv"
BUDGETS_CSV = "data/budgets.csv"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_tables():
    # Make sure data directory exists
    os.makedirs("data", exist_ok=True)

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


def load_demo_data():
    """
    Load CSV demo data into SQLite only when the tables are empty.
    This makes the project work correctly after a fresh clone.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # Load transactions
    # ---------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM transactions")
    transaction_count = cursor.fetchone()[0]

    if transaction_count == 0 and os.path.exists(TRANSACTIONS_CSV):

        with open(
            TRANSACTIONS_CSV,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            records = []

            for row in reader:
                records.append(
                    (
                        row["date"],
                        row["type"],
                        row["category"],
                        row["description"],
                        float(row["amount"]),
                        row["payment_method"]
                    )
                )

        if records:
            cursor.executemany(
                """
                INSERT INTO transactions
                (date, type, category, description, amount, payment_method)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                records
            )

    # ---------------------------------------------------------
    # Load budgets
    # ---------------------------------------------------------

    cursor.execute("SELECT COUNT(*) FROM budgets")
    budget_count = cursor.fetchone()[0]

    if budget_count == 0 and os.path.exists(BUDGETS_CSV):

        with open(
            BUDGETS_CSV,
            "r",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            records = []

            for row in reader:
                records.append(
                    (
                        row["category"],
                        float(row["budget"])
                    )
                )

        if records:
            cursor.executemany(
                """
                INSERT OR IGNORE INTO budgets
                (category, budget)
                VALUES (?, ?)
                """,
                records
            )

    connection.commit()
    connection.close()


def initialize_database():
    """
    Create database tables and load demo data if necessary.
    """

    create_tables()
    load_demo_data()


if __name__ == "__main__":

    initialize_database()

    print("✅ Database ready!")