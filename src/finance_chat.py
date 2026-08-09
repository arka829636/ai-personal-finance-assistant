import sqlite3
import os
import pandas as pd


# =========================================================
# DATABASE PATH
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "data",
    "finance.db"
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    return sqlite3.connect(
        DB_PATH
    )


# =========================================================
# LOAD TRANSACTIONS
# =========================================================

def get_transactions():

    connection = get_connection()

    query = """
        SELECT
            id,
            date,
            type,
            category,
            description,
            amount,
            payment_method
        FROM transactions
        ORDER BY date
    """

    try:

        df = pd.read_sql_query(
            query,
            connection
        )

    finally:

        connection.close()

    return df


# =========================================================
# FINANCIAL SUMMARY
# =========================================================

def get_summary():

    df = get_transactions()

    if df.empty:

        return {
            "income": 0,
            "expenses": 0,
            "savings": 0,
            "savings_rate": 0
        }

    income = df[
        df["type"].str.lower() == "income"
    ]["amount"].sum()

    expenses = df[
        df["type"].str.lower() == "expense"
    ]["amount"].sum()

    savings = income - expenses

    savings_rate = (
        savings / income * 100
        if income > 0
        else 0
    )

    return {
        "income": income,
        "expenses": expenses,
        "savings": savings,
        "savings_rate": savings_rate
    }


# =========================================================
# CATEGORY SPENDING
# =========================================================

def get_category_spending():

    df = get_transactions()

    expenses = df[
        df["type"].str.lower() == "expense"
    ]

    if expenses.empty:

        return pd.Series(dtype=float)

    return (
        expenses
        .groupby("category")["amount"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


# =========================================================
# ANSWER USER QUESTION
# =========================================================

def answer_question(question):

    question = question.lower().strip()

    summary = get_summary()

    # -----------------------------------------
    # INCOME
    # -----------------------------------------

    if (
        "income" in question
        or "salary" in question
        or "earned" in question
    ):

        return (
            f"💵 Your total income is "
            f"₹{summary['income']:,.2f}."
        )

    # -----------------------------------------
    # EXPENSES
    # -----------------------------------------

    if (
        "expense" in question
        or "spent" in question
        or "spending" in question
        or "spend" in question
    ):

        return (
            f"💸 Your total expenses are "
            f"₹{summary['expenses']:,.2f}."
        )

    # -----------------------------------------
    # SAVINGS
    # -----------------------------------------

    if (
        "saving" in question
        or "saved" in question
    ):

        return (
            f"💰 Your savings are "
            f"₹{summary['savings']:,.2f} "
            f"with a savings rate of "
            f"{summary['savings_rate']:.2f}%."
        )

    # -----------------------------------------
    # HIGHEST SPENDING
    # -----------------------------------------

    if (
        "highest" in question
        or "most" in question
        or "biggest" in question
        or "category" in question
    ):

        category_data = (
            get_category_spending()
        )

        if category_data.empty:

            return (
                "No expense data is available."
            )

        category = category_data.index[0]

        amount = category_data.iloc[0]

        return (
            f"📌 Your highest spending "
            f"category is {category} "
            f"with spending of "
            f"₹{amount:,.2f}."
        )

    # -----------------------------------------
    # TRANSACTION COUNT
    # -----------------------------------------

    if (
        "transaction" in question
        or "transactions" in question
    ):

        df = get_transactions()

        return (
            f"🧾 You have "
            f"{len(df)} transactions "
            f"recorded."
        )

    # -----------------------------------------
    # ADVICE
    # -----------------------------------------

    if (
        "advice" in question
        or "suggest" in question
        or "recommend" in question
        or "recommendation" in question
    ):

        rate = summary["savings_rate"]

        if rate >= 30:

            return (
                "🟢 Your savings rate is excellent. "
                "Keep maintaining your current "
                "financial discipline."
            )

        elif rate >= 20:

            return (
                "🟡 Your savings rate is good. "
                "Try to maintain it consistently."
            )

        elif rate >= 10:

            return (
                "🟠 Your savings rate is moderate. "
                "Consider reducing unnecessary "
                "expenses."
            )

        else:

            return (
                "🔴 Your savings rate is low. "
                "Review your spending and try "
                "to increase your savings."
            )

    # -----------------------------------------
    # HELP
    # -----------------------------------------

    return (
        "🤖 I can help you with questions about:\n\n"
        "• Total income\n"
        "• Total expenses\n"
        "• Savings\n"
        "• Savings rate\n"
        "• Highest spending category\n"
        "• Transaction count\n"
        "• Financial recommendations\n\n"
        "Try asking: "
        "'How much did I spend?'"
    )


# =========================================================
# TERMINAL CHAT
# =========================================================

def run_chat():

    print()
    print("=" * 55)
    print("💬 AI PERSONAL FINANCE CHAT ASSISTANT")
    print("=" * 55)

    print(
        "\nAsk questions about your finances."
    )

    print(
        "Type 'exit' to stop."
    )

    while True:

        question = input(
            "\nYou: "
        )

        if question.lower().strip() in [
            "exit",
            "quit",
            "q"
        ]:

            print(
                "\nFinance Chat closed."
            )

            break

        answer = answer_question(
            question
        )

        print(
            f"\n🤖 Assistant: {answer}"
        )


# =========================================================
# DIRECT EXECUTION
# =========================================================

if __name__ == "__main__":

    run_chat()