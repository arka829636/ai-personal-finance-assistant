import pandas as pd


def get_transaction_type():
    while True:
        transaction_type = input(
            "Enter type (Income/Expense): "
        ).strip().capitalize()

        if transaction_type in ["Income", "Expense"]:
            return transaction_type

        print("❌ Invalid type. Please enter Income or Expense.")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount > 0:
                return amount

            print("❌ Amount must be greater than 0.")

        except ValueError:
            print("❌ Invalid amount. Please enter a number.")


def get_date():
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()

        try:
            pd.to_datetime(date)
            return date

        except ValueError:
            print("❌ Invalid date. Use YYYY-MM-DD.")


def get_non_empty_input(message):

    while True:

        value = input(message).strip()

        if value:
            return value

        print("❌ This field cannot be empty.")