import pandas as pd

from database import get_connection


def show_summary():

    connection = get_connection()

    query = """
        SELECT
            type,
            SUM(amount) AS total
        FROM transactions
        GROUP BY type
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    income = 0
    expenses = 0

    for _, row in df.iterrows():

        if row["type"] == "Income":
            income = row["total"]

        elif row["type"] == "Expense":
            expenses = row["total"]

    savings = income - expenses

    print("\n===== FINANCIAL SUMMARY =====")

    print(
        f"Total Income  : ₹{income:,.2f}"
    )

    print(
        f"Total Expense : ₹{expenses:,.2f}"
    )

    print(
        f"Savings       : ₹{savings:,.2f}"
    )


def monthly_analysis():

    connection = get_connection()

    query = """
        SELECT
            date,
            type,
            amount
        FROM transactions
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo transactions found.")

        return

    df["date"] = pd.to_datetime(
        df["date"]
    )

    latest_month = (
        df["date"]
        .dt.to_period("M")
        .max()
    )

    monthly_df = df[
        df["date"].dt.to_period("M")
        == latest_month
    ]

    income = monthly_df[
        monthly_df["type"] == "Income"
    ]["amount"].sum()

    expenses = monthly_df[
        monthly_df["type"] == "Expense"
    ]["amount"].sum()

    savings = income - expenses

    if income > 0:

        savings_rate = (
            savings / income
        ) * 100

    else:

        savings_rate = 0

    print(
        "\n===== MONTHLY FINANCIAL ANALYSIS ====="
    )

    print(
        f"Month        : {latest_month}"
    )

    print(
        f"Income       : ₹{income:,.2f}"
    )

    print(
        f"Expenses     : ₹{expenses:,.2f}"
    )

    print(
        f"Savings      : ₹{savings:,.2f}"
    )

    print(
        f"Savings Rate : {savings_rate:.2f}%"
    )


def financial_insights():

    connection = get_connection()

    query = """
        SELECT
            type,
            category,
            amount
        FROM transactions
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo transactions found.")

        return

    income = df[
        df["type"] == "Income"
    ]["amount"].sum()

    expenses = df[
        df["type"] == "Expense"
    ]["amount"].sum()

    savings = income - expenses

    if income > 0:

        savings_rate = (
            savings / income
        ) * 100

    else:

        savings_rate = 0

    print(
        "\n===== FINANCIAL INSIGHTS ====="
    )

    if savings_rate >= 30:

        print(
            "✅ Excellent! Your savings rate is above 30%."
        )

    elif savings_rate >= 20:

        print(
            "🟢 Good! Your savings rate is healthy."
        )

    elif savings_rate >= 10:

        print(
            "🟡 Your savings rate is moderate. Try to save more."
        )

    else:

        print(
            "🔴 Warning! Your savings rate is low."
        )

    expense_df = df[
        df["type"] == "Expense"
    ]

    if expense_df.empty:

        print("\nNo expenses found.")

        return

    category_expenses = (
        expense_df
        .groupby("category")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    highest_category = (
        category_expenses.index[0]
    )

    highest_amount = (
        category_expenses.iloc[0]
    )

    print(
        f"💰 Highest spending category: "
        f"{highest_category} "
        f"(₹{highest_amount:,.2f})"
    )

    print(
        "\n📊 Spending breakdown:"
    )

    for category, amount in category_expenses.items():

        percentage = (
            amount / expenses
        ) * 100

        print(
            f"   {category}: "
            f"₹{amount:,.2f} "
            f"({percentage:.1f}%)"
        )