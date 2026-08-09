import sqlite3
import random
from datetime import datetime, timedelta

DB_PATH = "data/finance.db"

# Expense categories
categories = {
    "Food": (100, 800),
    "Transport": (50, 500),
    "Shopping": (200, 2500),
    "Entertainment": (100, 1200),
    "Education": (200, 2000),
    "Bills": (300, 3000),
    "Healthcare": (100, 1500)
}

payment_methods = ["UPI", "Card", "Cash", "Bank"]


def generate_demo_data():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Start 90 days before the existing dataset
    start_date = datetime(2026, 5, 3)

    records = []

    for day in range(90):
        current_date = start_date + timedelta(days=day)

        # 1-3 expenses per day
        number_of_expenses = random.randint(1, 3)

        for _ in range(number_of_expenses):
            category = random.choice(list(categories.keys()))

            min_amount, max_amount = categories[category]

            amount = round(
                random.uniform(min_amount, max_amount),
                2
            )

            description = f"{category} expense"

            payment_method = random.choice(payment_methods)

            records.append(
                (
                    current_date.strftime("%Y-%m-%d"),
                    "Expense",
                    category,
                    description,
                    amount,
                    payment_method
                )
            )

    # Insert demo transactions
    cursor.executemany(
        """
        INSERT INTO transactions
        (date, type, category, description, amount, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        records
    )

    connection.commit()
    connection.close()

    print(f"Successfully added {len(records)} demo transactions.")
    print("These records are synthetic data for ML development.")


if __name__ == "__main__":
    generate_demo_data()