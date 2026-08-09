import pandas as pd

from database import get_connection

from utils import (
    get_transaction_type,
    get_amount,
    get_date,
    get_non_empty_input
)


def add_transaction():

    print("\n===== ADD NEW TRANSACTION =====")

    date = get_date()

    transaction_type = get_transaction_type()

    category = get_non_empty_input(
        "Enter category: "
    )

    category = category.title()

    description = get_non_empty_input(
        "Enter description: "
    )

    amount = get_amount()

    payment_method = get_non_empty_input(
        "Enter payment method: "
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO transactions
        (date, type, category, description, amount, payment_method)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        date,
        transaction_type,
        category,
        description,
        amount,
        payment_method
    ))

    connection.commit()

    connection.close()

    print("\n✅ Transaction added successfully!")


def show_transactions():

    connection = get_connection()

    query = """
        SELECT
            date,
            type,
            category,
            description,
            amount,
            payment_method
        FROM transactions
        ORDER BY date
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    print("\n===== ALL TRANSACTIONS =====")

    if df.empty:

        print("No transactions found.")

    else:

        print(
            df.to_string(index=False)
        )