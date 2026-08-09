import pandas as pd
from src.database import get_connection


def generate_recommendations():

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

        print("\n🤖 Assistant: No financial data available.")

        return


    # --------------------------------
    # BASIC CALCULATIONS
    # --------------------------------

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


    # --------------------------------
    # CATEGORY ANALYSIS
    # --------------------------------

    expense_data = df[
        df["type"] == "Expense"
    ]

    category_spending = (
        expense_data
        .groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
    )


    print("\n======================================")
    print("🤖 AI FINANCIAL RECOMMENDATIONS")
    print("======================================")

    print(
        f"\n💰 Income: ₹{income:,.2f}"
    )

    print(
        f"💸 Expenses: ₹{expenses:,.2f}"
    )

    print(
        f"💵 Savings: ₹{savings:,.2f}"
    )

    print(
        f"📊 Savings Rate: {savings_rate:.2f}%"
    )


    print("\n💡 Recommendations:")


    # --------------------------------
    # SAVINGS RECOMMENDATION
    # --------------------------------

    if savings_rate >= 30:

        print(
            "✅ Excellent savings rate. "
            "Continue maintaining your current discipline."
        )

    elif savings_rate >= 20:

        print(
            "👍 Your savings rate is good. "
            "Try to gradually increase it toward 30%."
        )

    elif savings_rate >= 10:

        print(
            "⚠️ Your savings rate could be improved. "
            "Try reducing unnecessary expenses."
        )

    else:

        print(
            "🚨 Your savings rate is low. "
            "Prioritize essential expenses and reduce "
            "non-essential spending."
        )


    # --------------------------------
    # HIGHEST CATEGORY
    # --------------------------------

    if not category_spending.empty:

        highest_category = (
            category_spending.index[0]
        )

        highest_amount = (
            category_spending.iloc[0]
        )

        print(
            f"📌 Highest spending category: "
            f"{highest_category} "
            f"(₹{highest_amount:,.2f})"
        )


        # --------------------------------
        # CATEGORY RECOMMENDATION
        # --------------------------------

        if income > 0:

            category_percentage = (
                highest_amount / income
            ) * 100

        else:

            category_percentage = 0


        if category_percentage > 30:

            print(
                f"⚠️ {highest_category} takes up "
                f"{category_percentage:.1f}% of your income. "
                f"Consider reducing spending in this category."
            )

        elif category_percentage > 20:

            print(
                f"💡 Consider monitoring your "
                f"{highest_category} expenses."
            )

        else:

            print(
                f"✅ Your {highest_category} spending "
                f"does not appear excessive based on income."
            )


    # --------------------------------
    # GENERAL RECOMMENDATIONS
    # --------------------------------

    print(
        "\n📋 General recommendations:"
    )

    print(
        "1. Track every expense."
    )

    print(
        "2. Set monthly limits for non-essential spending."
    )

    print(
        "3. Build an emergency fund."
    )

    print(
        "4. Review your spending categories regularly."
    )

    print(
        "5. Try to increase your savings gradually."
    )


if __name__ == "__main__":

    generate_recommendations()