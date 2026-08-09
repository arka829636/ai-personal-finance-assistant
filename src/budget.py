import pandas as pd

from database import get_connection


def budget_analysis():

    connection = get_connection()

    # Get budgets from SQLite
    budget_query = """
        SELECT category, budget
        FROM budgets
        ORDER BY category
    """

    budgets = pd.read_sql_query(
        budget_query,
        connection
    )

    # Get expenses from SQLite
    expense_query = """
        SELECT category, SUM(amount) AS spent
        FROM transactions
        WHERE type = 'Expense'
        GROUP BY category
    """

    spending = pd.read_sql_query(
        expense_query,
        connection
    )

    connection.close()

    print("\n===== BUDGET ANALYSIS =====")

    if budgets.empty:

        print("No budgets found.")

        return

    # Convert spending into dictionary
    spending_dict = dict(
        zip(
            spending["category"],
            spending["spent"]
        )
    )

    for _, row in budgets.iterrows():

        category = row["category"]

        budget = row["budget"]

        spent = spending_dict.get(
            category,
            0
        )

        remaining = budget - spent

        print(f"\n📌 {category}")

        print(
            f"   Budget    : ₹{budget:,.2f}"
        )

        print(
            f"   Spent     : ₹{spent:,.2f}"
        )

        print(
            f"   Remaining : ₹{remaining:,.2f}"
        )

        if spent > budget:

            overspent = spent - budget

            print(
                f"   🔴 OVER BUDGET by "
                f"₹{overspent:,.2f}"
            )

        elif spent >= budget * 0.8:

            print(
                "   🟡 Warning: "
                "You are close to your budget."
            )

        else:

            print(
                "   🟢 Within budget."
            )