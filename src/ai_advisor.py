import pandas as pd

from src.database import get_connection
from src.recommendations import generate_recommendations


def get_financial_data():

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

    return df


def generate_advice():

    df = get_financial_data()

    if df.empty:

        print("\nNo financial data available.")

        return

    # --------------------------------
    # INCOME
    # --------------------------------

    income = df[
        df["type"] == "Income"
    ]["amount"].sum()


    # --------------------------------
    # EXPENSES
    # --------------------------------

    expenses_df = df[
        df["type"] == "Expense"
    ]

    expenses = expenses_df[
        "amount"
    ].sum()


    # --------------------------------
    # SAVINGS
    # --------------------------------

    savings = income - expenses

    if income > 0:

        savings_rate = (
            savings / income
        ) * 100

    else:

        savings_rate = 0


    # --------------------------------
    # HEADER
    # --------------------------------

    print("\n")
    print("======================================")
    print("        🤖 AI FINANCIAL ADVISOR")
    print("======================================")


    # --------------------------------
    # FINANCIAL SUMMARY
    # --------------------------------

    print(
        f"\n💰 Total Income: ₹{income:,.2f}"
    )

    print(
        f"💸 Total Expenses: ₹{expenses:,.2f}"
    )

    print(
        f"💵 Savings: ₹{savings:,.2f}"
    )

    print(
        f"📊 Savings Rate: {savings_rate:.2f}%"
    )


    # --------------------------------
    # AI RECOMMENDATIONS
    # --------------------------------

    print("\n🧠 AI RECOMMENDATIONS:")
    print("--------------------------------------")


    # Savings recommendation

    if savings_rate >= 30:

        print(
            "✅ Excellent savings rate."
        )

        print(
            "   You are saving a healthy portion "
            "of your income."
        )

    elif savings_rate >= 20:

        print(
            "🟢 Good savings rate."
        )

        print(
            "   Try to maintain it consistently."
        )

    elif savings_rate >= 10:

        print(
            "🟡 Your savings rate is moderate."
        )

        print(
            "   Consider reducing unnecessary expenses."
        )

    else:

        print(
            "🔴 Your savings rate is low."
        )

        print(
            "   You should review your spending."
        )


    # --------------------------------
    # HIGHEST SPENDING CATEGORY
    # --------------------------------

    if not expenses_df.empty:

        category_spending = (
            expenses_df
            .groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )

        highest_category = (
            category_spending.index[0]
        )

        highest_amount = (
            category_spending.iloc[0]
        )

        print(
            f"\n📌 Highest spending category: "
            f"{highest_category}"
        )

        print(
            f"   Amount: ₹{highest_amount:,.2f}"
        )


        # --------------------------------
        # SPENDING PERCENTAGE
        # --------------------------------

        if expenses > 0:

            percentage = (
                highest_amount / expenses
            ) * 100


            if percentage > 40:

                print(
                    f"⚠️ {highest_category} represents "
                    f"{percentage:.1f}% of your expenses."
                )

                print(
                    "   Consider reviewing this category."
                )

            else:

                print(
                    f"👍 Your highest category, "
                    f"{highest_category}, represents "
                    f"{percentage:.1f}% of total expenses."
                )


    # --------------------------------
    # SAVINGS STATUS
    # --------------------------------

    if savings > 0:

        print(
            "\n💡 You are currently saving money."
        )

        if savings >= income * 0.30:

            print(
                "   Keep maintaining your current "
                "financial discipline."
            )

        elif savings >= income * 0.20:

            print(
                "   Try to gradually increase your "
                "savings toward 30%."
            )

        else:

            print(
                "   Try to increase your savings "
                "over the coming months."
            )

    else:

        print(
            "\n🚨 Your expenses are higher than "
            "or equal to your income."
        )

        print(
            "   Review your spending immediately."
        )


    # --------------------------------
    # RECOMMENDATION ENGINE
    # --------------------------------

    print("\n")
    print("======================================")
    print("      💡 FINANCIAL RECOMMENDATIONS")
    print("======================================")

    generate_recommendations()


    # --------------------------------
    # END
    # --------------------------------

    print("\n======================================")
    print("       ADVISOR ANALYSIS COMPLETE")
    print("======================================")


# --------------------------------
# DIRECT EXECUTION
# --------------------------------

if __name__ == "__main__":

    generate_advice()